import AuthenticationServices
import Foundation
import Observation
import UIKit

@Observable
@MainActor
final class AppState {
    var accessToken: String? {
        didSet { SessionStore.accessToken = accessToken }
    }
    var currentUser: MeResponse?
    var isLoadingSession = false
    var sessionError: String?

    private let appleSignIn = AppleSignInCoordinator()

    private var client: APIClient {
        APIClient(accessToken: accessToken)
    }

    init() {
        accessToken = SessionStore.accessToken
    }

    func bootstrap() async {
        guard let accessToken, !accessToken.isEmpty else { return }
        isLoadingSession = true
        sessionError = nil
        defer { isLoadingSession = false }
        do {
            currentUser = try await client.get("/me")
        } catch {
            self.accessToken = nil
            self.currentUser = nil
            sessionError = (error as? LocalizedError)?.errorDescription
        }
    }

    func signInWithApple() async {
        isLoadingSession = true
        sessionError = nil
        defer { isLoadingSession = false }
        do {
            let window = UIApplication.shared.connectedScenes
                .compactMap { $0 as? UIWindowScene }
                .flatMap(\.windows)
                .first { $0.isKeyWindow }
            let identityToken = try await appleSignIn.signIn(
                presentationAnchor: window ?? ASPresentationAnchor()
            )
            let req = AppleAuthRequest(identityToken: identityToken)
            let token: TokenResponse = try await APIClient(accessToken: nil)
                .post("/auth/apple", body: req)
            accessToken = token.accessToken
            currentUser = try await client.get("/me")
        } catch {
            sessionError = (error as? LocalizedError)?.errorDescription ?? "Sign in failed."
        }
    }

    #if DEBUG
    func devSignIn(sub: String = "ios-dev-user", email: String = "dev@seedjournal.local") async {
        isLoadingSession = true
        sessionError = nil
        defer { isLoadingSession = false }
        let tokenJSON = "{\"sub\":\"\(sub)\",\"email\":\"\(email)\"}"
        let req = AppleAuthRequest(identityToken: tokenJSON)
        do {
            let token: TokenResponse = try await APIClient(accessToken: nil)
                .post("/auth/apple", body: req)
            accessToken = token.accessToken
            currentUser = try await client.get("/me")
        } catch {
            sessionError = (error as? LocalizedError)?.errorDescription ?? "Sign in failed."
        }
    }
    #endif

    func updateAIDepth(_ enabled: Bool) async {
        guard accessToken != nil else { return }
        do {
            let req = MePatchRequest(timezone: nil, aiDepthEnabled: enabled)
            currentUser = try await client.patch("/me", body: req)
        } catch {
            sessionError = (error as? LocalizedError)?.errorDescription
        }
    }

    func signOut() {
        accessToken = nil
        currentUser = nil
    }
}