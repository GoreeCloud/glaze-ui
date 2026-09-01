package com.goreecloud.glazeui.reference.android22;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.inputmethod.InputMethodManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.drawable.GradientDrawable;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.TextView;

public final class MainActivity extends Activity {
    private int targetDp = 48;
    private int canvas;
    private int surface;
    private int raised;
    private int textPrimary;
    private int textSecondary;
    private int accent;
    private int line;
    private boolean reducedTransparency;
    private boolean deleteConfirming;

    private LinearLayout root;
    private LinearLayout searchPanel;
    private LinearLayout controlPanel;
    private EditText searchInput;
    private TextView panelState;
    private TextView actionState;
    private Button deleteButton;
    private Button wifiButton;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        Intent intent = getIntent();
        String appearance = intent.getStringExtra("appearance");
        if (appearance == null) appearance = "light";
        reducedTransparency = intent.getBooleanExtra("reducedTransparency", false);
        boolean touchAssistance = intent.getBooleanExtra("touchAssistance", false);
        targetDp = touchAssistance ? 56 : 48;
        configurePalette(appearance);
        configureWindow();
        setContentView(buildUi(appearance, touchAssistance));
    }

    private void configurePalette(String appearance) {
        if ("deep-dark".equals(appearance)) {
            canvas = Color.rgb(5, 7, 10);
            surface = Color.rgb(13, 16, 21);
            raised = Color.rgb(23, 28, 35);
            textPrimary = Color.rgb(245, 247, 250);
            textSecondary = Color.rgb(171, 180, 194);
            accent = Color.rgb(141, 181, 255);
            line = Color.rgb(62, 70, 82);
        } else if ("dark".equals(appearance)) {
            canvas = Color.rgb(11, 13, 17);
            surface = Color.rgb(18, 21, 27);
            raised = Color.rgb(27, 32, 40);
            textPrimary = Color.rgb(245, 247, 250);
            textSecondary = Color.rgb(176, 183, 195);
            accent = Color.rgb(141, 181, 255);
            line = Color.rgb(63, 70, 82);
        } else {
            canvas = Color.rgb(245, 247, 250);
            surface = Color.WHITE;
            raised = Color.rgb(250, 251, 253);
            textPrimary = Color.rgb(21, 26, 35);
            textSecondary = Color.rgb(93, 102, 117);
            accent = Color.rgb(52, 120, 246);
            line = Color.rgb(214, 219, 226);
        }
    }

    private void configureWindow() {
        Window window = getWindow();
        window.setStatusBarColor(canvas);
        window.setNavigationBarColor(canvas);
        window.getDecorView().setSystemUiVisibility(textPrimary == Color.rgb(21, 26, 35)
                ? View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
                : 0);
    }

    private View buildUi(String appearance, boolean touchAssistance) {
        FrameLayout safeHost = new FrameLayout(this);
        safeHost.setBackgroundColor(canvas);
        safeHost.setClipChildren(true);
        safeHost.setClipToPadding(true);

        FrameLayout viewport = new FrameLayout(this);
        viewport.setBackgroundColor(canvas);
        viewport.setClipChildren(true);
        viewport.setClipToPadding(true);

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(canvas);
        scroll.setClipToPadding(true);

        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(18), dp(18), dp(18), dp(28));
        scroll.addView(root, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT));

        viewport.addView(scroll, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT));
        FrameLayout.LayoutParams viewportParams = new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT);
        safeHost.addView(viewport, viewportParams);
        safeHost.setOnApplyWindowInsetsListener((v, insets) -> {
            FrameLayout.LayoutParams params = (FrameLayout.LayoutParams) viewport.getLayoutParams();
            params.setMargins(
                    insets.getSystemWindowInsetLeft(),
                    insets.getSystemWindowInsetTop(),
                    insets.getSystemWindowInsetRight(),
                    insets.getSystemWindowInsetBottom());
            viewport.setLayoutParams(params);
            return insets;
        });
        safeHost.requestApplyInsets();

        root.addView(label("Glaze UI 2.2 Candidate", 28, true));
        root.addView(label("Current Stable: 2.1.0", 15, false));
        root.addView(spacer(8));
        root.addView(label("Native Android System Shell reference", 18, true));
        root.addView(label("Workspace → Application → System Overlay → System Panel → Critical System", 14, false));
        root.addView(spacer(12));

        String appearanceLabel = "deep-dark".equals(appearance) ? "Deep Dark" : "dark".equals(appearance) ? "Dark" : "Light";
        root.addView(infoCard("Appearance: " + appearanceLabel));
        root.addView(infoCard("Target floor: " + targetDp + " dp"));
        root.addView(infoCard(touchAssistance ? "Touch Assistance: 56 dp minimum target" : "Touch Assistance: Off"));
        root.addView(infoCard(reducedTransparency
                ? "Reduced Transparency: Solid system panels"
                : "Transparency: Native effects are optional; semantics do not depend on blur"));
        root.addView(infoCard("System Glaze budget: one dominant panel"));
        root.addView(spacer(12));

        boolean largeText = getResources().getConfiguration().fontScale >= 1.5f;
        LinearLayout launcherRow = new LinearLayout(this);
        launcherRow.setOrientation(largeText ? LinearLayout.VERTICAL : LinearLayout.HORIZONTAL);
        launcherRow.setGravity(Gravity.CENTER_VERTICAL);
        Button searchButton = actionButton("Open Search");
        searchButton.setContentDescription("Open Universal Search");
        Button controlButton = actionButton("Open Control Center");
        if (largeText) {
            launcherRow.addView(searchButton, matchWrapTarget());
            LinearLayout.LayoutParams controlParams = matchWrapTarget();
            controlParams.topMargin = dp(8);
            launcherRow.addView(controlButton, controlParams);
        } else {
            launcherRow.addView(searchButton, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            LinearLayout.LayoutParams controlParams = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
            controlParams.setMarginStart(dp(8));
            launcherRow.addView(controlButton, controlParams);
        }
        root.addView(launcherRow);

        panelState = label("Dominant panel: None", 14, false);
        panelState.setContentDescription("Dominant panel state");
        root.addView(panelState);
        root.addView(spacer(10));

        searchPanel = panelContainer("Universal Search");
        searchPanel.setVisibility(View.GONE);
        searchInput = new EditText(this);
        searchInput.setSingleLine(true);
        searchInput.setHint("Search everything");
        searchInput.setHintTextColor(textSecondary);
        searchInput.setTextColor(textPrimary);
        searchInput.setContentDescription("Search everything");
        searchInput.setMinHeight(dp(targetDp));
        searchInput.setPadding(dp(12), dp(8), dp(12), dp(8));
        searchInput.setBackground(panelShape(raised, 14));
        searchPanel.addView(searchInput, matchWrap());
        searchPanel.addView(sectionLabel("BEST MATCH"));
        Button projectResult = actionButton("Project Brief");
        projectResult.setContentDescription("Project Brief, File, exact match");
        searchPanel.addView(projectResult, matchTarget());
        searchPanel.addView(sectionLabel("ACTIONS"));
        Button appearanceResult = actionButton("Appearance settings");
        searchPanel.addView(appearanceResult, matchTarget());
        deleteButton = actionButton("Delete local cache");
        deleteButton.setContentDescription("Delete local cache, destructive action");
        searchPanel.addView(deleteButton, matchTarget());
        TextView generated = infoCard("Generated answer · Source: Project Brief");
        generated.setContentDescription("Generated answer. Source Project Brief.");
        searchPanel.addView(generated);
        actionState = label("Search action: None", 14, false);
        actionState.setContentDescription("Search action state");
        searchPanel.addView(actionState);
        root.addView(searchPanel, matchWrap());

        controlPanel = panelContainer("Control Center");
        controlPanel.setVisibility(View.GONE);
        wifiButton = actionButton("Wi-Fi: On");
        wifiButton.setContentDescription("Wi-Fi toggle, on");
        controlPanel.addView(wifiButton, matchTarget());
        Button bluetoothButton = actionButton("Bluetooth: On");
        bluetoothButton.setContentDescription("Bluetooth toggle, on");
        controlPanel.addView(bluetoothButton, matchTarget());
        controlPanel.addView(sectionLabel("Brightness"));
        SeekBar brightness = range("Brightness", 64);
        controlPanel.addView(brightness, matchTarget());
        controlPanel.addView(sectionLabel("Volume"));
        SeekBar volume = range("Volume", 64);
        controlPanel.addView(volume, matchTarget());
        Button focusButton = actionButton("Focus: Off");
        focusButton.setContentDescription("Focus toggle, off");
        controlPanel.addView(focusButton, matchTarget());
        Button mediaButton = actionButton("Media: Playing");
        mediaButton.setContentDescription("Media playback toggle, playing");
        controlPanel.addView(mediaButton, matchTarget());
        root.addView(controlPanel, matchWrap());

        TextView boundary = infoCard("Reference boundary: emulator-native interaction evidence only; no live GoreeCloud state, physical-device certification, TalkBack acceptance, signing, distribution, or human Visual Excellence claim.");
        LinearLayout.LayoutParams boundaryParams = matchWrap();
        boundaryParams.topMargin = dp(14);
        root.addView(boundary, boundaryParams);

        searchButton.setOnClickListener(v -> openSearch());
        controlButton.setOnClickListener(v -> openControlCenter());
        projectResult.setOnClickListener(v -> actionState.setText("Search action: Opened Project Brief"));
        appearanceResult.setOnClickListener(v -> actionState.setText("Search action: Opened Appearance settings"));
        deleteButton.setOnClickListener(v -> handleDelete());
        wifiButton.setOnClickListener(v -> toggleButton(wifiButton, "Wi-Fi"));
        bluetoothButton.setOnClickListener(v -> toggleButton(bluetoothButton, "Bluetooth"));
        focusButton.setOnClickListener(v -> toggleButton(focusButton, "Focus"));
        mediaButton.setOnClickListener(v -> toggleMedia(mediaButton));

        return safeHost;
    }

    private void openSearch() {
        controlPanel.setVisibility(View.GONE);
        searchPanel.setVisibility(View.VISIBLE);
        panelState.setText("Dominant panel: Universal Search");
        deleteConfirming = false;
        deleteButton.setText("Delete local cache");
        searchInput.requestFocus();
        searchInput.post(() -> {
            InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
            if (imm != null) imm.showSoftInput(searchInput, InputMethodManager.SHOW_IMPLICIT);
        });
    }

    private void openControlCenter() {
        searchPanel.setVisibility(View.GONE);
        controlPanel.setVisibility(View.VISIBLE);
        panelState.setText("Dominant panel: Control Center");
        wifiButton.requestFocus();
    }

    private void handleDelete() {
        if (!deleteConfirming) {
            deleteConfirming = true;
            deleteButton.setText("Confirm Delete local cache");
            actionState.setText("Search action: Confirmation required");
            return;
        }
        deleteConfirming = false;
        deleteButton.setText("Delete local cache");
        actionState.setText("Search action: Deleted local cache");
    }

    private void toggleButton(Button button, String name) {
        boolean on = button.getText().toString().endsWith("On");
        button.setText(name + ": " + (on ? "Off" : "On"));
        button.setContentDescription(name + " toggle, " + (on ? "off" : "on"));
    }

    private void toggleMedia(Button button) {
        boolean playing = button.getText().toString().contains("Playing");
        button.setText("Media: " + (playing ? "Paused" : "Playing"));
        button.setContentDescription("Media playback toggle, " + (playing ? "paused" : "playing"));
    }

    private SeekBar range(String name, int initial) {
        SeekBar bar = new SeekBar(this);
        bar.setMax(100);
        bar.setProgress(initial);
        bar.setMinHeight(dp(targetDp));
        bar.setContentDescription(name + " " + initial + " percent");
        bar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                seekBar.setContentDescription(name + " " + progress + " percent");
            }
            @Override public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override public void onStopTrackingTouch(SeekBar seekBar) {}
        });
        return bar;
    }

    private LinearLayout panelContainer(String title) {
        LinearLayout panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        panel.setPadding(dp(14), dp(14), dp(14), dp(14));
        panel.setBackground(panelShape(reducedTransparency ? raised : surface, 22));
        panel.setContentDescription(title + " system panel");
        panel.addView(label(title, 20, true));
        panel.addView(label("Only one dominant system panel may be open.", 13, false));
        return panel;
    }

    private TextView label(String text, int sp, boolean strong) {
        TextView view = new TextView(this);
        view.setText(text);
        view.setTextColor(strong ? textPrimary : textSecondary);
        view.setTextSize(sp);
        view.setPadding(0, dp(3), 0, dp(3));
        if (strong) view.setTypeface(view.getTypeface(), android.graphics.Typeface.BOLD);
        return view;
    }

    private TextView sectionLabel(String text) {
        TextView view = label(text, 12, true);
        LinearLayout.LayoutParams params = matchWrap();
        params.topMargin = dp(10);
        view.setLayoutParams(params);
        return view;
    }

    private TextView infoCard(String text) {
        TextView view = label(text, 14, false);
        view.setTextColor(textPrimary);
        view.setPadding(dp(12), dp(10), dp(12), dp(10));
        view.setBackground(panelShape(raised, 14));
        LinearLayout.LayoutParams params = matchWrap();
        params.bottomMargin = dp(7);
        view.setLayoutParams(params);
        return view;
    }

    private Button actionButton(String text) {
        Button button = new Button(this);
        button.setAllCaps(false);
        button.setText(text);
        button.setTextColor(textPrimary);
        button.setTextSize(15);
        button.setMinHeight(dp(targetDp));
        button.setMinimumHeight(dp(targetDp));
        button.setGravity(Gravity.CENTER_VERTICAL | Gravity.START);
        button.setSingleLine(false);
        button.setMaxLines(3);
        button.setPadding(dp(14), dp(8), dp(14), dp(8));
        button.setBackground(panelShape(raised, 14));
        button.setStateListAnimator(null);
        return button;
    }

    private GradientDrawable panelShape(int color, int radiusDp) {
        GradientDrawable drawable = new GradientDrawable();
        drawable.setColor(color);
        drawable.setCornerRadius(dp(radiusDp));
        drawable.setStroke(dp(1), line);
        return drawable;
    }

    private View spacer(int heightDp) {
        View view = new View(this);
        view.setLayoutParams(new LinearLayout.LayoutParams(1, dp(heightDp)));
        return view;
    }

    private LinearLayout.LayoutParams matchWrap() {
        return new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    private LinearLayout.LayoutParams matchWrapTarget() {
        return new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    private LinearLayout.LayoutParams matchTarget() {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        params.topMargin = dp(6);
        return params;
    }

    private int dp(float value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
