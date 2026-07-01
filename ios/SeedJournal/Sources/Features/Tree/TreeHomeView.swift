import SwiftUI

struct TreeHomeView: View {
    @Environment(AppState.self) private var appState
    @Environment(\.colorScheme) private var colorScheme
    @State private var showJournal = false
    @State private var showHistory = false
    @State private var showSettings = false
    @State private var showSearch = false
    @State private var showInsights = false
    @State private var treeState = TreeVisualState(
        stage: "seed", season: "spring",
        rootsCount: 1, branchesCount: 0, leavesCount: 0, flowersCount: 0
    )

    var body: some View {
        ZStack {
            backgroundGradient.ignoresSafeArea()

            VStack(spacing: DesignTokens.Spacing.md) {
                HStack {
                    Button("Ask") { showSearch = true }
                        .font(DesignTokens.FontToken.journal(14))
                        .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.45))
                    Button("Patterns") { showInsights = true }
                        .font(DesignTokens.FontToken.journal(14))
                        .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.45))
                    Spacer()
                    Button { showSettings = true } label: {
                        Image(systemName: "gearshape")
                            .font(.body.weight(.light))
                            .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.6))
                    }
                    .accessibilityLabel("Settings")
                }
                .padding(.horizontal, DesignTokens.Spacing.sm)

                Spacer()

                SakuraTreeCanvas(state: treeState)
                    .frame(maxHeight: 360)
                    .accessibilityElement(children: .combine)
                    .accessibilityLabel(treeAccessibilityLabel)

                seasonCaption

                Text("A quiet place for your real self.")
                    .font(DesignTokens.FontToken.editorial(15))
                    .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.55))

                Spacer()

                Button { showJournal = true } label: {
                    Text("Reflect")
                        .font(DesignTokens.FontToken.editorial(17))
                        .foregroundStyle(DesignTokens.ColorToken.paper)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                        .background(DesignTokens.ColorToken.ink)
                        .clipShape(RoundedRectangle(cornerRadius: DesignTokens.Radius.pill))
                }
                .padding(.horizontal, DesignTokens.Spacing.lg)

                Button("Past reflections") { showHistory = true }
                    .font(DesignTokens.FontToken.journal(14))
                    .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.45))
                    .padding(.bottom, DesignTokens.Spacing.md)
            }
        }
        .sheet(isPresented: $showJournal) {
            JournalComposeView(
                viewModel: JournalComposeViewModel(
                    accessToken: appState.accessToken,
                    aiDepthEnabled: appState.currentUser?.aiDepthEnabled ?? true
                ),
                accessToken: appState.accessToken,
                onFinished: { Task { await loadTree() } }
            )
        }
        .sheet(isPresented: $showHistory) {
            PastReflectionsView(accessToken: appState.accessToken)
        }
        .sheet(isPresented: $showSettings) {
            SettingsView(appState: appState)
        }
        .sheet(isPresented: $showSearch) {
            MemorySearchView(accessToken: appState.accessToken)
        }
        .sheet(isPresented: $showInsights) {
            InsightsView(accessToken: appState.accessToken)
        }
        .task { await loadTree() }
    }

    private var backgroundGradient: LinearGradient {
        DesignTokens.backgroundGradient(colorScheme: colorScheme, season: treeState.season)
    }

    @ViewBuilder
    private var seasonCaption: some View {
        if treeState.season == "winter" {
            Text("A quiet season. Your tree rests with you.")
                .font(DesignTokens.FontToken.journal(13))
                .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.4))
        }
    }

    private var treeAccessibilityLabel: String {
        var label = "Your sakura tree is at the \(treeState.stage) stage, in \(treeState.season)."
        if treeState.leavesCount > 0 {
            label += " \(treeState.leavesCount) memories are leaves on your tree."
        }
        if treeState.flowersCount > 0 {
            label += " \(treeState.flowersCount) growth moments are in bloom."
        }
        return label
    }

    private func loadTree() async {
        guard appState.accessToken != nil else { return }
        struct TreeDTO: Decodable {
            let stage, season: String
            let rootsCount, branchesCount, leavesCount, flowersCount: Int
            enum CodingKeys: String, CodingKey {
                case stage, season
                case rootsCount = "roots_count"
                case branchesCount = "branches_count"
                case leavesCount = "leaves_count"
                case flowersCount = "flowers_count"
            }
        }
        do {
            let t: TreeDTO = try await APIClient(accessToken: appState.accessToken).get("/tree")
            treeState = TreeVisualState(
                stage: t.stage,
                season: t.season,
                rootsCount: t.rootsCount,
                branchesCount: t.branchesCount,
                leavesCount: t.leavesCount,
                flowersCount: t.flowersCount
            )
        } catch {
            treeState = TreeVisualState(
                stage: "seed", season: "spring",
                rootsCount: 1, branchesCount: 0, leavesCount: 0, flowersCount: 0
            )
        }
    }
}

struct SettingsView: View {
    @Environment(\.dismiss) private var dismiss
    @Bindable var appState: AppState
    @State private var showDeleteConfirm = false
    @State private var statusMessage: String?
    @State private var aiDepth: Bool = true

    var body: some View {
        NavigationStack {
            List {
                Section("Reflection") {
                    Toggle("AI depth (gentle follow-up questions)", isOn: $aiDepth)
                        .onChange(of: aiDepth) { _, newValue in
                            Task { await appState.updateAIDepth(newValue) }
                        }
                }
                Section("Account") {
                    if let email = appState.currentUser?.email { Text(email) }
                    else { Text("Signed in") }
                    Button("Sign out", role: .destructive) {
                        appState.signOut()
                        dismiss()
                    }
                }
                Section("Your data") {
                    Button("Export my journal (JSON)") {
                        Task { await exportData() }
                    }
                    Button("Delete account", role: .destructive) { showDeleteConfirm = true }
                }
                Section("Trust") {
                    NavigationLink("Privacy & AI") { PrivacyTrustView() }
                    Link("Crisis resources", destination: URL(string: "https://988lifeline.org")!)
                }
                if let statusMessage {
                    Section { Text(statusMessage).font(.footnote) }
                }
            }
            .navigationTitle("Settings")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) { Button("Done") { dismiss() } }
            }
            .onAppear { aiDepth = appState.currentUser?.aiDepthEnabled ?? true }
            .confirmationDialog("Delete your account and all journal data?", isPresented: $showDeleteConfirm) {
                Button("Delete everything", role: .destructive) {
                    Task { await deleteAccount() }
                }
            }
        }
    }

    private func exportData() async {
        guard let token = appState.accessToken else { return }
        var req = URLRequest(url: APIConfig.baseURL.appending(path: "me/export"))
        req.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        do {
            let (data, _) = try await URLSession.shared.data(for: req)
            let url = FileManager.default.temporaryDirectory.appendingPathComponent("seedjournal-export.json")
            try data.write(to: url)
            statusMessage = "Export saved to \(url.lastPathComponent) in Files."
        } catch {
            statusMessage = "Export failed."
        }
    }

    private func deleteAccount() async {
        guard let token = appState.accessToken else { return }
        var req = URLRequest(url: APIConfig.baseURL.appending(path: "me"))
        req.httpMethod = "DELETE"
        req.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        do {
            let (_, resp) = try await URLSession.shared.data(for: req)
            if (resp as? HTTPURLResponse)?.statusCode == 204 {
                appState.signOut()
                dismiss()
            } else {
                statusMessage = "Could not delete account."
            }
        } catch {
            statusMessage = "Could not delete account."
        }
    }
}

struct PrivacyTrustView: View {
    private var privacyURL: URL? {
        guard let raw = Bundle.main.object(forInfoDictionaryKey: "SEEDJOURNAL_PRIVACY_URL") as? String,
              let url = URL(string: raw), !raw.isEmpty
        else { return nil }
        return url
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("SeedJournal is a private reflection journal, not therapy or medical care.")
                    .font(DesignTokens.FontToken.editorial(18))
                Text("Your entries may be processed by AI to suggest gentle questions and extract memories you can search later. You can turn AI depth off in a future update.")
                    .font(DesignTokens.FontToken.journal(15))
                    .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.7))
                if let privacyURL {
                    Link("Privacy policy", destination: privacyURL)
                        .font(DesignTokens.FontToken.journal(15))
                }
            }
            .padding()
        }
        .background(DesignTokens.ColorToken.paper)
        .navigationTitle("Privacy & AI")
    }
}

#Preview {
    TreeHomeView().environment(AppState())
}