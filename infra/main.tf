terraform {
  required_providers {
    render = {
      source  = "render/api"
      version = "~> 0.4"
    }
  }
}

provider "render" {
  api_key = var.render_api_key
}

resource "render_service" "app" {
  name        = "secure-api-protection"
  repo        = "github.com/yourusername/secure-api-protection"
  branch      = "main"
  plan        = "free"
  env_vars = {
    "ENV" = "production"
  }
}
