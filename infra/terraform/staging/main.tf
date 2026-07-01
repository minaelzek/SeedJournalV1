provider "fly" {
  fly_api_token = var.fly_api_token
}

# App registration only — deploy code with: cd backend && fly deploy
resource "fly_app" "api" {
  name = var.app_name
  org  = var.fly_org
}

output "api_hostname" {
  value = "${fly_app.api.name}.fly.dev"
}

output "health_url" {
  value = "https://${fly_app.api.name}.fly.dev/health"
}

output "deploy_hint" {
  value = "cd backend && fly secrets set DATABASE_URL=... JWT_SECRET=... && fly deploy -a ${fly_app.api.name}"
}