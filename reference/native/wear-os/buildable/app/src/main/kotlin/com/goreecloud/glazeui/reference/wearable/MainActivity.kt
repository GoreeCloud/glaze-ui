package com.goreecloud.glazeui.reference.wearable

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent

/**
 * Build harness entry point for the Glaze UI wearable Development Candidate.
 *
 * Successful compilation proves stable-SDK source compatibility only. It is not
 * emulator, accessibility-runtime, battery, interruption, or real-device acceptance.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            GlazeWearableReference()
        }
    }
}
