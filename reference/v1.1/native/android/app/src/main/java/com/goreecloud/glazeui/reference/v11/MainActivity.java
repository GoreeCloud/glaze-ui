package com.goreecloud.glazeui.reference.v11;

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
 * Bounded GLAZE UI V1.1 Android handheld release-candidate reference.
 * Framework-native implementation and emulator evidence only.
 */
public final class MainActivity extends Activity {
    public static final int MIN_TOUCH_DP = 48;
    public static final int TOUCH_ASSISTANCE_DP = 56;

    private int canvas;
    private int base;
    private int raised;
    private int text;
    private int secondary;
    private int line;
    private int teal;
    private int mineralTeal;
    private int aqua;
    private int amber;
    private int targetFloorDp;
    private String appearance;
    private boolean reducedTransparency;
    private TextView actionState;

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
        teal = Color.rgb(15, 107, 111);       // Deep Teal #0F6B6F
        mineralTeal = Color.rgb(28, 138, 141); // Mineral Teal #1C8A8D
        aqua = Color.rgb(143, 214, 210);       // Soft Aqua #8FD6D2
        amber = Color.rgb(217, 163, 95);       // Soft Amber #D9A35F

        if ("deep-dark".equals(appearance)) {
            canvas = Color.rgb(5, 7, 10);
            base = Color.rgb(13, 16, 21);
            raised = Color.rgb(23, 28, 35);
            text = Color.rgb(245, 247, 250);
            secondary = Color.rgb(171, 180, 194);
            line = Color.rgb(64, 72, 84);
        } else if ("dark".equals(appearance)) {
            canvas = Color.rgb(11, 13, 17);
            base = Color.rgb(18, 21, 27);
            raised = Color.rgb(27, 32, 40);
            text = Color.rgb(245, 247, 250);
            secondary = Color.rgb(176, 183, 195);
            line = Color.rgb(62, 70, 83);
        } else {
            canvas = Color.rgb(245, 247, 250);
            base = Color.WHITE;
            raised = Color.WHITE;
            text = Color.rgb(21, 26, 35);
            secondary = Color.rgb(93, 102, 117);
            line = Color.rgb(211, 216, 224);
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
        scroll.setContentDescription("GLAZE UI V1.1 Android native reference scroll container");
        applySystemInsets(scroll);

        LinearLayout page = new LinearLayout(this);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(dp(20), dp(22), dp(20), dp(34));
        page.setBackground(reducedTransparency ? solid(canvas, 0, canvas, 0) : canvasGradient());

        LinearLayout header = panel(mix(base, teal, "light".equals(appearance) ? 0.025f : 0.05f), 24, line, 1);
        add(header, kicker("GOREECLOUD · GLAZE UI V1.1"), 2);
        add(header, title("Native calm, exact structure.", 30), 8);
        TextView intro = body("A framework-native handheld reference for the human-approved Deep Teal + Soft Amber optical system.", 16);
        add(header, intro, 4);
        page.addView(header, block(16));

        LinearLayout facts = panel(raised, 24, line, 1);
        add(facts, section("Release-candidate evidence"), 8);
        add(facts, fact("Lifecycle", "Release Candidate"), 5);
        add(facts, fact("Reference", "Android handheld · framework native"), 5);
        add(facts, fact("Appearance", appearanceLabel()), 5);
        add(facts, fact("Target floor", targetFloorDp + " dp"), 5);
        add(facts, fact("Atmosphere", reducedTransparency ? "suppressed by Reduced Transparency" : "bounded Deep Teal + Soft Amber"), 5);
        add(facts, acceptance("Appearance: " + appearanceLabel()), 2);
        add(facts, acceptance("Target floor: " + targetFloorDp + " dp"), 2);
        if (reducedTransparency) {
            add(facts, acceptance("Reduced Transparency: atmosphere suppressed"), 2);
        }
        if (touchAssistance) {
            add(facts, acceptance("Touch Assistance: 56 dp minimum target"), 2);
        }
        page.addView(facts, block(16));

        LinearLayout atmosphere = panel(
            reducedTransparency ? base : mix(base, teal, "light".equals(appearance) ? 0.035f : 0.07f),
            28,
            mix(line, aqua, 0.18f),
            1
        );
        add(atmosphere, kicker("ATMOSPHERE"), 2);
        add(atmosphere, title("Teal first. Warmth stays sparse.", 22), 8);
        TextView atmosphericCopy = body(
            "Readable structure remains neutral. Teal supplies environmental depth; amber remains a localized counter-light and never carries protected semantic meaning.",
            15
        );
        add(atmosphere, atmosphericCopy, 4);
        page.addView(atmosphere, block(16));

        LinearLayout semantics = panel(base, 24, line, 1);
        add(semantics, section("Semantic boundary"), 8);
        TextView semanticCopy = body(
            "Reference labels are descriptive only. Security, privacy, identity, recovery, and coordination truth remains producer-authoritative outside this presentation harness.",
            14
        );
        add(semantics, semanticCopy, 6);
        add(semantics, fact("Protected state", "not synthesized by atmosphere"), 4);
        add(semantics, fact("Color-only meaning", "not permitted"), 4);
        page.addView(semantics, block(16));

        LinearLayout actions = panelGradient(
            reducedTransparency ? new int[]{raised, raised} : new int[]{mix(raised, teal, 0.10f), mix(raised, amber, 0.035f)},
            28,
            mix(line, mineralTeal, 0.24f),
            1
        );
        add(actions, kicker("INTERACTION"), 2);
        add(actions, title("Minimum targets survive density.", 22), 6);
        actionState = body("Action: Ready", 14);
        actionState.setContentDescription("Reference action state Ready");
        add(actions, actionState, 10);

        Button primary = actionButton("Primary action", mineralTeal, true);
        primary.setContentDescription("Primary action");
        primary.setOnClickListener(v -> {
            actionState.setText("Action: Complete");
            actionState.setContentDescription("Reference action state Complete");
            primary.setText("Complete");
            primary.setContentDescription("Complete primary action");
        });
        add(actions, primary, 8);

        Button secondaryAction = actionButton("Secondary action", raised, false);
        secondaryAction.setContentDescription("Secondary action");
        secondaryAction.setOnClickListener(v -> {
            actionState.setText("Action: Secondary");
            actionState.setContentDescription("Reference action state Secondary");
        });
        add(actions, secondaryAction, 0);
        page.addView(actions, block(16));

        TextView boundary = body(
            "Evidence boundary: emulator execution is not OEM-wide, physical-device, TalkBack, signing, distribution, downstream-application, or production-deployment acceptance.",
            12
        );
        boundary.setGravity(Gravity.CENTER_HORIZONTAL);
        page.addView(boundary, block(0));

        scroll.addView(page, new ScrollView.LayoutParams(
            ScrollView.LayoutParams.MATCH_PARENT,
            ScrollView.LayoutParams.WRAP_CONTENT
        ));
        return scroll;
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
        view.setTextColor(mineralTeal);
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
        view.setLineSpacing(0f, 1.22f);
        return view;
    }

    private TextView fact(String name, String value) {
        TextView view = body(name + " · " + value, 14);
        view.setContentDescription(name + ": " + value);
        return view;
    }

    private TextView acceptance(String value) {
        TextView view = body(value, 11);
        view.setAlpha(0.82f);
        return view;
    }

    private TextView label(String value, int sp, boolean strong) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextColor(text);
        view.setTextSize(sp);
        view.setPadding(0, dp(2), 0, dp(4));
        if (strong) {
            view.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        }
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
        button.setBackground(solid(background, 999, primary ? mix(background, aqua, 0.25f) : line, 1));
        if (primary) button.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        return button;
    }

    private LinearLayout panel(int color, int radiusDp, int stroke, int strokeDp) {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(dp(20), dp(20), dp(20), dp(20));
        layout.setBackground(solid(color, radiusDp, stroke, strokeDp));
        return layout;
    }

    private LinearLayout panelGradient(int[] colors, int radiusDp, int stroke, int strokeDp) {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(dp(20), dp(20), dp(20), dp(20));
        GradientDrawable shape = new GradientDrawable(GradientDrawable.Orientation.TL_BR, colors);
        shape.setCornerRadius(dp(radiusDp));
        if (strokeDp > 0) shape.setStroke(dp(strokeDp), stroke);
        layout.setBackground(shape);
        return layout;
    }

    private GradientDrawable canvasGradient() {
        int tealInfluence = mix(canvas, teal, "light".equals(appearance) ? 0.035f : 0.075f);
        int amberInfluence = mix(canvas, amber, "light".equals(appearance) ? 0.015f : 0.03f);
        return new GradientDrawable(GradientDrawable.Orientation.TL_BR, new int[]{tealInfluence, canvas, amberInfluence});
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

    private void add(LinearLayout parent, View child, int marginBottomDp) {
        parent.addView(child, block(marginBottomDp));
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
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
