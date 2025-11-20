# This file deploys the services of the ixen demo app on the cluster
# Apps Deployed: iXen 
# Manifests from: 
# 

# Variable definitions
deployment_namespace=default 
deployment_path=./iXenOnK8sGCPNFS


# Deploy iXen deployments
kubectl apply -n ${deployment_namespace} -f ${deployment_path}/deploymments
