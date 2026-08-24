plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.goreecloud.glazeui.reference.wearable"
    compileSdk = 37

    defaultConfig {
        applicationId = "com.goreecloud.glazeui.reference.wearable"
        minSdk = 30
        targetSdk = 36
        versionCode = 1
        versionName = "0.0.0-development-candidate"
    }

    buildFeatures {
        compose = true
    }

    sourceSets["main"].kotlin.srcDir("../..")
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2026.08.00"))
    implementation("androidx.activity:activity-compose:1.13.0")
    implementation("androidx.wear.compose:compose-foundation:1.5.0")
    implementation("androidx.wear.compose:compose-material3:1.5.0")
    implementation("androidx.compose.ui:ui-tooling-preview")
    debugImplementation("androidx.compose.ui:ui-tooling")
}
