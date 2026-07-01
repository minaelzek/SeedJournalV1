import SwiftUI

/// Zen + editorial luxury palette — calm, mature, premium.
enum DesignTokens {
    enum ColorToken {
        static let paper = Color(red: 0.97, green: 0.96, blue: 0.94)
        static let ink = Color(red: 0.12, green: 0.11, blue: 0.10)
        static let sakura = Color(red: 0.91, green: 0.72, blue: 0.78)
        static let moss = Color(red: 0.45, green: 0.55, blue: 0.48)
        static let skyWash = Color(red: 0.88, green: 0.92, blue: 0.95)

        static func resolvedPaper(_ scheme: ColorScheme) -> Color {
            scheme == .dark ? Color(red: 0.11, green: 0.11, blue: 0.12) : Color(red: 0.97, green: 0.96, blue: 0.94)
        }

        static func resolvedInk(_ scheme: ColorScheme) -> Color {
            scheme == .dark ? Color(red: 0.92, green: 0.91, blue: 0.89) : Color(red: 0.12, green: 0.11, blue: 0.10)
        }
    }

    static func backgroundGradient(colorScheme: ColorScheme, season: String) -> LinearGradient {
        let paper = ColorToken.resolvedPaper(colorScheme)
        let top: Color
        if season == "winter" {
            top = colorScheme == .dark ? Color(red: 0.15, green: 0.17, blue: 0.2) : Color(red: 0.82, green: 0.86, blue: 0.9)
        } else {
            top = colorScheme == .dark ? Color(red: 0.14, green: 0.16, blue: 0.18) : ColorToken.skyWash
        }
        return LinearGradient(colors: [top, paper], startPoint: .top, endPoint: .bottom)
    }

    enum FontToken {
        static func editorial(_ size: CGFloat) -> Font {
            .system(size: size, weight: .medium, design: .serif)
        }

        static func journal(_ size: CGFloat) -> Font {
            .system(size: size, weight: .regular, design: .default)
        }
    }

    enum Spacing {
        static let xs: CGFloat = 8
        static let sm: CGFloat = 16
        static let md: CGFloat = 24
        static let lg: CGFloat = 40
    }

    enum Radius {
        static let soft: CGFloat = 14
        static let pill: CGFloat = 28
    }
}