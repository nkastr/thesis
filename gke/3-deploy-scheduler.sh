# Configures the custom scheduler 
# This file only changes the default scheduler and instead has k8s use our scheduler
#
# Depending on the image you choose in the spec.command.image field on the yaml file
# that will be the scheduler that is implemented
# 
# Sources:
# https://www.youtube.com/watch?v=bezQz-mIO7U&t=3s
# https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/


# Variable definitions

path_to_scheduler_config="./manifests/scheduler"
path_to_repo_credentials="docker-secret.json"
scheduler_config="scheduler.yaml"

# (!!!) Create scheduler image and upload to dockerhub before running this file

# Give rbac permissions to scheduler
kubectl apply -f ${path_to_scheduler_config}/scheduler-rbac.yaml 

# Wait for permissions to be created
# sleep 5

# Create secret to give kuberentes access to the repo
kubectl create secret generic regcred --from-file=.dockerconfigjson=${path_to_repo_credentials} --type=kubernetes.io/dockerconfigjson

# Create the scheduler deployment
kubectl apply -f ${path_to_scheduler_config}/${scheduler_config} 


# Verify that the scheduler pod is running (optional)
# kubectl get pods --namespace=default


# For pods to be scheduled by my-scheduler instead of the default one
# we have to add the field spec.schedulerName and the value my-scheduler 
# to each pod
