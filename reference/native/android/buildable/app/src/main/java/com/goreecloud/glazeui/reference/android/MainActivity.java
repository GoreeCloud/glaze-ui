package com.goreecloud.glazeui.reference.android;

import android.app.Activity;
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
    private int canvasColor;
    private int glazeColor;
    private int borderColor;
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
            surfaceColor = Color.rgb(17, 17, 17);
            glazeColor = Color.rgb(29, 36, 48);
            textColor = Color.WHITE;
            mutedTextColor = Color.rgb(196, 201, 212);
            borderColor = Color.rgb(76, 84, 101);
        } else if ("dark".equals(appearance)) {
            canvasColor = Color.rgb(16, 17, 22);
            surfaceColor = Color.rgb(25, 27, 33);
            glazeColor = Color.rgb(40, 50, 70);
            textColor = Color.WHITE;
            mutedTextColor = Color.rgb(202, 207, 219);
            borderColor = Color.rgb(79, 88, 106);
        } else {
            canvasColor = Color.rgb(246, 247, 251);
            surfaceColor = Color.WHITE;
            glazeColor = Color.rgb(226, 234, 252);
            textColor = Color.rgb(23, 25, 31);
            mutedTextColor = Color.rgb(78, 84, 99);
            borderColor = Color.rgb(198, 207, 225);
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
        scroll.setBackgroundColor(canvasColor);
        scroll.setContentDescription("Glaze UI 2.1 Android reference scroll container");

        LinearLayout page = new LinearLayout(this);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(dp(24), dp(24), dp(24), dp(32));
        page.setGravity(Gravity.CENTER_HORIZONTAL);
        page.setBackgroundColor(canvasColor);

        LinearLayout surface = panel(surfaceColor, 24, borderColor);
        surface.setContentDescription("Solid content Surface");
        add(surface, label("Glaze UI 2.1", 30, true), LinearLayout.LayoutParams.MATCH_PARENT);
        add(surface, label("Android handheld native reference", 20, true), LinearLayout.LayoutParams.MATCH_PARENT);
        add(surface, label("Reference scope: native Android emulator mapping; no live GoreeCloud state.", 16, false), LinearLayout.LayoutParams.MATCH_PARENT);
        add(surface, label("Content is solid. Interaction is glazed.", 18, true), LinearLayout.LayoutParams.MATCH_PARENT);

        String appearanceLabel = "deep-dark".equals(appearance) ? "Deep Dark" : capitalize(appearance);
        add(surface, label("Appearance: " + appearanceLabel, 16, false), LinearLayout.LayoutParams.MATCH_PARENT);
        add(surface, label("Material Clarity: " + effectiveClarity, 16, false), LinearLayout.LayoutParams.MATCH_PARENT);
        add(surface, label("Target floor: " + targetFloorDp + " dp", 16, false), LinearLayout.LayoutParams.MATCH_PARENT);
        if ("deep-dark".equals(appearance)) {
            add(surface, label("Canvas: true black", 16, false), LinearLayout.LayoutParams.MATCH_PARENT);
        }
        if (reducedTransparency) {
            add(surface, label("Reduced Transparency: Solid interaction treatment", 16, false), LinearLayout.LayoutParams.MATCH_PARENT);
        }
        if (touchAssistance) {
            add(surface, label("Touch Assistance: 56 dp minimum target", 16, false), LinearLayout.LayoutParams.MATCH_PARENT);
        }

        TextView states = label("Reference states: Protected · Offline · Conflict — simulated labels only", 16, false);
        states.setContentDescription("Simulated semantic states: Protected, Offline, Conflict");
        add(surface, states, LinearLayout.LayoutParams.MATCH_PARENT);
        page.addView(surface, blockParams());

        LinearLayout glaze = panel(glazeColor, 24, borderColor);
        glaze.setContentDescription("Glaze interaction zone");
        add(glaze, label("Glaze action zone", 18, true), LinearLayout.LayoutParams.MATCH_PARENT);

        actionState = label("Reference action state: Ready", 16, false);
        actionState.setContentDescription("Reference action state Ready");
        add(glaze, actionState, LinearLayout.LayoutParams.MATCH_PARENT);

        Button primary = new Button(this);
        primary.setText("Continue");
        primary.setAllCaps(false);
        primary.setTextSize(16);
        primary.setTextColor(textColor);
        primary.setMinimumHeight(dp(targetFloorDp));
        primary.setMinHeight(dp(targetFloorDp));
        primary.setContentDescription("Continue reference action");
        primary.setBackground(roundRect(glazeColor, 999, borderColor));
        primary.setOnClickListener(v -> {
            actionState.setText("Reference action state: Completed");
            actionState.setContentDescription("Reference action state Completed");
            primary.setText("Completed");
            primary.setContentDescription("Completed reference action");
        });
        add(glaze, primary, LinearLayout.LayoutParams.MATCH_PARENT);

        Button reset = new Button(this);
        reset.setText("Reset");
        reset.setAllCaps(false);
        reset.setTextSize(16);
        reset.setTextColor(textColor);
        reset.setMinimumHeight(dp(targetFloorDp));
        reset.setMinHeight(dp(targetFloorDp));
        reset.setContentDescription("Reset reference action");
        reset.setBackground(roundRect(surfaceColor, 999, borderColor));
        reset.setOnClickListener(v -> {
            actionState.setText("Reference action state: Ready");
            actionState.setContentDescription("Reference action state Ready");
            primary.setText("Continue");
            primary.setContentDescription("Continue reference action");
        });
        add(glaze, reset, LinearLayout.LayoutParams.MATCH_PARENT);
        page.addView(glaze, blockParams());

        TextView boundary = label(
            "Candidate evidence boundary: emulator execution is not TalkBack, physical-device, signing, distribution, or human Visual Excellence acceptance.",
            14,
            false
        );
        boundary.setTextColor(mutedTextColor);
        page.addView(boundary, blockParams());

        scroll.addView(page, new ScrollView.LayoutParams(
            ScrollView.LayoutParams.MATCH_PARENT,
            ScrollView.LayoutParams.WRAP_CONTENT
        ));
        return scroll;
    }

    private LinearLayout panel(int color, int radiusDp, int stroke) {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(dp(20), dp(20), dp(20), dp(20));
        layout.setBackground(roundRect(color, radiusDp, stroke));
        return layout;
    }

    private GradientDrawable roundRect(int color, int radiusDp, int stroke) {
        GradientDrawable shape = new GradientDrawable();
        shape.setColor(color);
        shape.setCornerRadius(dp(radiusDp));
        shape.setStroke(dp(1), stroke);
        return shape;
    }

    private TextView label(String value, int sp, boolean strong) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextColor(textColor);
        view.setTextSize(sp);
        view.setLineSpacing(0f, 1.1f);
        view.setPadding(0, dp(4), 0, dp(8));
        if (strong) {
            view.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        }
        return view;
    }

    private void add(LinearLayout parent, View child, int width) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(width, LinearLayout.LayoutParams.WRAP_CONTENT);
        params.bottomMargin = dp(8);
        parent.addView(child, params);
    }

    private LinearLayout.LayoutParams blockParams() {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        );
        params.bottomMargin = dp(16);
        return params;
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
