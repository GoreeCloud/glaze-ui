package com.goreecloud.glazeui.reference.wearable

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.wear.compose.foundation.lazy.TransformingLazyColumn
import androidx.wear.compose.material3.Button
import androidx.wear.compose.material3.MaterialTheme
import androidx.wear.compose.material3.Text
import androidx.wear.compose.material3.minimumInteractiveComponentSize

/**
 * Glaze UI wearable Development Candidate reference.
 *
 * This is implementation evidence only. It is not a Stable Glaze UI contract,
 * production-ready application screen, or real-device acceptance record.
 */
@Composable
fun GlazeWearableReference(
    status: String = "All systems healthy",
    onOpenDetails: () -> Unit = {},
) {
    MaterialTheme {
        TransformingLazyColumn(modifier = Modifier.fillMaxSize()) {
            item {
                Text("Glaze UI")
            }
            item {
                Text(status)
            }
            item {
                Button(
                    onClick = onOpenDetails,
                    modifier = Modifier.minimumInteractiveComponentSize(),
                ) {
                    Text("Open details")
                }
            }
        }
    }
}

// TransformingLazyColumn provides the expected vertical wearable flow and
// current Compose for Wear OS rotary behavior. The action retains the platform
// minimum interactive component sizing rather than shrinking a phone control.
