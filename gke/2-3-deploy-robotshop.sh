# This file configures robot shop on the cluster
# Specific deployments: services, storages, deployments of frontend and database related services
# Apps Deployed: Stan's Robot Shop 
# Manifests from: 
# https://github.com/konveyor/mig-demo-apps/tree/master/apps/robot-shop/manifests
# Robot Shop main github page:
# https://github.com/instana/robot-shop

# Variable definitions
cluster_name="thesis"
cluster_location="europe-west1-b"
kubeconfig_path=~/.kube/config

project_id="thesis-413009" 
deployment_namespace=default 
deployment_path=./manifests/robot-shop


# Label nodes w/ their names for nodeSelector (done in eshop deployment)
# for node in $(kubectl get nodes -o name)  
# do
#     node_name=($(echo $node | tr "-" "\n"))
#     node_name=${node_name[2]}
#     kubectl label ${node} name=${node_name}
# done

# Deploy the storages (& others)
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/storages
# kubectl apply -n ${deployment_namespace} -f ${deployment_path}/other

# Deploy the services
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/services

# Deploy pods
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/web1.yaml
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/web2.yaml
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/mysql.yaml
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/mongodb.yaml
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/redis.yaml
