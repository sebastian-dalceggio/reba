resource "google_storage_bucket" "reba_bucket_sd" {
  name          = local.envs["BUCKET_NAME"]
  location      = local.envs["GCP_REGION"]
  storage_class = "STANDARD"
  force_destroy = true

  uniform_bucket_level_access = true
}