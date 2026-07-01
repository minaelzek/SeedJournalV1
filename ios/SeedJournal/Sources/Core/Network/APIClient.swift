import Foundation

enum APIError: LocalizedError {
    case unauthorized
    case server(Int)
    case decoding
    case network(Error)

    var errorDescription: String? {
        switch self {
        case .unauthorized: return "Please sign in again."
        case .server(let code): return "Something went wrong (\(code))."
        case .decoding: return "Could not read the response."
        case .network(let err): return err.localizedDescription
        }
    }
}

struct APIClient {
    var accessToken: String?

    func post<T: Encodable, R: Decodable>(_ path: String, body: T) async throws -> R {
        try await request(path, method: "POST", body: body)
    }

    func get<R: Decodable>(_ path: String) async throws -> R {
        try await request(path, method: "GET", bodyData: nil)
    }

    func patch<T: Encodable, R: Decodable>(_ path: String, body: T) async throws -> R {
        try await request(path, method: "PATCH", body: body)
    }

    private func request<T: Encodable, R: Decodable>(
        _ path: String,
        method: String,
        body: T
    ) async throws -> R {
        let data = try JSONEncoder.api.encode(body)
        return try await request(path, method: method, bodyData: data)
    }

    private func request<R: Decodable>(
        _ path: String,
        method: String,
        bodyData: Data?
    ) async throws -> R {
        var url = APIConfig.baseURL
        url.append(path: path.trimmingCharacters(in: CharacterSet(charactersIn: "/")))

        var req = URLRequest(url: url)
        req.httpMethod = method
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        if let accessToken {
            req.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        }
        if let bodyData {
            req.httpBody = bodyData
        }

        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await URLSession.shared.data(for: req)
        } catch {
            throw APIError.network(error)
        }

        guard let http = response as? HTTPURLResponse else {
            throw APIError.server(-1)
        }
        if http.statusCode == 401 { throw APIError.unauthorized }
        guard (200 ... 299).contains(http.statusCode) else {
            throw APIError.server(http.statusCode)
        }
        do {
            return try JSONDecoder.api.decode(R.self, from: data)
        } catch {
            throw APIError.decoding
        }
    }
}

extension JSONEncoder {
    static let api: JSONEncoder = {
        let e = JSONEncoder()
        e.dateEncodingStrategy = .iso8601
        return e
    }()
}

extension JSONDecoder {
    static let api: JSONDecoder = {
        let d = JSONDecoder()
        d.dateDecodingStrategy = .iso8601
        return d
    }()
}