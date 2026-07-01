import SwiftUI

struct OnboardingView: View {
    @Binding var isComplete: Bool
    @State private var page = 0

    private let pages: [(title: String, body: String)] = [
        ("A private sanctuary", "What you write here is yours. No feed, no scores, no audience."),
        ("A tree that grows with you", "Your sakura tree reflects inner growth — not rewards. Seasons change; winter is rest, not failure."),
        ("A gentle guide", "After you save, you may explore one or two questions — or simply close. You are always in control."),
    ]

    var body: some View {
        VStack(spacing: DesignTokens.Spacing.lg) {
            Spacer()
            Text(pages[page].title)
                .font(DesignTokens.FontToken.editorial(26))
                .multilineTextAlignment(.center)
            Text(pages[page].body)
                .font(DesignTokens.FontToken.journal(16))
                .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.6))
                .multilineTextAlignment(.center)
                .padding(.horizontal, DesignTokens.Spacing.lg)
            Spacer()
            HStack(spacing: 8) {
                ForEach(0..<pages.count, id: \.self) { i in
                    Circle()
                        .fill(i == page ? DesignTokens.ColorToken.ink : DesignTokens.ColorToken.ink.opacity(0.2))
                        .frame(width: 6, height: 6)
                }
            }
            Button(page < pages.count - 1 ? "Continue" : "Enter") {
                if page < pages.count - 1 { page += 1 }
                else {
                    UserDefaults.standard.set(true, forKey: "seedjournal.onboarding.done")
                    isComplete = true
                }
            }
            .font(DesignTokens.FontToken.editorial(17))
            .foregroundStyle(DesignTokens.ColorToken.paper)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 14)
            .background(DesignTokens.ColorToken.ink)
            .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.pill))
            .padding(.horizontal, DesignTokens.Spacing.lg)
            Button("Skip") {
                UserDefaults.standard.set(true, forKey: "seedjournal.onboarding.done")
                isComplete = true
            }
            .font(DesignTokens.FontToken.journal(14))
            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.4))
            .padding(.bottom, DesignTokens.Spacing.md)
        }
        .background(DesignTokens.ColorToken.paper)
    }
}