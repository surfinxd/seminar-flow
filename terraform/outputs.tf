output "gke_cluster_name" {
  value       = google_container_cluster.gke_cluster.name
  description = "The name of the GKE Cluster"
}

output "gke_cluster_endpoint" {
  value       = google_container_cluster.gke_cluster.endpoint
  description = "The IP address of the GKE Cluster control plane"
}

output "artifact_registry_repository_url" {
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.gar_repo.repository_id}"
  description = "The URL of the Google Artifact Registry repository"
}

output "github_actions_sa_email" {
  value       = google_service_account.github_actions.email
  description = "The email address of the GitHub Actions CI/CD service account"
}
