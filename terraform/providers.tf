terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.68.0"
    }
  }
}

provider "google" {
  project = local.envs["GCP_PROJECT"]
  region = local.envs["GCP_REGION"]
  zone = "us-central1-a"
}