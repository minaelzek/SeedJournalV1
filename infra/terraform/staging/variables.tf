variable "fly_api_token" {
  type        = string
  sensitive   = true
  description = "Fly.io API token (fly auth token)"
}

variable "fly_org" {
  type        = string
  description = "Fly organization slug"
}

variable "app_name" {
  type        = string
  default     = "seedjournal-api-staging"
  description = "Fly app name for staging API"
}

variable "primary_region" {
  type    = string
  default = "iad"
}

variable "database_url" {
  type        = string
  sensitive   = true
  description = "postgresql+asyncpg://... with pgvector-enabled Postgres"
}

variable "jwt_secret" {
  type        = string
  sensitive   = true
  description = "Long random JWT signing secret"
}

variable "apple_client_id" {
  type    = string
  default = "com.seedjournal.app"
}

variable "openai_api_key" {
  type        = string
  sensitive   = true
  default     = ""
  description = "Leave empty to keep LLM_PROVIDER=stub on staging"
}

variable "llm_provider" {
  type    = string
  default = "stub"
}

variable "cors_origins" {
  type    = string
  default = ""
}