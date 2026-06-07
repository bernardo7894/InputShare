package com.inputshare.keepawake;

import android.accessibilityservice.AccessibilityService;
import android.os.Bundle;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class SendActionAccessibilityService extends AccessibilityService {
    private static SendActionAccessibilityService instance;

    @Override
    public void onServiceConnected() {
        instance = this;
    }

    @Override
    public void onDestroy() {
        if (instance == this) {
            instance = null;
        }
        super.onDestroy();
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
    }

    @Override
    public void onInterrupt() {
    }

    public static boolean requestSend() {
        SendActionAccessibilityService service = instance;
        return service != null && service.performSend();
    }

    private boolean performSend() {
        List<AccessibilityNodeInfo> roots = new ArrayList<>();
        AccessibilityNodeInfo root = getRootInActiveWindow();
        if (root != null) {
            roots.add(root);
        }
        if (android.os.Build.VERSION.SDK_INT >= 21) {
            for (android.view.accessibility.AccessibilityWindowInfo window : getWindows()) {
                AccessibilityNodeInfo windowRoot = window.getRoot();
                if (windowRoot != null && windowRoot != root) {
                    roots.add(windowRoot);
                }
            }
        }

        for (AccessibilityNodeInfo candidateRoot : roots) {
            AccessibilityNodeInfo sendNode = findSendNode(candidateRoot);
            if (sendNode != null && clickNode(sendNode)) {
                recycleRoots(roots);
                return true;
            }
        }

        recycleRoots(roots);
        return false;
    }

    private AccessibilityNodeInfo findSendNode(AccessibilityNodeInfo node) {
        if (node == null) {
            return null;
        }

        if (isSendCandidate(node)) {
            return node;
        }

        for (int i = 0; i < node.getChildCount(); i++) {
            AccessibilityNodeInfo child = node.getChild(i);
            AccessibilityNodeInfo found = findSendNode(child);
            if (found != null) {
                return found;
            }
            if (child != null) {
                child.recycle();
            }
        }
        return null;
    }

    private boolean isSendCandidate(AccessibilityNodeInfo node) {
        if (!node.isVisibleToUser() || !node.isEnabled()) {
            return false;
        }

        CharSequence text = node.getText();
        CharSequence description = node.getContentDescription();
        CharSequence viewId = android.os.Build.VERSION.SDK_INT >= 18 ? node.getViewIdResourceName() : null;

        return isSendLabel(text)
            || isSendLabel(description)
            || isSendViewId(viewId);
    }

    private boolean isSendLabel(CharSequence label) {
        if (label == null) {
            return false;
        }
        String value = label.toString().trim().toLowerCase(Locale.ROOT);
        return value.equals("send")
            || value.equals("enviar")
            || value.equals("send message")
            || value.equals("enviar mensagem")
            || value.equals("send prompt")
            || value.equals("submit")
            || value.equals("submit message");
    }

    private boolean isSendViewId(CharSequence viewId) {
        if (viewId == null) {
            return false;
        }
        String value = viewId.toString().toLowerCase(Locale.ROOT);
        return value.contains("send")
            || value.contains("submit");
    }

    private boolean clickNode(AccessibilityNodeInfo node) {
        AccessibilityNodeInfo current = node;
        while (current != null) {
            if (current.isClickable() && current.performAction(AccessibilityNodeInfo.ACTION_CLICK)) {
                return true;
            }
            AccessibilityNodeInfo parent = current.getParent();
            if (current != node) {
                current.recycle();
            }
            current = parent;
        }
        return false;
    }

    private void recycleRoots(List<AccessibilityNodeInfo> roots) {
        for (AccessibilityNodeInfo root : roots) {
            if (root != null) {
                root.recycle();
            }
        }
    }
}
