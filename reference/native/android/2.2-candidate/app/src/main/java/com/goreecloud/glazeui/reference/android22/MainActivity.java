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
    private int ambientA;
    private int ambientB;
    private int surface;
    private int raised;
    private int glassSoft;
    private int glassStrong;
    private int accentSoft;
    private int textPrimary;
    private int textSecondary;
    private int accent;
    private int line;
    private boolean reducedTransparency;
    private boolean deleteConfirming;
    private boolean largeText;

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
        largeText = getResources().getConfiguration().fontScale >= 1.5f;
        configurePalette(appearance);
        configureWindow();
        setContentView(buildUi(appearance, touchAssistance));
    }

    private void configurePalette(String appearance) {
        if ("deep-dark".equals(appearance)) {
            canvas = Color.rgb(4, 6, 10);
            ambientA = Color.rgb(9, 18, 34);
            ambientB = Color.rgb(22, 12, 34);
            surface = Color.rgb(14, 17, 23);
            raised = Color.rgb(29, 35, 45);
            glassSoft = Color.argb(214, 24, 30, 40);
            glassStrong = Color.argb(238, 22, 27, 36);
            accentSoft = Color.argb(92, 99, 145, 255);
            textPrimary = Color.rgb(246, 248, 252);
            textSecondary = Color.rgb(177, 186, 201);
            accent = Color.rgb(125, 166, 255);
            line = Color.rgb(73, 82, 98);
        } else if ("dark".equals(appearance)) {
            canvas = Color.rgb(9, 12, 18);
            ambientA = Color.rgb(19, 34, 58);
            ambientB = Color.rgb(38, 25, 58);
            surface = Color.rgb(20, 24, 32);
            raised = Color.rgb(34, 40, 51);
            glassSoft = Color.argb(218, 31, 38, 49);
            glassStrong = Color.argb(240, 27, 33, 43);
            accentSoft = Color.argb(92, 88, 139, 255);
            textPrimary = Color.rgb(246, 248, 252);
            textSecondary = Color.rgb(181, 189, 202);
            accent = Color.rgb(125, 166, 255);
            line = Color.rgb(75, 83, 98);
        } else {
            canvas = Color.rgb(240, 246, 255);
            ambientA = Color.rgb(218, 233, 255);
            ambientB = Color.rgb(238, 226, 255);
            surface = Color.rgb(250, 252, 255);
            raised = Color.WHITE;
            glassSoft = Color.argb(218, 251, 253, 255);
            glassStrong = Color.argb(240, 252, 253, 255);
            accentSoft = Color.argb(64, 72, 124, 246);
            textPrimary = Color.rgb(21, 26, 35);
            textSecondary = Color.rgb(91, 101, 117);
            accent = Color.rgb(66, 113, 236);
            line = Color.rgb(198, 207, 221);
        }
        if (reducedTransparency) {
            glassSoft = raised;
            glassStrong = surface;
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
        safeHost.setBackground(ambientBackground());
        safeHost.setClipChildren(true);
        safeHost.setClipToPadding(true);

        FrameLayout viewport = new FrameLayout(this);
        viewport.setBackgroundColor(Color.TRANSPARENT);
        viewport.setClipChildren(true);
        viewport.setClipToPadding(true);

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(Color.TRANSPARENT);
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
        final int largeTextSystemChromeSafety = largeText ? dp(8) : 0;
        safeHost.setOnApplyWindowInsetsListener((v, insets) -> {
            FrameLayout.LayoutParams params = (FrameLayout.LayoutParams) viewport.getLayoutParams();
            params.setMargins(
                    insets.getSystemWindowInsetLeft(),
                    insets.getSystemWindowInsetTop() + largeTextSystemChromeSafety,
                    insets.getSystemWindowInsetRight(),
                    insets.getSystemWindowInsetBottom());
            viewport.setLayoutParams(params);
            return insets;
        });
        safeHost.requestApplyInsets();

        TextView title = label("Glaze UI 2.2 Candidate", 28, true);
        title.setTextColor(textPrimary);
        root.addView(title);
        root.addView(label("Optical Reachability · Native Android reference", 14, false));
        root.addView(spacer(7));
        TextView hierarchy = label("Workspace → Application → System Overlay → System Panel → Critical System", 13, false);
        hierarchy.setPadding(0, 0, 0, dp(5));
        root.addView(hierarchy);
        root.addView(spacer(8));

        String appearanceLabel = "deep-dark".equals(appearance) ? "Deep Dark" : "dark".equals(appearance) ? "Dark" : "Light";
        addInfoPair("Appearance: " + appearanceLabel, "Target floor: " + targetDp + " dp");
        root.addView(infoCard(touchAssistance ? "Touch Assistance: 56 dp minimum target" : "Touch Assistance: Off"));
        root.addView(infoCard(reducedTransparency
                ? "Reduced Transparency: Solid system panels"
                : "Optical Glaze: Native translucency is decorative; semantics do not depend on blur"));
        root.addView(infoCard("System Glaze budget: one dominant panel"));
        root.addView(spacer(11));

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

        panelState = label("Dominant panel: None", 13, false);
        panelState.setContentDescription("Dominant panel state");
        panelState.setPadding(dp(3), dp(7), 0, dp(2));
        root.addView(panelState);
        root.addView(spacer(8));

        searchPanel = panelContainer("Universal Search");
        searchPanel.setVisibility(View.GONE);
        searchInput = new EditText(this);
        searchInput.setSingleLine(true);
        searchInput.setHint("Search everything");
        searchInput.setHintTextColor(textSecondary);
        searchInput.setTextColor(textPrimary);
        searchInput.setContentDescription("Search everything");
        searchInput.setMinHeight(dp(targetDp));
        searchInput.setPadding(dp(16), dp(9), dp(16), dp(9));
        searchInput.setBackground(panelShape(reducedTransparency ? raised : glassSoft, 24));
        searchPanel.addView(searchInput, matchWrap());
        searchPanel.addView(sectionLabel("BEST MATCH"));
        Button projectResult = actionButton("Project Brief");
        projectResult.setContentDescription("Project Brief, File, exact match");
        projectResult.setBackground(panelShape(reducedTransparency ? raised : accentSoft, 22));
        searchPanel.addView(projectResult, matchTarget());
        searchPanel.addView(sectionLabel("ACTIONS"));
        Button appearanceResult = actionButton("Appearance settings");
        searchPanel.addView(appearanceResult, matchTarget());
        deleteButton = actionButton("Delete local cache");
        deleteButton.setContentDescription("Delete local cache, destructive action");
        searchPanel.addView(deleteButton, matchTarget());
        TextView generated = infoCard("Generated answer · Source: Project Brief");
        generated.setContentDescription("Generated answer. Source Project Brief.");
        generated.setBackground(panelShape(reducedTransparency ? raised : Color.argb(54, 119, 92, 246), 22));
        LinearLayout.LayoutParams generatedParams = matchWrap();
        generatedParams.topMargin = dp(8);
        generated.setLayoutParams(generatedParams);
        searchPanel.addView(generated);
        actionState = label("Search action: None", 13, false);
        actionState.setContentDescription("Search action state");
        searchPanel.addView(actionState);
        root.addView(searchPanel, matchWrap());

        controlPanel = panelContainer("Control Center");
        controlPanel.setVisibility(View.GONE);
        wifiButton = actionButton("Wi-Fi: On");
        wifiButton.setContentDescription("Wi-Fi toggle, on");
        wifiButton.setBackground(panelShape(reducedTransparency ? raised : accentSoft, 22));
        Button bluetoothButton = actionButton("Bluetooth: On");
        bluetoothButton.setContentDescription("Bluetooth toggle, on");
        bluetoothButton.setBackground(panelShape(reducedTransparency ? raised : accentSoft, 22));
        addButtonPair(controlPanel, wifiButton, bluetoothButton);
        controlPanel.addView(sectionLabel("Brightness"));
        SeekBar brightness = range("Brightness", 64);
        controlPanel.addView(brightness, matchTarget());
        controlPanel.addView(sectionLabel("Volume"));
        SeekBar volume = range("Volume", 64);
        controlPanel.addView(volume, matchTarget());
        Button focusButton = actionButton("Focus: Off");
        focusButton.setContentDescription("Focus toggle, off");
        Button mediaButton = actionButton("Media: Playing");
        mediaButton.setContentDescription("Media playback toggle, playing");
        mediaButton.setBackground(panelShape(reducedTransparency ? raised : accentSoft, 22));
        addButtonPair(controlPanel, focusButton, mediaButton);
        root.addView(controlPanel, matchWrap());

        TextView boundary = infoCard("Reference boundary: emulator-native interaction evidence only; no live GoreeCloud state, physical-device certification, TalkBack acceptance, signing, distribution, or human Visual Excellence claim.");
        boundary.setBackground(panelShape(reducedTransparency ? raised : glassSoft, 22));
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

    private void addInfoPair(String first, String second) {
        if (largeText) {
            root.addView(infoCard(first));
            root.addView(infoCard(second));
            return;
        }
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        TextView a = infoCard(first);
        TextView b = infoCard(second);
        row.addView(a, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        LinearLayout.LayoutParams bParams = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        bParams.setMarginStart(dp(8));
        row.addView(b, bParams);
        root.addView(row, matchWrap());
    }

    private void addButtonPair(LinearLayout parent, Button first, Button second) {
        if (largeText) {
            parent.addView(first, matchTarget());
            parent.addView(second, matchTarget());
            return;
        }
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        LinearLayout.LayoutParams firstParams = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        firstParams.topMargin = dp(7);
        row.addView(first, firstParams);
        LinearLayout.LayoutParams secondParams = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        secondParams.topMargin = dp(7);
        secondParams.setMarginStart(dp(8));
        row.addView(second, secondParams);
        parent.addView(row, matchWrap());
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
        button.setBackground(panelShape(reducedTransparency ? raised : (on ? glassSoft : accentSoft), 22));
    }

    private void toggleMedia(Button button) {
        boolean playing = button.getText().toString().contains("Playing");
        button.setText("Media: " + (playing ? "Paused" : "Playing"));
        button.setContentDescription("Media playback toggle, " + (playing ? "paused" : "playing"));
        button.setBackground(panelShape(reducedTransparency ? raised : (playing ? glassSoft : accentSoft), 22));
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
        panel.setPadding(dp(16), dp(16), dp(16), dp(16));
        panel.setBackground(panelShape(reducedTransparency ? surface : glassStrong, 30));
        panel.setElevation(reducedTransparency ? 0f : dp(10));
        panel.setContentDescription(title + " system panel");
        panel.addView(label(title, 22, true));
        panel.addView(label("Only one dominant system panel may be open.", 13, false));
        LinearLayout.LayoutParams params = matchWrap();
        params.topMargin = dp(6);
        panel.setLayoutParams(params);
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
        TextView view = label(text, 11, true);
        view.setTextColor(textSecondary);
        LinearLayout.LayoutParams params = matchWrap();
        params.topMargin = dp(12);
        view.setLayoutParams(params);
        return view;
    }

    private TextView infoCard(String text) {
        TextView view = label(text, 14, false);
        view.setTextColor(textPrimary);
        view.setPadding(dp(14), dp(11), dp(14), dp(11));
        view.setBackground(panelShape(reducedTransparency ? raised : glassSoft, 22));
        view.setElevation(reducedTransparency ? 0f : dp(1));
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
        button.setPadding(dp(16), dp(9), dp(16), dp(9));
        button.setBackground(panelShape(reducedTransparency ? raised : glassSoft, 22));
        button.setStateListAnimator(null);
        button.setElevation(reducedTransparency ? 0f : dp(1));
        return button;
    }

    private GradientDrawable ambientBackground() {
        GradientDrawable drawable = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{ambientA, canvas, ambientB});
        drawable.setGradientType(GradientDrawable.LINEAR_GRADIENT);
        return drawable;
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
