import SwiftUI

struct MemoryItemDTO: Codable, Identifiable {
    let id: UUID
    let type: String
    let title: String
    let summary: String
    let confidence: Double
    let dismissed: Bool
    let sourceEntryId: UUID
    let firstMentionedAt: Date
    let createdAt: Date
    let score: Double?

    enum CodingKeys: String, CodingKey {
        case id, type, title, summary, confidence, dismissed, score
        case sourceEntryId = "source_entry_id"
        case firstMentionedAt = "first_mentioned_at"
        case createdAt = "created_at"
    }
}

struct MemoryListResponse: Codable {
    let items: [MemoryItemDTO]
}

@MainActor
@Observable
final class MemorySearchViewModel {
    var query = ""
    var results: [MemoryItemDTO] = []
    var isSearching = false
    var errorMessage: String?

    private let client: APIClient

    init(accessToken: String?) {
        client = APIClient(accessToken: accessToken)
    }

    func search() async {
        let q = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !q.isEmpty else { return }
        isSearching = true
        errorMessage = nil
        defer { isSearching = false }
        struct Body: Encodable {
            let query: String
            let limit: Int
        }
        do {
            let response: MemoryListResponse = try await client.post(
                "/memories/search",
                body: Body(query: q, limit: 12)
            )
            results = response.items
        } catch {
            errorMessage = (error as? LocalizedError)?.errorDescription
        }
    }
}

struct MemorySearchView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var viewModel: MemorySearchViewModel

    init(accessToken: String?) {
        _viewModel = State(initialValue: MemorySearchViewModel(accessToken: accessToken))
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: DesignTokens.Spacing.sm) {
                HStack {
                    TextField("What have you said about…", text: $viewModel.query)
                        .font(DesignTokens.FontToken.journal(16))
                        .onSubmit { Task { await viewModel.search() } }
                    Button("Search") {
                        Task { await viewModel.search() }
                    }
                    .disabled(viewModel.isSearching)
                }
                .padding(DesignTokens.Spacing.sm)

                if let err = viewModel.errorMessage {
                    Text(err)
                        .font(DesignTokens.FontToken.journal(13))
                        .foregroundStyle(.red.opacity(0.75))
                }

                List(viewModel.results) { item in
                    VStack(alignment: .leading, spacing: 6) {
                        Text(item.title)
                            .font(DesignTokens.FontToken.editorial(16))
                        Text(item.summary)
                            .font(DesignTokens.FontToken.journal(14))
                            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.6))
                        Text(item.firstMentionedAt.formatted(date: .abbreviated, time: .omitted))
                            .font(DesignTokens.FontToken.journal(11))
                            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.35))
                    }
                    .listRowBackground(DesignTokens.ColorToken.paper)
                }
                .listStyle(.plain)
            }
            .background(DesignTokens.ColorToken.paper)
            .navigationTitle("Ask your journal")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}