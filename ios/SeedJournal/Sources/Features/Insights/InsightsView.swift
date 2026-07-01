import SwiftUI

struct PatternsResponse: Codable {
    let items: [PatternItem]
    let narrative: String
    struct PatternItem: Codable, Identifiable {
        var id: String { memoryType }
        let memoryType: String
        let count: Int
        enum CodingKeys: String, CodingKey {
            case memoryType = "memory_type"
            case count
        }
    }
}

struct FirstMentionResponse: Codable {
    let query: String
    let narrative: String
    let items: [FirstMentionItem]
    struct FirstMentionItem: Codable, Identifiable {
        let memoryId: UUID
        let title: String
        let summary: String
        let firstMentionedAt: Date
        let score: Double
        var id: UUID { memoryId }
        enum CodingKeys: String, CodingKey {
            case memoryId = "memory_id"
            case title, summary, score
            case firstMentionedAt = "first_mentioned_at"
        }
    }
}

struct InsightsView: View {
    @Environment(\.dismiss) private var dismiss
    let accessToken: String?
    @State private var patterns: PatternsResponse?
    @State private var query = ""
    @State private var firstMention: FirstMentionResponse?
    @State private var error: String?

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: DesignTokens.Spacing.md) {
                    if let patterns {
                        Text(patterns.narrative)
                            .font(DesignTokens.FontToken.journal(15))
                            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.65))
                        ForEach(patterns.items) { item in
                            HStack {
                                Text(item.memoryType.replacingOccurrences(of: "_", with: " "))
                                    .font(DesignTokens.FontToken.editorial(15))
                                Spacer()
                                Text("\(item.count)")
                                    .font(DesignTokens.FontToken.journal(14))
                                    .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.4))
                            }
                        }
                    }
                    Divider().padding(.vertical, 8)
                    Text("When did I first talk about…")
                        .font(DesignTokens.FontToken.editorial(17))
                    HStack {
                        TextField("A theme or word", text: $query)
                        Button("Search") { Task { await searchFirst() } }
                    }
                    if let fm = firstMention {
                        Text(fm.narrative)
                            .font(DesignTokens.FontToken.journal(14))
                            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.6))
                        ForEach(fm.items) { item in
                            VStack(alignment: .leading, spacing: 4) {
                                Text(item.title).font(DesignTokens.FontToken.editorial(15))
                                Text(item.firstMentionedAt.formatted(date: .long, time: .omitted))
                                    .font(DesignTokens.FontToken.journal(12))
                                    .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.4))
                            }
                        }
                    }
                    if let error { Text(error).foregroundStyle(.red.opacity(0.7)) }
                }
                .padding()
            }
            .background(DesignTokens.ColorToken.paper)
            .navigationTitle("Patterns")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) { Button("Done") { dismiss() } }
            }
            .task { await loadPatterns() }
        }
    }

    private func loadPatterns() async {
        do {
            patterns = try await APIClient(accessToken: accessToken).get("/insights/patterns")
        } catch {
            self.error = (error as? LocalizedError)?.errorDescription
        }
    }

    private func searchFirst() async {
        let q = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !q.isEmpty else { return }
        var comp = URLComponents(url: APIConfig.baseURL.appending(path: "insights/first-mention"), resolvingAgainstBaseURL: false)!
        comp.queryItems = [URLQueryItem(name: "q", value: q)]
        var req = URLRequest(url: comp.url!)
        if let accessToken { req.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization") }
        do {
            let (data, _) = try await URLSession.shared.data(for: req)
            firstMention = try JSONDecoder.api.decode(FirstMentionResponse.self, from: data)
        } catch {
            self.error = "Search failed."
        }
    }
}