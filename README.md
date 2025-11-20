# Thesis: Dynamic Microservices Placement Strategies in Kubernetes

In short, this project includes
- Setup of a K8s cluster in GCP, using Terraform and shell, including Istio service mesh, Prometheus and more
- Deployment a new K8s Scheduler that makes placement decisions of microservices based on communication between them
- Deployment of Google's eShop demo app for testing
- Deployment of locust load testing app for experimentation

To run (note: for all scripts, change variables accordingly and follow the file's instructions when unsure)
- Run terraform in /terraform_files to create the cluster
- Run shell scripts in /gke in the order they are written (0-, 1-, 2-,3-)
  - 0 creates Scheduler image in your Dockerhub (run once)
  - 1 deploys Istio service mesh to the cluster
  - 2 deploys frontend service and redis service/db to the cluster
  - 3 deploys new scheduler (the new scheduler will then schedule all the other services accordingly)
- Wait until Scheduler places all services (may take a few minutes)
  - Use "check-deployed.sh" in /experiments folder
- Run "run-locust.sh" in /experiments folder to test the application latency
  - define the locust experiment using the "file" variable

To see the results, use locust's GUI in your browser.
