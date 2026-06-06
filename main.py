import socket
import sys
from typing import Callable

from adbutils import AdbInstallError
from multiprocessing import freeze_support
from server import deploy_reporter_server, deploy_scrcpy_server, scrcpy_receiver, reporter_receiver
from input.callbacks import callback_context_wrapper
from ui.connecting_window import open_connecting_window
from ui.tray import tray_thread_factory
from utils.adb_controller import (
    ADBWiredConnectionError,
    append_adb_device,
    get_adb_client,
    start_adb_server,
    start_keep_awake_helper,
    stop_keep_awake_helper,
    try_connect_device,
)
from utils.config_manager import get_config
from utils.i18n import get_i18n
from utils.logger import LogType, LOGGER
from utils.notification import Notification, send_notification
from utils.network import get_ip_from_ip_port, is_valid_ip, is_valid_ip_port, scan_port

def close_notification_resolver(errno: Exception | None):
    close_notification = None
    i18n = get_i18n()
    match errno:
        case None: pass
        case ADBWiredConnectionError():
            close_notification = Notification(
                i18n(["ConnectionError", "连接错误"]),
                i18n(["Wired connection failed, please check if the device is connected correctly.", "有线连接失败，请检查是否正确连接设备。"]))
        case scrcpy_receiver.InvalidDummyByteException():
            close_notification = Notification(
                i18n(["NetworkError", "网络错误"]),
                i18n(["Connection with device failed, please retry.", "设备连接失败，请重试。"]))
        case AdbInstallError():
            close_notification = Notification(
                i18n(["NetworkError", "网络错误"]),
                i18n(["Android client installation failed, please retry.", "安卓客户端安装失败，请重试。"]))
        case socket.timeout | TimeoutError():
            close_notification = Notification(
                i18n(["NetworkError", "网络错误"]),
                i18n(["Connection with device timeout, please retry.", "设备连接超时，请重试。"]))
        case ConnectionAbortedError() | ConnectionResetError():
            close_notification = Notification(
                i18n(["NetworkError", "网络错误"]),
                i18n(["Unexpected connection aborted.", "连接意外中断。"]))
        case _:
            error_name = errno.__class__.__name__
            close_notification = Notification(
                i18n(["Error", "错误"]),
                i18n([f"Unknown error: {error_name}", f"未知错误：{error_name}"]))
    get_adb_client().server_kill()
    LOGGER.write(LogType.Adb, "ADB server killed.")
    LOGGER.write(LogType.Info, "Program terminated with: " + str(close_notification))
    send_notification(close_notification)

def try_connect_saved_device() -> bool:
    config = get_config()
    saved_addr = (config.device_addr1 or config.device_ip1).strip()
    if len(saved_addr) == 0: return False

    if is_valid_ip_port(saved_addr):
        return try_connect_device(saved_addr) is not None

    if not config.scan_port or not is_valid_ip(saved_addr):
        return False

    for port in scan_port(saved_addr):
        connect_addr = f"{saved_addr}:{port}"
        if try_connect_device(connect_addr) is not None:
            config.device_addr1 = connect_addr
            config.device_ip1 = get_ip_from_ip_port(connect_addr)
            return True
    return False

if __name__ == "__main__":
    freeze_support()

    scrcpy_server_process = None
    stop_scrcpy_receiver: Callable | None = None
    stop_reporter_receiver: Callable | None = None
    close_tray: Callable | None = None
    main_errno: Exception | None = None
    keep_awake_helper_started = False

    try:
        start_adb_server()
        if not try_connect_saved_device():
            is_wired_connection = open_connecting_window()
            if is_wired_connection:
                device_list = get_adb_client().device_list()
                if len(device_list) == 0:
                    # selected wired connection
                    main_errno = ADBWiredConnectionError()
                    sys.exit(1)
                append_adb_device(device_list[0])

        res = deploy_scrcpy_server()
        if isinstance(res, Exception):
            main_errno = res
            sys.exit(1)
        scrcpy_server_process, scrcpy_client_socket = res

        stop_scrcpy_receiver = scrcpy_receiver.server_receiver_factory(scrcpy_client_socket)

        if get_config().edge_toggling:
            res = deploy_reporter_server()
            if isinstance(res, Exception):
                main_errno = res
                sys.exit(1)
            stop_reporter_receiver = reporter_receiver.server_receiver_factory()

        if get_config().keep_wakeup:
            keep_awake_helper_started = start_keep_awake_helper()

        close_tray = tray_thread_factory(scrcpy_client_socket)
        callbacks  = callback_context_wrapper(scrcpy_client_socket)

        from input.controller import main_loop
        main_errno = main_loop(*callbacks)
    except KeyboardInterrupt:
        LOGGER.write(LogType.Info, "Interrupted from terminal.")
    finally:
        LOGGER.write(LogType.Info, "Terminated, closing...")
        if keep_awake_helper_started:
            stop_keep_awake_helper()
        stop_scrcpy_receiver and stop_scrcpy_receiver()
        stop_reporter_receiver and stop_reporter_receiver()
        scrcpy_server_process and scrcpy_server_process.terminate()
        close_notification_resolver(main_errno)
        close_tray and close_tray()
