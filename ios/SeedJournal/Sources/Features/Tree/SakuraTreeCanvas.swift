import SwiftUI

struct TreeVisualState: Equatable {
    var stage: String
    var season: String
    var rootsCount: Int
    var branchesCount: Int
    var leavesCount: Int
    var flowersCount: Int
}

struct SakuraTreeCanvas: View {
    let state: TreeVisualState
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    private var seasonPalette: (sky: Color, ground: Color, accent: Color) {
        switch state.season.lowercased() {
        case "winter":
            return (
                Color(red: 0.82, green: 0.86, blue: 0.9),
                DesignTokens.ColorToken.moss.opacity(0.08),
                DesignTokens.ColorToken.ink.opacity(0.25)
            )
        case "autumn":
            return (
                Color(red: 0.93, green: 0.88, blue: 0.82),
                DesignTokens.ColorToken.moss.opacity(0.14),
                Color(red: 0.75, green: 0.55, blue: 0.45)
            )
        case "summer":
            return (
                DesignTokens.ColorToken.skyWash,
                DesignTokens.ColorToken.moss.opacity(0.18),
                DesignTokens.ColorToken.moss
            )
        default:
            return (
                DesignTokens.ColorToken.skyWash,
                DesignTokens.ColorToken.moss.opacity(0.12),
                DesignTokens.ColorToken.sakura
            )
        }
    }

    private var trunkHeight: CGFloat {
        switch state.stage.lowercased() {
        case "blooming", "sakura": return 88
        case "sapling": return 64
        case "sprout": return 40
        default: return 24
        }
    }

    var body: some View {
        let palette = seasonPalette
        TimelineView(.animation(minimumInterval: reduceMotion ? 3600 : 1 / 30)) { timeline in
            let t = reduceMotion ? 0.0 : timeline.date.timeIntervalSinceReferenceDate
            Canvas { context, size in
                let center = CGPoint(x: size.width / 2, y: size.height * 0.55)
                let groundY = size.height * 0.78

                var ground = Path()
                ground.addEllipse(in: CGRect(x: center.x - 110, y: groundY, width: 220, height: 36))
                context.fill(ground, with: .color(palette.ground))

                for i in 0..<min(state.rootsCount, 8) {
                    let angle = Double(i) / 8.0 * .pi - .pi / 2
                    var root = Path()
                    root.move(to: CGPoint(x: center.x, y: groundY + 8))
                    root.addQuadCurve(
                        to: CGPoint(
                            x: center.x + CGFloat(cos(angle)) * 36,
                            y: groundY + 28
                        ),
                        control: CGPoint(x: center.x + CGFloat(cos(angle)) * 18, y: groundY + 20)
                    )
                    context.stroke(root, with: .color(palette.accent.opacity(0.35)), lineWidth: 2)
                }

                var trunk = Path()
                trunk.move(to: CGPoint(x: center.x, y: groundY + 4))
                trunk.addLine(to: CGPoint(x: center.x, y: groundY - trunkHeight))
                context.stroke(trunk, with: .color(palette.accent.opacity(0.55)), lineWidth: 6)

                let branchN = min(max(state.branchesCount, 1), 6)
                for i in 0..<branchN {
                    let side: CGFloat = i % 2 == 0 ? -1 : 1
                    let y = groundY - trunkHeight + CGFloat(i) * 12
                    var branch = Path()
                    branch.move(to: CGPoint(x: center.x, y: y))
                    branch.addQuadCurve(
                        to: CGPoint(x: center.x + side * (40 + CGFloat(i) * 6), y: y - 18),
                        control: CGPoint(x: center.x + side * 24, y: y - 6)
                    )
                    context.stroke(branch, with: .color(palette.accent.opacity(0.4)), lineWidth: 3)
                }

                let leafN = min(state.leavesCount, 24)
                for i in 0..<leafN {
                    let seed = Double(i * 17 + state.leavesCount)
                    let lx = center.x + CGFloat(sin(seed + t * 0.15) * 55)
                    let ly = groundY - trunkHeight - 20 - CGFloat(i % 6) * 8
                    let leaf = CGRect(x: lx, y: ly, width: 8, height: 5)
                    context.fill(
                        Path(ellipseIn: leaf),
                        with: .color(DesignTokens.ColorToken.moss.opacity(0.45))
                    )
                }

                let flowerN = min(state.flowersCount, 12)
                for i in 0..<flowerN {
                    let seed = Double(i * 13)
                    let fx = center.x + CGFloat(cos(seed) * 42)
                    let fy = groundY - trunkHeight - 36 - CGFloat(i % 4) * 10
                    context.fill(
                        Path(ellipseIn: CGRect(x: fx, y: fy, width: 10, height: 10)),
                        with: .color(DesignTokens.ColorToken.sakura.opacity(0.85))
                    )
                }

                if state.stage.lowercased() == "seed" {
                    context.fill(
                        Path(ellipseIn: CGRect(x: center.x - 10, y: groundY - 8, width: 20, height: 14)),
                        with: .color(palette.accent.opacity(0.5))
                    )
                }
            }
        }
        .overlay(alignment: .bottom) {
            Text(state.stage.capitalized)
                .font(DesignTokens.FontToken.editorial(13))
                .foregroundStyle(DesignTokens.ColorToken.ink.opacity(0.35))
                .padding(.bottom, 4)
        }
    }
}