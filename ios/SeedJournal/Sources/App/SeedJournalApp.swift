import SwiftUI

@main
struct SeedJournalApp: App {
    @State private var appState = AppState()
    @AppStorage("seedjournal.onboarding.done") private var onboardingDone = false

    var body: some Scene {
        WindowGroup {
            RootView(onboardingDone: $onboardingDone)
                .environment(appState)
                .task { await appState.bootstrap() }
                .preferredColorScheme(nil)
        }
    }
}

struct RootView: View {
    @Environment(AppState.self) private var appState
    @Binding var onboardingDone: Bool

    var body: some View {
        Group {
            if !onboardingDone && appState.currentUser != nil {
                OnboardingView(isComplete: $onboardingDone)
            } else if appState.currentUser != nil {
                TreeHomeView()
            } else if appState.isLoadingSession {
                ProgressView().tint(DesignTokens.ColorToken.ink)
            } else {
                ZStack {
                    TreeHomeView().blur(radius: 12).allowsHitTesting(false)
                    SignInGateView(appState: appState)
                }
            }
        }
    }
}