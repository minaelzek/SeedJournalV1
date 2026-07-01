import Foundation

struct TokenResponse: Codable {
    let accessToken: String
    let tokenType: String
    let expiresIn: Int

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case tokenType = "token_type"
        case expiresIn = "expires_in"
    }
}

struct AppleAuthRequest: Codable {
    let identityToken: String

    enum CodingKeys: String, CodingKey {
        case identityToken = "identity_token"
    }
}

struct MePatchRequest: Codable {
    let timezone: String?
    let aiDepthEnabled: Bool?

    enum CodingKeys: String, CodingKey {
        case timezone
        case aiDepthEnabled = "ai_depth_enabled"
    }
}

struct MeResponse: Codable {
    let id: UUID
    let email: String?
    let timezone: String
    let aiDepthEnabled: Bool
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id, email, timezone
        case aiDepthEnabled = "ai_depth_enabled"
        case createdAt = "created_at"
    }
}

struct EntryCreate: Codable {
    let title: String?
    let body: String
}

struct EntryResponse: Codable, Identifiable {
    let id: UUID
    let title: String?
    let body: String
    let wordCount: Int
    let reflectionCompleted: Bool
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id, title, body
        case wordCount = "word_count"
        case reflectionCompleted = "reflection_completed"
        case createdAt = "created_at"
    }
}

struct EntryListResponse: Codable {
    let items: [EntryListItem]
    let nextCursor: Date?

    enum CodingKeys: String, CodingKey {
        case items
        case nextCursor = "next_cursor"
    }
}

struct ReflectionTurnDTO: Codable, Identifiable {
    let id: UUID
    let role: String
    let content: String
    let sequence: Int
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id, role, content, sequence
        case createdAt = "created_at"
    }

    var isAssistant: Bool { role == "assistant" }
}

struct ReflectionStartResponse: Codable {
    let sessionId: UUID
    let assistantMessage: ReflectionTurnDTO?
    let turnCount: Int
    let maxTurns: Int

    enum CodingKeys: String, CodingKey {
        case sessionId = "session_id"
        case assistantMessage = "assistant_message"
        case turnCount = "turn_count"
        case maxTurns = "max_turns"
    }
}

struct ReflectionMessageRequest: Codable {
    let message: String
}

struct ReflectionMessageResponse: Codable {
    let userTurn: ReflectionTurnDTO
    let assistantTurn: ReflectionTurnDTO?
    let turnCount: Int
    let maxTurns: Int
    let limitReached: Bool

    enum CodingKeys: String, CodingKey {
        case userTurn = "user_turn"
        case assistantTurn = "assistant_turn"
        case turnCount = "turn_count"
        case maxTurns = "max_turns"
        case limitReached = "limit_reached"
    }
}

struct ReflectionCompleteResponse: Codable {
    let entryId: UUID
    let reflectionCompleted: Bool
    let completedAt: Date?

    enum CodingKeys: String, CodingKey {
        case entryId = "entry_id"
        case reflectionCompleted = "reflection_completed"
        case completedAt = "completed_at"
    }
}

struct EntryListItem: Codable, Identifiable {
    let id: UUID
    let title: String?
    let bodyPreview: String
    let wordCount: Int
    let reflectionCompleted: Bool
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id, title
        case bodyPreview = "body_preview"
        case wordCount = "word_count"
        case reflectionCompleted = "reflection_completed"
        case createdAt = "created_at"
    }
}