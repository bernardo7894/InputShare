package com.inputshare.keepawake;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.graphics.PixelFormat;
import android.os.Build;
import android.os.IBinder;
import android.provider.Settings;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;

public class KeepAwakeService extends Service {
    private static final String CHANNEL_ID = "inputshare_keep_awake";
    private static final int NOTIFICATION_ID = 1;
    public static final String EXTRA_SEND_MESSAGE = "send_message";

    private WindowManager windowManager;
    private View keepAwakeView;

    @Override
    public void onCreate() {
        super.onCreate();
        windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        boolean stop = intent != null && intent.getBooleanExtra("stop", false);
        if (stop) {
            stopSelf();
            return START_NOT_STICKY;
        }
        boolean sendMessage = intent != null && intent.getBooleanExtra(EXTRA_SEND_MESSAGE, false);
        if (sendMessage) {
            SendActionAccessibilityService.requestSend();
            return START_NOT_STICKY;
        }

        startForeground(NOTIFICATION_ID, buildNotification());
        showKeepAwakeOverlay();
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        hideKeepAwakeOverlay();
        stopForeground(true);
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private Notification buildNotification() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "InputShare Keep Awake",
                NotificationManager.IMPORTANCE_LOW
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
        }

        Notification.Builder builder = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
            ? new Notification.Builder(this, CHANNEL_ID)
            : new Notification.Builder(this);

        return builder
            .setContentTitle("InputShare connected")
            .setContentText("Keeping the screen awake")
            .setSmallIcon(android.R.drawable.ic_menu_view)
            .setOngoing(true)
            .build();
    }

    private void showKeepAwakeOverlay() {
        if (keepAwakeView != null) {
            return;
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(this)) {
            return;
        }

        keepAwakeView = new View(this);
        keepAwakeView.setAlpha(0.01f);

        int windowType = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
            ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            : WindowManager.LayoutParams.TYPE_PHONE;

        WindowManager.LayoutParams params = new WindowManager.LayoutParams(
            1,
            1,
            windowType,
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON
                | WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                | WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE
                | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        );
        params.gravity = Gravity.TOP | Gravity.LEFT;

        try {
            windowManager.addView(keepAwakeView, params);
        } catch (RuntimeException e) {
            keepAwakeView = null;
        }
    }

    private void hideKeepAwakeOverlay() {
        if (keepAwakeView == null) {
            return;
        }
        try {
            windowManager.removeView(keepAwakeView);
        } catch (RuntimeException ignored) {
        } finally {
            keepAwakeView = null;
        }
    }
}
