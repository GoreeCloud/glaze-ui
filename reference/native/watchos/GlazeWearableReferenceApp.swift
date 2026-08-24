import SwiftUI

/// Minimal watchOS application entry point for Glaze UI Development Candidate
/// SDK-compatibility evidence. This is not a Stable application contract.
@main
struct GlazeWearableReferenceApp: App {
    var body: some Scene {
        WindowGroup {
            GlazeWearableReference()
        }
    }
}
