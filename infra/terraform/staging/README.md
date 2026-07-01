# Terraform — Staging (Fly.io)

Manages the **Fly app shell** and machine env. **Container images** still deploy via:

```bash
cd backend && fly deploy
```

Terraform does not replace `fly deploy` for code releases—it pins infra + secrets-shaped env on the machine.

## First-time workflow

1. Create Neon DB + `CREATE EXTENSION vector;`
2. Copy `terraform.tfvars.example` → `terraform.tfvars` (gitignored)
3. `fly auth token` → `fly_api_token`
4. Build & push first image so machine can start:

```bash
cd backend
fly apps create seedjournal-api-staging  # if not exists
fly deploy
```

5. Apply Terraform (optional, if you prefer IaC for machine/env):

```bash
cd infra/terraform/staging
terraform init
terraform plan
terraform apply
```

## Provider note

The `fly-apps/fly` provider evolves quickly. If `fly_machine` conflicts with your account, use **`fly.toml` + `fly secrets`** only (`docs/STAGING_DEPLOY.md`) and treat this module as reference.

## State

Keep `terraform.tfvars` and state files out of git. Use S3 or Terraform Cloud for team state.