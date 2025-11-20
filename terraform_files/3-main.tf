# Enable services
module "project-services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "14.3.0"
  project_id  = var.gcp_project_id
  disable_services_on_destroy = false
  activate_apis = [
    "compute.googleapis.com",
    "iam.googleapis.com",
    "container.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "anthos.googleapis.com",
    "cloudtrace.googleapis.com",
    "meshca.googleapis.com",
    "meshtelemetry.googleapis.com",
    "meshconfig.googleapis.com",
    "iamcredentials.googleapis.com",
    "gkeconnect.googleapis.com",
    "gkehub.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    # mcs required services (some are above)
    "multiclusterservicediscovery.googleapis.com",
    "trafficdirector.googleapis.com",
    "dns.googleapis.com"
  ]
}

# resource "google_project_service" "compute" {
#     service = "compute.googleapis.com"
#     disable_dependent_services = true
# }

# resource "google_project_service" "container" {
#     service = "container.googleapis.com"
#     disable_dependent_services = true
# }

# K8s Clusters

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster

# cluster
resource "google_container_cluster" "primary" {
    name = "thesis" # var.cluster-alias[0]       
    location =  var.cluster-zone[0]   
    remove_default_node_pool = true
    initial_node_count = 1 

    # logging_service = "none"         
    # monitoring_service = "none"         
    networking_mode = "VPC_NATIVE"

    addons_config {
        http_load_balancing {
          disabled = false   # has to be enabled for multi cluster ingress
        }

        horizontal_pod_autoscaling {
          disabled = true
        }
     }

     vertical_pod_autoscaling {
       enabled = false
     }

     release_channel {
       channel = "REGULAR"
     }

     workload_identity_config {
       workload_pool = "${var.gcp_project_id}.svc.id.goog"
     }

     ip_allocation_policy {
       cluster_ipv4_cidr_block =   ""   # var.pod-ips[count.index]
       services_ipv4_cidr_block =  ""   # var.service-ips[count.index]
     }
    depends_on = [ 
        # google_project_service.compute,
        # google_project_service.container,
        module.project-services
     ]
}

# Node pools
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_node_pool

# node pool as edge1
resource "google_container_node_pool" "edge1" {
    name = "edge1"
    cluster = google_container_cluster.primary.id
    node_count = var.node_count

    management {
      auto_repair = true
      auto_upgrade = true
    }

    node_config {
      preemptible = true
      machine_type = "e2-standard-2"    # "e2-medium"     # 2vcpu & 4gb mem   
      disk_size_gb = "40"
      disk_type    = "pd-standard"
      image_type   = "COS_CONTAINERD"

      labels = {
        role = "general"
      }

      service_account = "${var.service_account_name}@${var.gcp_project_id}.iam.gserviceaccount.com" # google_service_account.my-svc-acc.email

      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]
    }
    
    depends_on = [ google_container_cluster.primary ]
}

# node pool as edge2
# resource "google_container_node_pool" "edge2" {
#     name = "edge2"
#     cluster = google_container_cluster.primary.id
#     node_count = var.node_count

#     management {
#       auto_repair = true
#       auto_upgrade = true
#     }

#     node_config {
#       preemptible = true
#       machine_type = "e2-standard-2"      #  "e2-medium"     # 2vcpu & 4gb mem  
#       disk_size_gb = "40"
#       disk_type    = "pd-standard"
#       image_type   = "COS_CONTAINERD"

#       labels = {
#         role = "general"
#       }

#       service_account = "${var.service_account_name}@${var.gcp_project_id}.iam.gserviceaccount.com" # google_service_account.my-svc-acc.email

#       oauth_scopes = [
#         "https://www.googleapis.com/auth/cloud-platform"
#       ]
#     }
    
#     depends_on = [ google_container_cluster.primary ]
# }

# node pool as fog1
resource "google_container_node_pool" "fog1" {
    name = "fog1"
    cluster = google_container_cluster.primary.id
    node_count = var.node_count

    management {
      auto_repair = true
      auto_upgrade = true
    }

    node_config {
      preemptible = true
      machine_type = "e2-standard-2"     # "e2-highcpu-4"  # 4vcpu & 4gb mem
      disk_size_gb = "40"
      disk_type    = "pd-standard"
      image_type   = "COS_CONTAINERD"

      labels = {
        role = "general"
      }

      service_account = "${var.service_account_name}@${var.gcp_project_id}.iam.gserviceaccount.com" # google_service_account.my-svc-acc.email

      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]
    }
    
    depends_on = [ google_container_cluster.primary ]
}

# node pool as fog2
resource "google_container_node_pool" "fog2" {
    name = "fog2"
    cluster = google_container_cluster.primary.id
    node_count = var.node_count

    management {
      auto_repair = true
      auto_upgrade = true
    }

    node_config {
      preemptible = true
      machine_type = "e2-standard-2"     # "e2-highcpu-4"    # 4vcpu & 4gb mem for fog nodes 
      disk_size_gb = "40"
      disk_type    = "pd-standard"
      image_type   = "COS_CONTAINERD"

      labels = {
        role = "general"
      }

      service_account = "${var.service_account_name}@${var.gcp_project_id}.iam.gserviceaccount.com" # google_service_account.my-svc-acc.email

      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]
    }
    
    depends_on = [ google_container_cluster.primary ]
}

# node pool as cloud
resource "google_container_node_pool" "cloud" {
    name = "cloud"
    cluster = google_container_cluster.primary.id
    node_count = var.node_count

    management {
      auto_repair = true
      auto_upgrade = true
    }

    node_config {
      preemptible = true
      machine_type = "e2-standard-2"       # "e2-standard-4"    # 4vcpu & 16gb memory for the cloud node
      disk_size_gb = "40"
      disk_type    = "pd-standard"
      image_type   = "COS_CONTAINERD"

      labels = {
        role = "general"
      }

      service_account = "${var.service_account_name}@${var.gcp_project_id}.iam.gserviceaccount.com" # google_service_account.my-svc-acc.email

      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]
    }
    
    depends_on = [ google_container_cluster.primary ]
}

data "google_client_config" "main" {}

# Get credentials for cluster
resource "null_resource" "gcloud-connection" {
  provisioner "local-exec" {
    command = "gcloud container clusters get-credentials thesis --zone ${var.cluster-zone[0]} --project ${var.gcp_project_id}"
  }

  depends_on = [ 
    google_container_cluster.primary,
    ]
}
