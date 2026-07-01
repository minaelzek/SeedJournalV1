import SwiftUI

@MainActor
@Observable
final class JournalComposeViewModel {
    var title = ""
    var bodyText = ""
    var isSaving = false
    var errorMessage: String?
    var savedEntry: EntryResponse?
    var showContinueChoice = false
    var reflectionStart: ReflectionStartResponse?

    private let client: APIClient
    let aiDepthEnabled: Bool

    init(accessToken: String?, aiDepthEnabled: Bool = true) {
        client = APIClient(accessToken: accessToken)
        self.aiDepthEnabled = aiDepthEnabled
    }

    var canSave: Bool {
        !bodyText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && !isSaving
    }

    func save() async {
        guard canSave else { return }
        isSaving = true
        errorMessage = nil
        defer { isSaving = false }
        let payload = EntryCreate(
            title: title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? nil : title,
            body: bodyText
        )
        do {
            savedEntry = try await client.post("/entries", body: payload)
            showContinueChoice = true
        } catch {
            errorMessage = (error as? LocalizedError)?.errorDescription ?? "Could not save."
        }
    }

    func completeWithoutReflection() async {
        guard let entry = savedEntry else { return }
        isSaving = true
        defer { isSaving = false }
        do {
            let _: ReflectionCompleteResponse = try await client.post(
                "/entries/\(entry.id.uuidString)/reflection/complete",
                body: EmptyEncodable()
            )
        } catch {
            errorMessage = (error as? LocalizedError)?.errorDescription
        }
    }

    func startReflection() async {
        guard let entry = savedEntry else { return }
        isSaving = true
        errorMessage = nil
        defer { isSaving = false }
        do {
            reflectionStart = try await client.post(
                "/entries/\(entry.id.uuidString)/reflection/start",
                body: EmptyEncodable()
            )
        } catch {
            errorMessage = (error as? LocalizedError)?.errorDescription ?? "Could not start reflection."
        }
    }
}

private struct EmptyEncodable: Encodable {}

struct JournalComposeView: View {
    @Environment(\.dismiss) private var dismiss
    @Bindable var viewModel: JournalComposeViewModel
    var accessToken: String?
    var onFinished: (() -> Void)?

    @State private var showReflection = false

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: DesignTokens.Spacing.sm) {
                if viewModel.savedEntry == nil {
                    editor
                } else {
                    savedConfirmation
                }

                if let error = viewModel.errorMessage {
                    Text(error)
                        .font(DesignTokens.FontToken.journal(14))
                        .foregroundStyle(.red.opacity(0.8))
                }

                Spacer()
            }
            .padding(DesignTokens.Spacing.md)
            .background(DesignTokens.ColorToken.paper)
            .navigationTitle("Reflect")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") {
                        Task {
                            if viewModel.savedEntry != nil {
                                await viewModel.completeWithoutReflection()
                            }
                            dismiss()
                        }
                    }
                }
                if viewModel.savedEntry == nil {
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Save") {
                            Task { await viewModel.save() }
                        }
                        .disabled(!viewModel.canSave)
                    }
                }
            }
            .sheet(isPresented: $showReflection) {
                if let entry = viewModel.savedEntry {
                    ReflectionThreadView(
                        viewModel: ReflectionThreadViewModel(
                            entryId: entry.id,
                            accessToken: accessToken,
                            initialAssistant: viewModel.reflectionStart?.assistantMessage
                        ),
                        onFinished: {
                            onFinished?()
                            dismiss()
                        }
                    )
                }
            }
        }
    }

    @ViewBuilder
    private var editor: some View {
        TextField("Title (optional)", text: $viewModel.title)
            .font(DesignTokens.FontToken.journal(17))
            .foregroundStyle(DesignTokens.ColorToken.ink)

        ZStack(alignment: .topLeading) {
            if viewModel.bodyText.isEmpty {
                Text("Write freely. This space is only yours.")
                    .font(DesignTokens.FontToken.journal(17))
                    .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.35))
                    .padding(.top, 8)
                    .padding(.leading, 4)
            }
            TextEditor(text: $viewModel.bodyText)
                .font(DesignTokens.FontToken.journal(17))
                .foregroundStyle(DesignTokens.ColorToken.ink)
                .scrollContentBackground(.hidden)
                .frame(minHeight: 220)
        }
    }

    @ViewBuilder
    private var savedConfirmation: some View {
        Text("Your words are saved.")
            .font(DesignTokens.FontToken.editorial(22))
            .foregroundStyle(DesignTokens.ColorToken.ink)

        Text("Would you like to stay with this a little longer?")
            .font(DesignTokens.FontToken.journal(16))
            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.6))
            .padding(.top, 4)

        if viewModel.aiDepthEnabled {
            Button {
                Task {
                    await viewModel.startReflection()
                    if viewModel.reflectionStart != nil {
                        showReflection = true
                    }
                }
            } label: {
                Text("Continue reflecting")
                    .font(DesignTokens.FontToken.editorial(17))
                    .foregroundStyle(DesignTokens.ColorToken.paper)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 14)
                    .background(DesignTokens.ColorToken.ink)
                    .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.pill))
            }
            .padding(.top, DesignTokens.Spacing.md)
            .disabled(viewModel.isSaving)
        }

        Button {
            Task {
                await viewModel.completeWithoutReflection()
                onFinished?()
                dismiss()
            }
        } label: {
            Text("Save & close")
                .font(DesignTokens.FontToken.journal(16))
                .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.55))
        }
        .padding(.top, DesignTokens.Spacing.sm)
        .disabled(viewModel.isSaving)
    }
}