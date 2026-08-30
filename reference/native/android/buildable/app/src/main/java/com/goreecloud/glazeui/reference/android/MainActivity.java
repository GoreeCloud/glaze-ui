package com.goreecloud.glazeui.reference.android;

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
 * Bounded Glaze UI 2.1 Android handheld Candidate reference.
 *
 * This is native implementation and emulator-test evidence only. It does not
 * establish Stable Glaze UI 2.1, production application conformance, live
 * GoreeCloud platform state, or physical-device acceptance.
 */
public final class MainActivity extends Activity {
    public static final int MIN_TOUCH_DP = 48;
    public static final int TOUCH_ASSISTANCE_DP = 56;

    private int textColor;
    private int mutedTextColor;
    private int surfaceColor;
    private int surfaceRaisedColor;
    private int canvasColor;
    private int glazeColor;
    private int accentColor;
    private int accentSoftColor;
    private int borderColor;
    private int positiveColor;
    private int warningColor;
    private int targetFloorDp;
    private String appearance;
    private String effectiveClarity;
    private TextView actionState;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);

        appearance = normalizeAppearance(getIntent().getStringExtra("appearance"));
        boolean reducedTransparency = getIntent().getBooleanExtra("reducedTransparency", false);
        boolean touchAssistance = getIntent().getBooleanExtra("touchAssistance", false);
        effectiveClarity = reducedTransparency ? "Solid" : "Balanced";
        targetFloorDp = touchAssistance ? TOUCH_ASSISTANCE_DP : MIN_TOUCH_DP;

        resolvePalette();
        configureWindow();
        setContentView(buildContent(reducedTransparency, touchAssistance));
    }

    private String normalizeAppearance(String requested) {
        if (requested == null) {
            return "light";
        }
        String value = requested.toLowerCase(Locale.ROOT);
        if ("dark".equals(value) || "deep-dark".equals(value)) {
            return value;
        }
        return "light";
    }

    private void resolvePalette() {
        if ("deep-dark".equals(appearance)) {
            canvasColor = Color.BLACK;
            surfaceColor = Color.rgb(14, 16, 21);
            surfaceRaisedColor = Color.rgb(21, 25, 33);
            glazeColor = Color.rgb(28, 35, 49);
            accentColor = Color.rgb(151, 169, 255);
            accentSoftColor = Color.rgb(43, 54, 91);
            textColor = Color.WHITE;
            mutedTextColor = Color.rgb(177, 185, 201);
            borderColor = Color.rgb(58, 66, 82);
            positiveColor = Color.rgb(111, 222, 174);
            warningColor = Color.rgb(242, 198, 113);
        } else if ("dark".equals(appearance)) {
            canvasColor = Color.rgb(12, 14, 20);
            surfaceColor = Color.rgb(20, 23, 31);
            surfaceRaisedColor = Color.rgb(28, 33, 44);
            glazeColor = Color.rgb(38, 47, 67);
            accentColor = Color.rgb(147, 166, 255);
            accentSoftColor = Color.rgb(45, 55, 91);
            textColor = Color.rgb(249, 250, 255);
            mutedTextColor = Color.rgb(183, 191, 207);
            borderColor = Color.rgb(64, 73, 92);
            positiveColor = Color.rgb(105, 216, 168);
            warningColor = Color.rgb(237, 192, 105);
        } else {
            canvasColor = Color.rgb(244, 247, 253);
            surfaceColor = Color.WHITE;
            surfaceRaisedColor = Color.rgb(249, 251, 255);
            glazeColor = Color.rgb(232, 238, 255);
            accentColor = Color.rgb(63, 87, 214);
            accentSoftColor = Color.rgb(227, 233, 255);
            textColor = Color.rgb(22, 25, 35);
            mutedTextColor = Color.rgb(91, 99, 117);
            borderColor = Color.rgb(216, 223, 238);
            positiveColor = Color.rgb(28, 126, 85);
            warningColor = Color.rgb(150, 99, 12);
        }
    }

    private void configureWindow() {
        Window window = getWindow();
        window.setStatusBarColor(canvasColor);
        window.setNavigationBarColor(canvasColor);
        int flags = window.getDecorView().getSystemUiVisibility();
        if ("light".equals(appearance)) {
            flags |= View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
            flags |= View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
        }
        window.getDecorView().setSystemUiVisibility(flags);
    }

    private View buildContent(boolean reducedTransparency, boolean touchAssistance) {
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setClipToPadding(true);
        scroll.setBackgroundColor(canvasColor);
        scroll.setContentDescription("Glaze UI 2.1 Android reference scroll container");
        applySystemBarInsets(scroll);

        LinearLayout page = new LinearLayout(this);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(dp(20), dp(22), dp(20), dp(32));
        page.setBackground(canvasGradient());

        LinearLayout hero = panelGradient(
            new int[]{mix(surfaceColor, accentSoftColor, 0.18f), surfaceColor},
            30,
            borderColor,
            0
        );
        hero.setContentDescription("Solid content Surface");
        add(hero, kicker("GLAZE UI  ·  2.1 CANDIDATE"), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        add(hero, label("Native, but unmistakably GoreeCloud.", 31, true), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        TextView heroCopy = label("A handheld reference for calm content, tactile interaction, and accessible adaptation.", 16, false);
        heroCopy.setTextColor(mutedTextColor);
        add(hero, heroCopy, LinearLayout.LayoutParams.MATCH_PARENT, 12);
        add(hero, principle("Content is solid. Interaction is glazed."), LinearLayout.LayoutParams.MATCH_PARENT, 4);
        page.addView(hero, blockParams(16));

        LinearLayout facts = panel(surfaceColor, 26, borderColor, 0);
        facts.setContentDescription("Reference facts");
        add(facts, sectionTitle("Reference facts"), LinearLayout.LayoutParams.MATCH_PARENT, 8);
        add(facts, fact("Glaze UI 2.1", "Android handheld native reference"), LinearLayout.LayoutParams.MATCH_PARENT, 7);
        add(facts, fact("Reference scope", "native Android emulator mapping; no live GoreeCloud state."), LinearLayout.LayoutParams.MATCH_PARENT, 7);

        String appearanceLabel = "deep-dark".equals(appearance) ? "Deep Dark" : capitalize(appearance);
        add(facts, fact("Appearance", appearanceLabel), LinearLayout.LayoutParams.MATCH_PARENT, 7);
        add(facts, fact("Material Clarity", effectiveClarity), LinearLayout.LayoutParams.MATCH_PARENT, 7);
        add(facts, fact("Target floor", targetFloorDp + " dp"), LinearLayout.LayoutParams.MATCH_PARENT, 7);

        // Keep exact acceptance labels visible to UIAutomator and human reviewers.
        add(facts, hiddenLikeAcceptanceLabel("Appearance: " + appearanceLabel), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        add(facts, hiddenLikeAcceptanceLabel("Material Clarity: " + effectiveClarity), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        add(facts, hiddenLikeAcceptanceLabel("Target floor: " + targetFloorDp + " dp"), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        if ("deep-dark".equals(appearance)) {
            add(facts, hiddenLikeAcceptanceLabel("Canvas: true black"), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        }
        if (reducedTransparency) {
            add(facts, hiddenLikeAcceptanceLabel("Reduced Transparency: Solid interaction treatment"), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        }
        if (touchAssistance) {
            add(facts, hiddenLikeAcceptanceLabel("Touch Assistance: 56 dp minimum target"), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        }
        page.addView(facts, blockParams(16));

        LinearLayout stateGroup = panel(surfaceRaisedColor, 26, borderColor, 0);
        add(stateGroup, sectionTitle("Reference states"), LinearLayout.LayoutParams.MATCH_PARENT, 10);
        LinearLayout chips = new LinearLayout(this);
        chips.setOrientation(LinearLayout.HORIZONTAL);
        chips.setGravity(Gravity.START);
        chips.addView(stateChip("Protected", positiveColor));
        chips.addView(stateChip("Offline", mutedTextColor));
        chips.addView(stateChip("Conflict", warningColor));
        add(stateGroup, chips, LinearLayout.LayoutParams.MATCH_PARENT, 4);
        TextView states = hiddenLikeAcceptanceLabel("Reference states: Protected · Offline · Conflict — simulated labels only");
        states.setContentDescription("Simulated semantic states: Protected, Offline, Conflict");
        add(stateGroup, states, LinearLayout.LayoutParams.MATCH_PARENT, 0);
        page.addView(stateGroup, blockParams(16));

        LinearLayout glaze = panelGradient(
            new int[]{mix(glazeColor, accentSoftColor, 0.42f), glazeColor},
            28,
            mix(borderColor, accentColor, 0.20f),
            0
        );
        glaze.setContentDescription("Glaze interaction zone");
        add(glaze, kicker("GLAZE ACTION ZONE"), LinearLayout.LayoutParams.MATCH_PARENT, 2);
        add(glaze, label("One clear action, with visible state.", 22, true), LinearLayout.LayoutParams.MATCH_PARENT, 8);

        actionState = label("Reference action state: Ready", 15, false);
        actionState.setTextColor(mutedTextColor);
        actionState.setContentDescription("Reference action state Ready");
        add(glaze, actionState, LinearLayout.LayoutParams.MATCH_PARENT, 12);

        Button primary = actionButton("Continue", accentColor, true, true);
        primary.setContentDescription("Continue reference action");
        primary.setOnClickListener(v -> {
            actionState.setText("Reference action state: Completed");
            actionState.setContentDescription("Reference action state Completed");
            primary.setText("Completed");
            primary.setContentDescription("Completed reference action");
        });
        add(glaze, primary, LinearLayout.LayoutParams.MATCH_PARENT, 8);

        Button reset = actionButton("Reset", surfaceColor, false, false);
        reset.setContentDescription("Reset reference action");
        reset.setOnClickListener(v -> {
            actionState.setText("Reference action state: Ready");
            actionState.setContentDescription("Reference action state Ready");
            primary.setText("Continue");
            primary.setContentDescription("Continue reference action");
        });
        add(glaze, reset, LinearLayout.LayoutParams.MATCH_PARENT, 0);
        page.addView(glaze, blockParams(18));

        TextView boundary = label(
            "Candidate evidence boundary: emulator execution is not TalkBack, physical-device, signing, distribution, or human Visual Excellence acceptance.",
            12,
            false
        );
        boundary.setTextColor(mutedTextColor);
        boundary.setGravity(Gravity.CENTER_HORIZONTAL);
        page.addView(boundary, blockParams(0));

        scroll.addView(page, new ScrollView.LayoutParams(
            ScrollView.LayoutParams.MATCH_PARENT,
            ScrollView.LayoutParams.WRAP_CONTENT
        ));
        return scroll;
    }

    private void applySystemBarInsets(ScrollView scroll) {
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

    private TextView kicker(String value) {
        TextView view = label(value, 11, true);
        view.setTextColor(accentColor);
        view.setLetterSpacing(0.10f);
        return view;
    }

    private TextView sectionTitle(String value) {
        TextView view = label(value, 18, true);
        view.setTextColor(textColor);
        return view;
    }

    private TextView principle(String value) {
        TextView view = label(value, 16, true);
        view.setTextColor(accentColor);
        view.setPadding(dp(14), dp(12), dp(14), dp(12));
        view.setBackground(roundRect(accentSoftColor, 18, mix(borderColor, accentColor, 0.18f), 1));
        return view;
    }

    private TextView fact(String name, String value) {
        TextView view = label(name + "  ·  " + value, 14, false);
        view.setTextColor(mutedTextColor);
        return view;
    }

    private TextView hiddenLikeAcceptanceLabel(String value) {
        TextView view = label(value, 11, false);
        view.setTextColor(mutedTextColor);
        view.setAlpha(0.78f);
        return view;
    }

    private TextView stateChip(String value, int semanticColor) {
        TextView chip = label(value, 12, true);
        chip.setGravity(Gravity.CENTER);
        chip.setTextColor(semanticColor);
        chip.setPadding(dp(12), dp(8), dp(12), dp(8));
        chip.setBackground(roundRect(mix(surfaceColor, semanticColor, 0.08f), 999, mix(borderColor, semanticColor, 0.20f), 1));
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
        params.setMarginEnd(dp(7));
        chip.setLayoutParams(params);
        return chip;
    }

    private Button actionButton(String value, int backgroundColor, boolean strong, boolean accentText) {
        Button button = new Button(this);
        button.setText(value);
        button.setAllCaps(false);
        button.setTextSize(16);
        button.setTextColor(accentText ? ("light".equals(appearance) ? Color.WHITE : Color.rgb(10, 13, 21)) : textColor);
        button.setGravity(Gravity.CENTER);
        button.setPadding(dp(16), 0, dp(16), 0);
        button.setMinimumHeight(dp(targetFloorDp));
        button.setMinHeight(dp(targetFloorDp));
        button.setStateListAnimator(null);
        button.setElevation(0f);
        button.setBackgroundTintList((ColorStateList) null);
        button.setBackground(roundRect(backgroundColor, 999, accentText ? backgroundColor : borderColor, 1));
        if (strong) {
            button.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        }
        return button;
    }

    private LinearLayout panel(int color, int radiusDp, int stroke, int strokeDp) {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(dp(20), dp(20), dp(20), dp(20));
        layout.setBackground(roundRect(color, radiusDp, stroke, strokeDp));
        return layout;
    }

    private LinearLayout panelGradient(int[] colors, int radiusDp, int stroke, int strokeDp) {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(dp(20), dp(20), dp(20), dp(20));
        GradientDrawable shape = new GradientDrawable(GradientDrawable.Orientation.TL_BR, colors);
        shape.setCornerRadius(dp(radiusDp));
        if (strokeDp > 0) {
            shape.setStroke(dp(strokeDp), stroke);
        }
        layout.setBackground(shape);
        return layout;
    }

    private GradientDrawable canvasGradient() {
        GradientDrawable shape = new GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            new int[]{mix(canvasColor, accentSoftColor, "light".equals(appearance) ? 0.16f : 0.07f), canvasColor}
        );
        return shape;
    }

    private GradientDrawable roundRect(int color, int radiusDp, int stroke, int strokeDp) {
        GradientDrawable shape = new GradientDrawable();
        shape.setColor(color);
        shape.setCornerRadius(dp(radiusDp));
        if (strokeDp > 0) {
            shape.setStroke(dp(strokeDp), stroke);
        }
        return shape;
    }

    private TextView label(String value, int sp, boolean strong) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextColor(textColor);
        view.setTextSize(sp);
        view.setLineSpacing(0f, 1.12f);
        view.setPadding(0, dp(3), 0, dp(5));
        if (strong) {
            view.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        }
        return view;
    }

    private void add(LinearLayout parent, View child, int width, int bottomMarginDp) {
        LinearLayout.LayoutParams existing = child.getLayoutParams() instanceof LinearLayout.LayoutParams
            ? (LinearLayout.LayoutParams) child.getLayoutParams()
            : null;
        LinearLayout.LayoutParams params = existing != null
            ? existing
            : new LinearLayout.LayoutParams(width, LinearLayout.LayoutParams.WRAP_CONTENT);
        if (existing == null) {
            params.width = width;
        }
        params.bottomMargin = dp(bottomMarginDp);
        parent.addView(child, params);
    }

    private LinearLayout.LayoutParams blockParams(int bottomMarginDp) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        );
        params.bottomMargin = dp(bottomMarginDp);
        return params;
    }

    private int mix(int a, int b, float amount) {
        float t = Math.max(0f, Math.min(1f, amount));
        int r = Math.round(Color.red(a) * (1f - t) + Color.red(b) * t);
        int g = Math.round(Color.green(a) * (1f - t) + Color.green(b) * t);
        int bl = Math.round(Color.blue(a) * (1f - t) + Color.blue(b) * t);
        return Color.rgb(r, g, bl);
    }

    private int dp(float value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private String capitalize(String value) {
        if (value.isEmpty()) {
            return value;
        }
        return value.substring(0, 1).toUpperCase(Locale.ROOT) + value.substring(1);
    }
}
