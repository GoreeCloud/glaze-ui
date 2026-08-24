import SwiftUI

/// Glaze UI wearable Development Candidate reference.
///
/// This is implementation evidence only. It is not a Stable Glaze UI contract,
/// production-ready application screen, or real-device acceptance record.
struct GlazeWearableReference: View {
    var status: String = "All systems healthy"
    var onOpenDetails: () -> Void = {}

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                Text("Glaze UI")
                    .font(.headline)

                Text(status)
                    .font(.body)
                    .accessibilityLabel("Status")
                    .accessibilityValue(status)

                Button("Open details", action: onOpenDetails)
                    .buttonStyle(.borderedProminent)
                    .accessibilityHint("Opens the focused detail task")
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
        }
    }
}

#Preview {
    GlazeWearableReference()
}

// ScrollView preserves the expected vertical watch interaction model and lets
// watchOS provide native Digital Crown scrolling behavior. Standard SwiftUI
// controls retain system accessibility, focus, text-scaling, and interaction
// semantics rather than recreating phone controls at watch size.
