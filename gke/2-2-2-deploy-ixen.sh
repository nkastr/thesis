# This file deploys the services of the ixen demo app on the cluster
# Apps Deployed: iXen 
# Manifests from: 
# 

# Before running this script, change the keyrock secret variable "host" into the correct base64 encoded ip (cluster ip)
# https://www.base64encode.org/

# Variable definitions
deployment_namespace=default 
deployment_path=./iXenOnK8sGCPNFS


# Deploy iXen services
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/services

# Deploy storages and stateful sets for ixen
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/storages
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/statefulsets

# Deploy keyrock secrets
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/secrets/keyrock-secret.yml
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/secrets/mysql-secret.yml

# Deploy keyrock
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deployments/keyrock.yml

# Deploy frontend
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/frontend/apache.yaml
# kubectl apply -n ${deployment_namespace} -f ${deployment_path}/frontend/apache2.yaml

# After deploying these elements, connect to keyrock and create an application in it

# kubectl apply -n ${deployment_namespace} -f iXenOnK8sGCPNFS/secrets

