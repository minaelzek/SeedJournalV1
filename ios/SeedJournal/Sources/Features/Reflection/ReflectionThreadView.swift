import SwiftUI

@MainActor
@Observable
final class ReflectionThreadViewModel {
    var turns: [ReflectionTurnDTO] = []
    var draft = ""
    var isLoading = false
    var errorMessage: String?
    var turnCount = 0
    var maxTurns = 6
    var limitReached = false

    let entryId: UUID
    private let client: APIClient

    init(entryId: UUID, accessToken: String?, initialAssistant: ReflectionTurnDTO?) {
        self.entryId = entryId
        client = APIClient(accessToken: accessToken)
        if let initialAssistant {
            turns = [initialAssistant]
            turnCount = 1
        }
    }

    var canSend: Bool {
        !draft.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
            && !isLoading
            && !limitReached
            && turnCount < maxTurns
    }

    func send() async {
        guard canSend else { return }
        isLoading = true
        errorMessage = nil
        let text = draft
        draft = ""
        defer { isLoading = false }
        do {
            let response: ReflectionMessageResponse = try await client.post(
                "/entries/\(entryId.uuidString)/reflection/message",
                body: ReflectionMessageRequest(message: text)
            )
            turns.append(response.userTurn)
            if let assistant = response.assistantTurn {
                turns.append(assistant)
            }
            turnCount = response.turnCount
            limitReached = response.limitReached
        } catch {
            errorMessage = (error as? LocalizedError)?.errorDescription ?? "Could not send."
            draft = text
        }
    }

    func complete() async -> Bool {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }
        do {
            let _: ReflectionCompleteResponse = try await client.post(
                "/entries/\(entryId.uuidString)/reflection/complete",
                body: EmptyBody()
            )
            return true
        } catch {
            errorMessage = (error as? LocalizedError)?.errorDescription ?? "Could not save."
            return false
        }
    }
}

private struct EmptyBody: Encodable {}

struct ReflectionThreadView: View {
    @Environment(\.dismiss) private var dismiss
    @Bindable var viewModel: ReflectionThreadViewModel
    var onFinished: (() -> Void)?

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: DesignTokens.Spacing.sm) {
                            ForEach(viewModel.turns) { turn in
                                ReflectionTurnRow(turn: turn)
                                    .id(turn.id)
                            }
                        }
                        .padding(DesignTokens.Spacing.md)
                    }
                    .onChange(of: viewModel.turns.count) { _, _ in
                        if let last = viewModel.turns.last {
                            withAnimation(.easeOut(duration: 0.25)) {
                                proxy.scrollTo(last.id, anchor: .bottom)
                            }
                        }
                    }
                }

                if let err = viewModel.errorMessage {
                    Text(err)
                        .font(DesignTokens.FontToken.journal(13))
                        .foregroundStyle(.red.opacity(0.75))
                        .padding(.horizontal, DesignTokens.Spacing.md)
                }

                HStack(spacing: DesignTokens.Spacing.xs) {
                    TextField("Continue reflecting...", text: $viewModel.draft, axis: .vertical)
                        .lineLimit(1 ... 4)
                        .font(DesignTokens.FontToken.journal(16))
                        .disabled(viewModel.limitReached || viewModel.isLoading)

                    Button("Send") {
                        Task { await viewModel.send() }
                    }
                    .disabled(!viewModel.canSend)
                }
                .padding(DesignTokens.Spacing.sm)
                .background(DesignTokens.ColorToken.paper)

                Button {
                    Task {
                        if await viewModel.complete() {
                            onFinished?()
                            dismiss()
                        }
                    }
                } label: {
                    Text("Save reflection")
                        .font(DesignTokens.FontToken.editorial(16))
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 14)
                }
                .buttonStyle(.borderedProminent)
                .tint(DesignTokens.ColorToken.ink)
                .padding(DesignTokens.Spacing.sm)
            }
            .background(DesignTokens.ColorToken.paper)
            .navigationTitle("Stay with this")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") {
                        Task {
                            _ = await viewModel.complete()
                            onFinished?()
                            dismiss()
                        }
                    }
                }
            }
        }
    }
}

struct ReflectionTurnRow: View {
    let turn: ReflectionTurnDTO

    var body: some View {
        HStack {
            if turn.isAssistant { Spacer(minLength: 24) }
            Text(turn.content)
                .font(DesignTokens.FontToken.journal(turn.isAssistant ? 16 : 17))
                .foregroundStyle(DesignTokens.ColorToken.ink.opacity(turn.isAssistant ? 0.75 : 0.95))
                .padding(DesignTokens.Spacing.sm)
                .background(
                    turn.isAssistant
                        ? DesignTokens.ColorToken.moss.opacity(0.08)
                        : Color.clear
                )
                .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.soft))
            if !turn.isAssistant { Spacer(minLength: 24) }
        }
    }
}