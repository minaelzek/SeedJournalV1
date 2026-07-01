import SwiftUI

@MainActor
@Observable
final class PastReflectionsViewModel {
    var items: [EntryListItem] = []
    var isLoading = false
    var errorMessage: String?

    private let client: APIClient

    init(accessToken: String?) {
        client = APIClient(accessToken: accessToken)
    }

    func load() async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }
        do {
            let response: EntryListResponse = try await client.get("/entries")
            items = response.items
        } catch {
            errorMessage = (error as? LocalizedError)?.errorDescription
        }
    }
}

struct PastReflectionsView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var viewModel: PastReflectionsViewModel
    let accessToken: String?

    init(accessToken: String?) {
        self.accessToken = accessToken
        _viewModel = State(initialValue: PastReflectionsViewModel(accessToken: accessToken))
    }

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.isLoading && viewModel.items.isEmpty {
                    ProgressView()
                } else if let err = viewModel.errorMessage {
                    Text(err)
                        .font(DesignTokens.FontToken.journal(15))
                        .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.6))
                } else if viewModel.items.isEmpty {
                    Text("Your reflections will gather here.")
                        .font(DesignTokens.FontToken.editorial(17))
                        .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.45))
                } else {
                    List(viewModel.items) { item in
                        NavigationLink {
                            EntryDetailView(entryId: item.id, accessToken: accessToken)
                        } label: {
                            VStack(alignment: .leading, spacing: 6) {
                                Text(item.title ?? item.createdAt.formatted(date: .abbreviated, time: .omitted))
                                    .font(DesignTokens.FontToken.editorial(16))
                                Text(item.bodyPreview)
                                    .font(DesignTokens.FontToken.journal(14))
                                    .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.55))
                                    .lineLimit(2)
                            }
                        }
                        .listRowBackground(DesignTokens.ColorToken.paper)
                    }
                    .listStyle(.plain)
                }
            }
            .background(DesignTokens.ColorToken.paper)
            .navigationTitle("Past reflections")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
            .task { await viewModel.load() }
        }
    }
}