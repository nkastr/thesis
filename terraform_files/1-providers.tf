terraform {
  # backend "gcs" {
  #   bucket = "iliadis_bucket"
  #   prefix = "terraform/state"
  # }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.74.0"  # 4.63.1
    }

    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.21.1"
    }

    helm = {
      source = "hashicorp/helm"
      version = "2.10.1"
    }

    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }

    # for anthos & fleet
    # google-beta = {
    #   source = "hashicorp/google-beta"
    #   version = "3.67.0"
    # }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.region
  credentials = file("${var.credentials_gcp}/service-account.json")
}

# https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs

# provider "kubernetes" {
#   # counter = length(var.cluster-alias)
#   host                   = "https://${google_container_cluster.primary.endpoint}"   # edge-1 
#   token                  = data.google_client_config.main.access_token
#   cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth.0.cluster_ca_certificate)
#   # alias = "cluster-edge-1"
# }

# provider "google-beta" {
#   credentials = file("${var.credentials_gcp}/service-account.json")
#   project = var.gcp_project_id
# }

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

provider "kubernetes" {
  host                   = "https://${google_container_cluster.primary.endpoint}"
  token                  = data.google_client_config.main.access_token
  cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth.0.cluster_ca_certificate)
  # alias = "edge1"
}

# provider "kubernetes" {
#   host                   = "https://${google_container_cluster.edge-2.endpoint}"
#   token                  = data.google_client_config.main.access_token
#   cluster_ca_certificate = base64decode(google_container_cluster.edge-2.master_auth.0.cluster_ca_certificate)
#   alias = "edge2"
# }

# provider "kubernetes" {
#   host                   = "https://${google_container_cluster.fog-1.endpoint}"
#   token                  = data.google_client_config.main.access_token
#   cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth.0.cluster_ca_certificate)
#   alias = "cluster-fog-1"
# }

# provider "kubernetes" {
#   host                   = "https://${google_container_cluster.fog-2.endpoint}"
#   token                  = data.google_client_config.main.access_token
#   cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth.0.cluster_ca_certificate)
#   alias = "cluster-fog-2"
# }

# provider "kubernetes" {
#   host                   = "https://${google_container_cluster.cloud.endpoint}"
#   token                  = data.google_client_config.main.access_token
#   cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth.0.cluster_ca_certificate)
#   alias = "cluster-cloud"
# }

# provider "kubectl" {
#   host                   = "https://${google_container_cluster.primary.endpoint}"
#   token                  = data.google_client_config.main.access_token
#   cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth.0.cluster_ca_certificate)
#   load_config_file       = false
# }
