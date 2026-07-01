import Foundation

enum SessionStore {
    private static let tokenAccount = "access_token"

    static var accessToken: String? {
        get { KeychainStore.load(account: tokenAccount) }
        set {
            if let newValue {
                _ = KeychainStore.save(newValue, account: tokenAccount)
            } else {
                KeychainStore.delete(account: tokenAccount)
            }
        }
    }
}