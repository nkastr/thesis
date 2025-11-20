
variable "gcp_project_id" {
  type        = string
  description = "The GCP project ID to apply this config to"
  default = "thesis-413009" 
}

variable "name" {
  type        = string
  description = "Name given to the new GKE cluster"
  default     = "thesis-cluster"
}

variable "region" {
  type        = string
  description = "Region of the new GKE cluster"
  default     = "europe-west1"
}

variable "namespace" {
  type        = string
  description = "Kubernetes Namespace in which the Online Boutique resources are to be deployed"
  default     = "default"
}

variable "filepath_manifest" {
  type        = string
  description = "Path to Online Boutique's Kubernetes resources, written using Kustomize"
  default     = "../eshop-k8s-manifest-imgs/"
}

variable "memorystore" {
  type        = bool
  description = "If true, Online Boutique's in-cluster Redis cache will be replaced with a Google Cloud Memorystore Redis cache"
  default = false
}

variable "multi-zonal" {
  type = bool
  description = "If true, we want to create a multi-zonal cluster"
  default = false
}

variable "zone" {
  type = string
  description = "The zone the cluster is created into, provided that it is a single zone cluster"
  default = "europe-west1-b"
}

variable "helm-charts" {
  type = string
  description = "The filepath for the helm chart files"
  default = "../configs/helm-charts"
}

variable "configuration_path" {
  type = string
  description = "The file path to config files"
  default = "../configs"
}

variable "credentials_gcp" { 
  type = string
  description = "Service account credentials filepath"
  default = "./configs" 
}

variable "node_count" {
  type = number
  description = "The number of nodes each node pool will have"
  default = 1
}

# multi cluster variables

variable "cluster-alias" {
  type = list(string)
  description = "Aliases to loop and create multiple gke clusters for the multi cluster"
  default = ["edge-cluster-1", "edge-cluster-2"]#, "fog-cluster-1", "fog-cluster-2", "cloud-cluster"]
}

variable "cluster-zone" {
  type = list(string)
  description = "Zones for each cluster"
  default = ["europe-west1-b", "europe-southwest1-a"]#, "us-central1-a", "us-east1-b", "southamerica-east1-a"]
}

variable "cluster-name" {
  type = list(string)
  description = "Names of clusters in MCS"
  default = ["edge-cluster-1", "edge-cluster-2"]#, "fog-cluster-1", "fog-cluster-2", "cloud-cluster"]
}

variable "service_account_name" {
  type = string
  description = "Name of the service account used for auth purposes"
  default = "thesis-service-account"
}

variable "pod-ips" {
  type = list(string)
  description = "The ip ranges for the pods in the clusters"
  default = [ "10.8.0.0/14", "10.16.0.0/14", "10.24.0.0/14", "10.32.0.0/14", "10.48.0.0/14"]
}

variable "service-ips" {
  type = list(string)
  description = "The ip ranges for the services in the clusters"
  default = [ "10.12.0.0/20", "10.20.0.0/20", "10.28.0.0/20", "10.36.0.0/20", "10.52.0.0/20"]
}