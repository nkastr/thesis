# This file checks on which node each service was placed
# Apps Deployed: Google's Online Boutique 


kubectl get pods -n default -o wide





# 
# Check for CrashLoopBackOff/debug pods in general
# https://sysdig.com/blog/debug-kubernetes-crashloopbackoff/
# 
# kubectl logs <mypod> --all-containers
# kubectl get pod <mypod>
# 