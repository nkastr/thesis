# This file configures boutique eshop on the cluster
# Specific deployments: services, deployments of frontend and database related services
# Apps Deployed: Google's Online Boutique 
# Manifests from: 
# https://github.com/GoogleCloudPlatform/microservices-demo/blob/main/release/kubernetes-manifests.yaml 

# Variable definitions
cluster_name="thesis"
cluster_location="europe-west1-b"
kubeconfig_path=~/.kube/config

project_id="thesis-413009" 
deployment_namespace=default 
deployment_path=./manifests/eshop


# Label nodes w/ their names for nodeSelector 
for node in $(kubectl get nodes -o name)  
do
    node_name=($(echo $node | tr "-" "\n"))
    node_name=${node_name[2]}
    kubectl label ${node} name=${node_name}
done

# Deploy the services (Deploy the app in the namespace the ingress gateway is deployed)
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/services

# Deploy pods for boutique
# kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/frontend.yaml
# kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/frontend2.yaml
# kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/loadgenerator1.yaml
# kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/loadgenerator2.yaml
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/redis.yaml
# kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/cartservice.yaml


# Deploy the VirtualService and DestinationRule for v1 of productcatalog
# kubectl apply -f ./canary-service/destination-vs-v1.yaml -n gateway-namespace

# Use the following command to find the ip address of the application
# kubectl get services -n ${deployment_namespace}