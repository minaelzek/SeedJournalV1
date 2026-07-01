import SwiftUI

struct SignInGateView: View {
    @Bindable var appState: AppState

    var body: some View {
        VStack(spacing: DesignTokens.Spacing.md) {
            Text("SeedJournal")
                .font(DesignTokens.FontToken.editorial(28))
                .foregroundStyle(DesignTokens.ColorToken.ink)

            Text("A private sanctuary for reflection.")
                .font(DesignTokens.FontToken.journal(15))
                .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.55))
                .multilineTextAlignment(.center)

            if let err = appState.sessionError {
                Text(err)
                    .font(DesignTokens.FontToken.journal(13))
                    .foregroundStyle(.red.opacity(0.75))
                    .multilineTextAlignment(.center)
            }

            Button {
                Task { await appState.signInWithApple() }
            } label: {
                HStack(spacing: 8) {
                    Image(systemName: "apple.logo")
                    Text("Sign in with Apple")
                }
                .font(DesignTokens.FontToken.editorial(17))
                .foregroundStyle(DesignTokens.ColorToken.paper)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 14)
                .background(Color.black)
                .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.pill))
            }
            .disabled(appState.isLoadingSession)
            .padding(.horizontal, DesignTokens.Spacing.lg)

            #if DEBUG
            Button {
                Task { await appState.devSignIn() }
            } label: {
                Text("Developer sign-in (local API)")
                    .font(DesignTokens.FontToken.journal(13))
                    .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.45))
            }
            .disabled(appState.isLoadingSession)
            #endif
        }
        .padding(DesignTokens.Spacing.lg)
    }
}