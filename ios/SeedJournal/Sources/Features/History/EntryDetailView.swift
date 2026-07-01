import SwiftUI

struct EntryDetailView: View {
    let entryId: UUID
    let accessToken: String?

    @State private var entry: EntryResponse?
    @State private var error: String?

    var body: some View {
        Group {
            if let entry {
                ScrollView {
                    VStack(alignment: .leading, spacing: 12) {
                        Text(entry.createdAt.formatted(date: .long, time: .shortened))
                            .font(DesignTokens.FontToken.journal(13))
                            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.4))
                        if let title = entry.title, !title.isEmpty {
                            Text(title).font(DesignTokens.FontToken.editorial(22))
                        }
                        Text(entry.body)
                            .font(DesignTokens.FontToken.journal(17))
                            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.9))
                    }
                    .padding()
                }
            } else if let error {
                Text(error)
            } else {
                ProgressView()
            }
        }
        .background(DesignTokens.ColorToken.paper)
        .navigationTitle("Reflection")
        .navigationBarTitleDisplayMode(.inline)
        .task { await load() }
    }

    private func load() async {
        do {
            entry = try await APIClient(accessToken: accessToken).get("/entries/\(entryId.uuidString)")
        } catch {
            self.error = (error as? LocalizedError)?.errorDescription
        }
    }
}