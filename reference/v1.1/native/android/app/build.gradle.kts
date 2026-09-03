plugins {
    id("com.android.application")
}

android {
    namespace = "com.goreecloud.glazeui.reference.v11"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.goreecloud.glazeui.reference.v11"
        minSdk = 28
        targetSdk = 36
        versionCode = 1
        versionName = "1.1.0-rc.1-reference"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
