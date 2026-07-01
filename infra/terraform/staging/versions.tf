terraform {
  required_version = ">= 1.5.0"

  required_providers {
    fly = {
      source  = "fly-apps/fly"
      version = "~> 0.0.36"
    }
  }

  # Optional remote state (uncomment after creating bucket)
  # backend "s3" {
  #   bucket = "seedjournal-terraform-state"
  #   key    = "staging/terraform.tfstate"
  #   region = "us-east-1"
  # }
}