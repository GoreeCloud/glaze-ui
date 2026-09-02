plugins {
    id("com.android.application")
}

android {
    namespace = "com.goreecloud.glazeui.reference.android22"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.goreecloud.glazeui.reference.android22"
        minSdk = 28
        targetSdk = 36
        versionCode = 1
        versionName = "2.2.0-candidate.1-reference"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
