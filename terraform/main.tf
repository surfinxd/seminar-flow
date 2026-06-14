# 1. Enable Required Google API Services
resource "google_project_service" "container_api" {
  service                    = "container.googleapis.com"
  disable_dependent_services = false
  disable_on_destroy         = false
}

resource "google_project_service" "artifactregistry_api" {
  service                    = "artifactregistry.googleapis.com"
  disable_dependent_services = false
  disable_on_destroy         = false
}

resource "google_project_service" "compute_api" {
  service                    = "compute.googleapis.com"
  disable_dependent_services = false
  disable_on_destroy         = false
}

resource "google_project_service" "iam_api" {
  service                    = "iam.googleapis.com"
  disable_dependent_services = false
  disable_on_destroy         = false
}

# 2. VPC Network and Subnet for GKE
resource "google_compute_network" "vpc_network" {
  name                    = "seminar-flow-vpc"
  auto_create_subnetworks = false

  depends_on = [google_project_service.compute_api]
}

resource "google_compute_subnetwork" "gke_subnet" {
  name          = "seminar-flow-subnet"
  ip_cidr_range = "10.0.0.0/20"
  network       = google_compute_network.vpc_network.id
  region        = var.region

  # Secondary ranges for GKE Pods and Services (VPC-Native)
  secondary_ip_range {
    range_name    = "gke-pods-range"
    ip_cidr_range = "10.4.0.0/14"
  }

  secondary_ip_range {
    range_name    = "gke-services-range"
    ip_cidr_range = "10.8.0.0/20"
  }
}

# 3. Google Kubernetes Engine (GKE) Cluster
resource "google_container_cluster" "gke_cluster" {
  name     = "seminar-flow-cluster"
  location = var.region

  # Configure VPC-native networking
  network    = google_compute_network.vpc_network.id
  subnetwork = google_compute_subnetwork.gke_subnet.id

  ip_allocation_policy {
    cluster_secondary_range_name  = "gke-pods-range"
    services_secondary_range_name = "gke-services-range"
  }

  # Best practice: Delete default node pool and create a separate one
  remove_default_node_pool = true
  initial_node_count       = 1
  deletion_protection      = false

  # 임시 노드 생성 시에도 커스텀 서비스 계정을 부여하여 기본 Compute SA 사용 권한 충돌 방지
  node_config {
    service_account = google_service_account.gke_nodes.email
  }

  depends_on = [
    google_project_service.container_api,
    google_service_account.gke_nodes
  ]
}

# Separate Node Pool for GKE (cost-effective e2-medium nodes)
resource "google_container_node_pool" "gke_nodes" {
  name       = "seminar-flow-node-pool"
  location   = var.region
  cluster    = google_container_cluster.gke_cluster.name
  node_count = 2

  node_config {
    preemptible  = false
    machine_type = "e2-medium"
    disk_size_gb = 50

    # ⚠️ 기본 서비스 계정 대신 커스텀 서비스 계정 할당 (최소 권한 준수)
    service_account = google_service_account.gke_nodes.email

    # Needed for GKE nodes to fetch images and manage resources
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      env = "dev"
    }

    tags = ["gke-node", "seminar-flow"]
  }
}

# GKE 노드 전용 서비스 계정 정의
resource "google_service_account" "gke_nodes" {
  account_id   = "gke-node-sa"
  display_name = "GKE Node Pool Service Account"

  depends_on = [google_project_service.iam_api]
}

# GKE 노드 구동을 위한 최소 권한 부여 (로깅, 모니터링)
resource "google_project_iam_member" "gke_nodes_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.gke_nodes.email}"
}

resource "google_project_iam_member" "gke_nodes_monitoring_metric" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.gke_nodes.email}"
}

resource "google_project_iam_member" "gke_nodes_monitoring_viewer" {
  project = var.project_id
  role    = "roles/monitoring.viewer"
  member  = "serviceAccount:${google_service_account.gke_nodes.email}"
}

# 생성된 Artifact Registry의 도커 이미지를 GKE 노드가 풀(Pull)할 수 있도록 읽기 권한만 부여
resource "google_artifact_registry_repository_iam_member" "gar_reader" {
  location   = google_artifact_registry_repository.gar_repo.location
  repository = google_artifact_registry_repository.gar_repo.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.gke_nodes.email}"
}

# 4. Google Artifact Registry (GAR) Docker Repository
resource "google_artifact_registry_repository" "gar_repo" {
  location      = var.region
  repository_id = "seminar-flow"
  description   = "Docker Repository for SeminarFlow App"
  format        = "DOCKER"

  depends_on = [google_project_service.artifactregistry_api]
}

# 5. Service Account and IAM for GitHub Actions CI/CD
resource "google_service_account" "github_actions" {
  account_id   = "github-actions-sa"
  display_name = "GitHub Actions CI/CD Service Account"

  depends_on = [google_project_service.iam_api]
}

# Grant the Service Account write permission to Google Artifact Registry repository
resource "google_artifact_registry_repository_iam_member" "gar_writer" {
  location   = google_artifact_registry_repository.gar_repo.location
  repository = google_artifact_registry_repository.gar_repo.name
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.github_actions.email}"
}
