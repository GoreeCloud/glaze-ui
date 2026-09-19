buildscript {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
    dependencies {
        // Security convergence for transitive Android build-tool dependencies.
        classpath("org.apache.commons:commons-lang3:3.18.0")
        classpath("org.bitbucket.b_c:jose4j:0.9.6")
        classpath("org.bouncycastle:bcpkix-jdk18on:1.85")
        classpath("org.bouncycastle:bcprov-jdk18on:1.85")
        classpath("org.bouncycastle:bcutil-jdk18on:1.85")
        classpath("org.jdom:jdom2:2.0.6.1")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:2.4.20")
    }
    configurations.classpath {
        resolutionStrategy.force(
            "org.apache.commons:commons-lang3:3.18.0",
            "org.bitbucket.b_c:jose4j:0.9.6",
            "org.bouncycastle:bcpkix-jdk18on:1.85",
            "org.bouncycastle:bcprov-jdk18on:1.85",
            "org.bouncycastle:bcutil-jdk18on:1.85",
            "org.jdom:jdom2:2.0.6.1",
            "org.jetbrains.kotlin:kotlin-gradle-plugin:2.4.20",
        )
    }
}

plugins {
    id("com.android.application") version "9.4.0" apply false
}
