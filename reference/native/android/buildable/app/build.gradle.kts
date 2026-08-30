plugins {
    id("com.android.application")
}

android {
    namespace = "com.goreecloud.glazeui.reference.android"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.goreecloud.glazeui.reference.android"
        minSdk = 28
        targetSdk = 36
        versionCode = 1
        versionName = "2.1.0-candidate.1-reference"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
