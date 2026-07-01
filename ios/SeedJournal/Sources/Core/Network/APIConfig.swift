import Foundation

enum APIConfig {
    static var baseURL: URL {
        if let url = Bundle.main.urlForSeedJournalAPI {
            return url
        }
        #if DEBUG
        return URL(string: "http://127.0.0.1:8000/v1")!
        #else
        return URL(string: "https://api.seedjournal.app/v1")!
        #endif
    }
}

private extension Bundle {
    var urlForSeedJournalAPI: URL? {
        guard let raw = object(forInfoDictionaryKey: "SEEDJOURNAL_API_BASE_URL") as? String,
              !raw.isEmpty,
              let url = URL(string: raw)
        else { return nil }
        return url
    }
}