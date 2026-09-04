package com.goreecloud.glazeui.reference.v12;

import android.app.Activity;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.util.Locale;

/**
 * Bounded framework-native Android handheld reference for the GLAZE UI V1.2
 * Frosted Neutral Candidate. Neutral translucent surfaces carry the hierarchy;
 * color is reserved for active/focus/state accents rather than the substrate.
 */
public final class MainActivity extends Activity {
    public static final int MIN_TOUCH_DP = 48;
    public static final int TOUCH_ASSISTANCE_DP = 56;

    private String appearance;
    private boolean reducedTransparency;
    private int targetFloorDp;

    private int canvas;
    private int canvasWarm;
    private int base;
    private int raised;
    private int overlay;
    private int panel;
    private int critical;
    private int text;
    private int secondary;
    private int line;
    private int accent;
    private int success;
    private int warning;

    private TextView interactionState;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        appearance = normalizeAppearance(getIntent().getStringExtra("appearance"));
        reducedTransparency = getIntent().getBooleanExtra("reducedTransparency", false);
        boolean touchAssistance = getIntent().getBooleanExtra("touchAssistance", false);
        targetFloorDp = touchAssistance ? TOUCH_ASSISTANCE_DP : MIN_TOUCH_DP;

        resolvePalette();
        configureWindow();
        setContentView(buildContent(touchAssistance));
    }

    private String normalizeAppearance(String requested) {
        if (requested == null) return "light";
        String value = requested.toLowerCase(Locale.ROOT);
        if ("dark".equals(value) || "deep-dark".equals(value)) return value;
        return "light";
    }

    private void resolvePalette() {
        accent = Color.rgb(47, 111, 237);   // purposeful GoreeCloud blue accent
        success = Color.rgb(38, 146, 92);
        warning = Color.rgb(184, 122, 42);

        if ("deep-dark".equals(appearance)) {
            canvas = Color.rgb(7, 7, 8);
            canvasWarm = Color.rgb(14, 13, 13);
            base = Color.argb(176, 24, 24, 26);
            raised = Color.argb(208, 34, 34, 37);
            overlay = Color.argb(224, 40, 40, 43);
            panel = Color.argb(238, 46, 46, 49);
            critical = Color.rgb(25, 25, 27);
            text = Color.rgb(247, 247, 248);
            secondary = Color.rgb(184, 184, 190);
            line = Color.argb(52, 255, 255, 255);
        } else if ("dark".equals(appearance)) {
            canvas = Color.rgb(18, 18, 20);
            canvasWarm = Color.rgb(24, 23, 22);
            base = Color.argb(176, 31, 31, 34);
            raised = Color.argb(208, 41, 41, 44);
            overlay = Color.argb(224, 48, 48, 51);
            panel = Color.argb(238, 54, 54, 57);
            critical = Color.rgb(30, 30, 32);
            text = Color.rgb(247, 247, 248);
            secondary = Color.rgb(188, 188, 194);
            line = Color.argb(48, 255, 255, 255);
        } else {
            canvas = Color.rgb(238, 241, 245);
            canvasWarm = Color.rgb(245, 241, 237);
            base = Color.argb(154, 255, 255, 255);
            raised = Color.argb(190, 255, 255, 255);
            overlay = Color.argb(218, 252, 252, 252);
            panel = Color.argb(232, 250, 250, 250);
            critical = Color.rgb(255, 255, 255);
            text = Color.rgb(25, 25, 28);
            secondary = Color.rgb(92, 92, 99);
            line = Color.argb(28, 45, 45, 50);
        }

        if (reducedTransparency) {
            base = opaque(base);
            raised = opaque(raised);
            overlay = opaque(overlay);
            panel = opaque(panel);
        }
    }

    private void configureWindow() {
        Window window = getWindow();
        window.setStatusBarColor(canvas);
        window.setNavigationBarColor(canvas);
        int flags = window.getDecorView().getSystemUiVisibility();
        if ("light".equals(appearance)) {
            flags |= View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
            flags |= View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
        }
        window.getDecorView().setSystemUiVisibility(flags);
    }

    private View buildContent(boolean touchAssistance) {
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(canvas);
        scroll.setContentDescription("GLAZE UI V1.2 Frosted Neutral Android candidate scroll container");
        applySystemInsets(scroll);

        LinearLayout page = new LinearLayout(this);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(dp(18), dp(20), dp(18), dp(34));
        page.setBackground(reducedTransparency ? solid(canvas, 0, canvas, 0) : canvasGradient());

        LinearLayout header = materialPanel(overlay, 30, line, 1);
        add(header, kicker("GOREECLOUD · GLAZE UI V1.2 CANDIDATE"), 4);
        add(header, title("Frosted Neutral, not tinted glass.", 29), 8);
        add(header, body("Milky white and neutral translucent surfaces carry the hierarchy. Blue, teal, green, and amber remain accents for state, focus, progress, and identity.", 15), 0);
        page.addView(header, block(14));

        LinearLayout facts = materialPanel(base, 24, line, 1);
        add(facts, section("Candidate evidence"), 8);
        add(facts, fact("Lifecycle", "V1.2 Candidate"), 4);
        add(facts, fact("Appearance", appearanceLabel()), 4);
        add(facts, fact("Material", reducedTransparency ? "Neutral opaque fallback" : "Neutral translucent glass"), 4);
        add(facts, fact("Target floor", targetFloorDp + " dp"), 4);
        add(facts, acceptance("Substrate: neutral"), 2);
        add(facts, acceptance("Color role: accent only"), 2);
        if (reducedTransparency) add(facts, acceptance("Reduced Transparency: enabled"), 2);
        if (touchAssistance) add(facts, acceptance("Touch Assistance: 56 dp minimum target"), 2);
        page.addView(facts, block(14));

        LinearLayout search = materialPanel(overlay, 24, line, 1);
        add(search, kicker("UNIVERSAL SEARCH"), 4);
        TextView searchField = body("Search GoreeCloud", 16);
        searchField.setTextColor(text);
        searchField.setMinHeight(dp(targetFloorDp));
        searchField.setGravity(Gravity.CENTER_VERTICAL);
        searchField.setPadding(dp(16), 0, dp(16), 0);
        searchField.setBackground(solid(raised, 999, line, 1));
        searchField.setContentDescription("Universal Search entry neutral glass");
        add(search, searchField, 8);
        add(search, body("Results use a deeper neutral layer without stacking another blur authority.", 13), 0);
        page.addView(search, block(14));

        LinearLayout controlCenter = materialPanel(panel, 30, line, 1);
        add(controlCenter, section("Quick Settings"), 2);
        add(controlCenter, body("Neutral panel · accent only on active state", 13), 10);
        add(controlCenter, quickSettingsRow(
            settingButton("Wi‑Fi", "Connected", true),
            settingButton("Bluetooth", "On", true)
        ), 8);
        add(controlCenter, quickSettingsRow(
            settingButton("Night Light", "Off", false),
            settingButton("Performance", "Balanced", true)
        ), 8);
        add(controlCenter, quickSettingsRow(
            settingButton("Airplane Mode", "Off", false),
            settingButton("Focus", "Available", false)
        ), 0);
        page.addView(controlCenter, block(14));

        LinearLayout criticalPanel = materialPanel(critical, 24, line, 1);
        add(criticalPanel, kicker("CRITICAL SYSTEM"), 4);
        add(criticalPanel, title("High-opacity clarity stays separate.", 20), 6);
        add(criticalPanel, body("Security, privacy, identity, recovery, and destructive confirmations do not depend on backdrop translucency for legibility.", 14), 0);
        criticalPanel.setContentDescription("Critical System high opacity non backdrop dependent surface");
        page.addView(criticalPanel, block(14));

        LinearLayout actions = materialPanel(raised, 26, line, 1);
        add(actions, section("Interaction"), 4);
        interactionState = body("Action: Ready", 14);
        interactionState.setContentDescription("Reference action state Ready");
        add(actions, interactionState, 10);

        Button primary = actionButton("Primary action", accent, true);
        primary.setContentDescription("Primary action");
        primary.setOnClickListener(v -> {
            interactionState.setText("Action: Complete");
            interactionState.setContentDescription("Reference action state Complete");
            primary.setText("Complete");
            primary.setContentDescription("Complete primary action");
        });
        add(actions, primary, 8);

        Button secondaryAction = actionButton("Secondary action", raised, false);
        secondaryAction.setContentDescription("Secondary action");
        secondaryAction.setOnClickListener(v -> {
            interactionState.setText("Action: Secondary");
            interactionState.setContentDescription("Reference action state Secondary");
        });
        add(actions, secondaryAction, 0);
        page.addView(actions, block(14));

        TextView boundary = body("Evidence boundary: emulator rendering validates framework-native candidate structure, state, fallback behavior, and target floors. It is not OEM-wide blur fidelity, physical-device, TalkBack, signing, distribution, downstream-app, production, or Stable-promotion acceptance.", 12);
        boundary.setGravity(Gravity.CENTER_HORIZONTAL);
        page.addView(boundary, block(0));

        scroll.addView(page, new ScrollView.LayoutParams(
            ScrollView.LayoutParams.MATCH_PARENT,
            ScrollView.LayoutParams.WRAP_CONTENT
        ));
        return scroll;
    }

    private LinearLayout quickSettingsRow(Button first, Button second) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.addView(first, weighted(1f, 4));
        row.addView(second, weighted(1f, 0));
        return row;
    }

    private Button settingButton(String name, String state, boolean active) {
        Button button = new Button(this);
        button.setAllCaps(false);
        button.setText(name + "\n" + state);
        button.setTextSize(14);
        button.setGravity(Gravity.START | Gravity.CENTER_VERTICAL);
        button.setPadding(dp(14), dp(8), dp(14), dp(8));
        button.setMinimumHeight(dp(Math.max(76, targetFloorDp)));
        button.setMinHeight(dp(Math.max(76, targetFloorDp)));
        button.setStateListAnimator(null);
        button.setElevation(0f);
        button.setBackgroundTintList((ColorStateList) null);
        button.setTextColor(text);
        button.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        button.setTag(active ? "active" : "inactive");
        applySettingMaterial(button, active);
        button.setContentDescription(name + ": " + state + (active ? "; active accent state" : "; inactive neutral state"));
        button.setOnClickListener(v -> {
            boolean next = !"active".equals(v.getTag());
            v.setTag(next ? "active" : "inactive");
            applySettingMaterial(button, next);
            button.setContentDescription(name + ": " + state + (next ? "; active accent state" : "; inactive neutral state"));
        });
        return button;
    }

    private void applySettingMaterial(Button button, boolean active) {
        int background = active ? mix(raised, accent, "light".equals(appearance) ? 0.16f : 0.24f) : raised;
        int stroke = active ? mix(line, accent, 0.55f) : line;
        button.setBackground(solid(background, 20, stroke, 1));
    }

    private void applySystemInsets(ScrollView scroll) {
        scroll.setOnApplyWindowInsetsListener((view, insets) -> {
            view.setPadding(
                insets.getSystemWindowInsetLeft(),
                insets.getSystemWindowInsetTop(),
                insets.getSystemWindowInsetRight(),
                insets.getSystemWindowInsetBottom()
            );
            return insets;
        });
    }

    private String appearanceLabel() {
        if ("deep-dark".equals(appearance)) return "Deep Dark";
        if ("dark".equals(appearance)) return "Dark";
        return "Light";
    }

    private TextView kicker(String value) {
        TextView view = label(value, 11, true);
        view.setTextColor(accent);
        view.setLetterSpacing(0.09f);
        return view;
    }

    private TextView section(String value) {
        return label(value, 18, true);
    }

    private TextView title(String value, int sp) {
        TextView view = label(value, sp, true);
        view.setLineSpacing(0f, 1.02f);
        return view;
    }

    private TextView body(String value, int sp) {
        TextView view = label(value, sp, false);
        view.setTextColor(secondary);
        view.setLineSpacing(0f, 1.20f);
        return view;
    }

    private TextView fact(String name, String value) {
        TextView view = body(name + " · " + value, 14);
        view.setContentDescription(name + ": " + value);
        return view;
    }

    private TextView acceptance(String value) {
        TextView view = body("✓ " + value, 12);
        view.setTextColor(success);
        view.setContentDescription(value);
        return view;
    }

    private TextView label(String value, int sp, boolean strong) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextColor(text);
        view.setTextSize(sp);
        view.setPadding(0, dp(2), 0, dp(4));
        if (strong) view.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        return view;
    }

    private Button actionButton(String value, int background, boolean primary) {
        Button button = new Button(this);
        button.setText(value);
        button.setAllCaps(false);
        button.setTextSize(16);
        button.setGravity(Gravity.CENTER);
        button.setPadding(dp(16), 0, dp(16), 0);
        button.setMinimumHeight(dp(targetFloorDp));
        button.setMinHeight(dp(targetFloorDp));
        button.setStateListAnimator(null);
        button.setElevation(0f);
        button.setBackgroundTintList((ColorStateList) null);
        button.setTextColor(primary ? Color.WHITE : text);
        button.setBackground(solid(background, 999, primary ? mix(background, Color.WHITE, 0.30f) : line, 1));
        if (primary) button.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        return button;
    }

    private LinearLayout materialPanel(int color, int radiusDp, int stroke, int strokeDp) {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(dp(18), dp(18), dp(18), dp(18));
        layout.setBackground(solid(color, radiusDp, stroke, strokeDp));
        layout.setElevation(dp(2));
        return layout;
    }

    private GradientDrawable canvasGradient() {
        int coolNeutral = mix(canvas, Color.rgb(230, 234, 241), "light".equals(appearance) ? 0.28f : 0.06f);
        int warmNeutral = mix(canvasWarm, Color.rgb(242, 232, 224), "light".equals(appearance) ? 0.18f : 0.04f);
        return new GradientDrawable(GradientDrawable.Orientation.TL_BR, new int[]{coolNeutral, canvas, warmNeutral});
    }

    private GradientDrawable solid(int color, int radiusDp, int stroke, int strokeDp) {
        GradientDrawable shape = new GradientDrawable();
        shape.setColor(color);
        shape.setCornerRadius(dp(radiusDp));
        if (strokeDp > 0) shape.setStroke(dp(strokeDp), stroke);
        return shape;
    }

    private LinearLayout.LayoutParams block(int marginBottomDp) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        );
        params.setMargins(0, 0, 0, dp(marginBottomDp));
        return params;
    }

    private LinearLayout.LayoutParams weighted(float weight, int marginEndDp) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, weight);
        params.setMargins(0, 0, dp(marginEndDp), 0);
        return params;
    }

    private void add(LinearLayout parent, View child, int marginBottomDp) {
        parent.addView(child, block(marginBottomDp));
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private static int opaque(int color) {
        return Color.rgb(Color.red(color), Color.green(color), Color.blue(color));
    }

    private static int mix(int first, int second, float amountSecond) {
        float t = Math.max(0f, Math.min(1f, amountSecond));
        int a = Math.round(Color.alpha(first) * (1f - t) + Color.alpha(second) * t);
        int r = Math.round(Color.red(first) * (1f - t) + Color.red(second) * t);
        int g = Math.round(Color.green(first) * (1f - t) + Color.green(second) * t);
        int b = Math.round(Color.blue(first) * (1f - t) + Color.blue(second) * t);
        return Color.argb(a, r, g, b);
    }
}
