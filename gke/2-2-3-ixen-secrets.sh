# This file deploys iXen secrets
# Run after following the necessary steps
# Create an application in keyrock using edge node ip address
# 

# Variable definitions
deployment_namespace=default 
deployment_path=./iXenOnK8sGCPNFS

# Deploy secrets
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/secrets
