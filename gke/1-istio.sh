# Configuring Istio on the cluster
# Steps from:
# https://istio.io/latest/docs/setup/getting-started/
#
# chmod u+rx FILE_NAME to give necessary permissions to the file (and all .sh files)
# 
# Variable definitions
nodes=5
node_names=("edge1" "edge2" "fog1" "fog2" "cloud")
cluster_locations=("europe-west1-b")
kubeconfig_path=~/.kube/config

project_id="thesis-413009"
project_number="672991466356"

# namespace where application will be deployed
namespace="default" 


# Download Istio
# curl -L https://istio.io/downloadIstio | sh -

# Add istioctl client binary to your path
export PATH=$PWD/istio-1.20.3/bin:$PATH

# Install Istio
istioctl install

# Enable automatic proxy injection (optional?)
kubectl label namespace ${namespace} istio-injection=enabled

# Source:
# https://medium.com/@vishal1909/setup-istio-on-gke-and-visualize-using-kiali-part-1-d542fa8da921

# Enable telemetry services (Grafana, Prometheus, Jaeger, Kiali, Loki)
kubectl apply -f ./istio-1.20.3/samples/addons

# Check 
# kubectl rollout status deployment/kiali -n istio-system
