plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.goreecloud.glazeui.reference.wearable"
    compileSdk = 36

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
    implementation("androidx.activity:activity-compose:1.13.0")
    implementation("androidx.wear.compose:compose-foundation:1.5.0")
    implementation("androidx.wear.compose:compose-material3:1.5.0")
}
