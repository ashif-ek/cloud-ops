
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

resource "docker_network" "cloudops_network" {
  name = "cloudops-network"
}

resource "docker_image" "postgres" {
  name         = "postgres:17-alpine"
  keep_locally = true
}

resource "docker_container" "postgres" {
  name  = "cloudops-postgres-tf"
  image = docker_image.postgres.image_id

  networks_advanced {
    name = docker_network.cloudops_network.name
  }

  env = [
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]

  ports {
    internal = 5432
    external = 5434
  }

  restart = "unless-stopped"
}

resource "docker_image" "api" {
  name = "cloudops-task-manager:terraform"

  build {
    context = ".."
  }

  keep_locally = true
}

resource "docker_container" "api" {
  name  = "cloudops-api-tf"
  image = docker_image.api.image_id

  networks_advanced {
    name = docker_network.cloudops_network.name
  }

  env = [
    "APP_NAME=CloudOps Task Manager",
    "ENVIRONMENT=production",
    "DATABASE_URL=postgresql+psycopg://${var.postgres_user}:${var.postgres_password}@cloudops-postgres-tf:5432/${var.postgres_db}"
  ]

  ports {
    internal = 8000
    external = 8001
  }

  restart = "unless-stopped"

  depends_on = [
    docker_container.postgres
  ]
}
