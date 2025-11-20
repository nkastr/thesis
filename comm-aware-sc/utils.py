import os
import time
import yaml
import re

from kubernetes import config
from kubernetes import client
from kubernetes.client.rest import ApiException
from reader import readYaml
from reader import addNodeSelector


CONTEXT = 'gke_thesis-413009_europe-west1-b_thesis' # 'k3d-edge1'

def test(node):
    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config(context=CONTEXT)
        except config.ConfigException:
            raise Exception("Could not configure kubernetes python client")
    kubectl = client.CoreV1Api()
        
    try:
        response = kubectl.list_pod_for_all_namespaces(pretty=True) # requires full node name e.g gke-thesis-cloud-090892f5-7qk0 (acquired from getNodes function)
    except ApiException as e:
        print(e)
        print("error reading node")

    # https://stackoverflow.com/questions/72504606/describe-nodes-api-call-in-kubernetes

    for i in response.items:
        for j in i.spec.containers:
            print(j.name)
            if j.resources.requests or j.resources.limits:
                # print(i.spec.node_name, j.resources.requests.get("cpu"))
                cpu = re.findall("[0-9]+", j.resources.requests.get("cpu"))[0]
                # cpu = 1 + (cpu)
    # print(response)

# test("gke-thesis-cloud-8e512aa2-w1kp")


class Utils:
    def __init__(self, namespace):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            try:
                config.load_kube_config(context=CONTEXT)
            except config.ConfigException:
                raise Exception("Could not configure kubernetes python client")

        self.namespace = namespace

    def getServices(self, ignore): # =["frontend", "frontend-external", "apache", "kubernetes", "loki", "loki-memberlist", "scheduler", "keyrock"]
        services = []
        kubectl = client.CoreV1Api()

        try:
            response = kubectl.list_namespaced_service(namespace=self.namespace, watch=False)
        except ApiException as e:
            print(e)
            print("error retrieving services")

        for i in response.items:
            service = i.metadata.name
            if service not in ignore:
                services.append(service)

        return services

    # returns service names of pods scheduled in a specific node
    def getNodeServices(self, node, ignore=["apache", "kubernetes", "loki", "loki-memberlist", "scheduler"]):
        kubectl = client.CoreV1Api()
        services = []

        try:
            response = kubectl.list_namespaced_pod(namespace="default")
        except ApiException as e:
            print(e)
            print("error getting node pods")
        
        
        for i in response.items:
            node_scheduled = i.spec.node_name
            if node_scheduled == node:
                service_name = i.metadata.name
                service_name = service_name.split("-")[0]
                if service_name not in ignore:
                    services.append(service_name)
        
        print("NODE="+node+"  SERVICES=")
        print(services)

        return services


    def getDeploy(self, ignore=["frontend", "apache"]):
        kubectl = client.AppsV1Api()
        deployments = []
        try:
            response = kubectl.list_namespaced_deployment(self.namespace)
        except ApiException as e:
            print(e)
            print("get deploy it breaks")

        try:
            for i in response.items:
                deploy = i.metadata.name
                if deploy not in ignore:
                    deployments.append(deploy)
        except TypeError as e:
            print(e)
        return deployments
    
    def getNodes(self):
        kubectl = client.CoreV1Api()
        nodes = []
        try:
            response = kubectl.list_node()
        except ApiException as e:
            print(e)
            print("get nodes error")

        for i in response.items:
            nodes.append(i.metadata.name)  
        
        return nodes
    
    def getNodeNames(self):
        kubectl = client.CoreV1Api()
        node_names = []
        try:
            response = kubectl.list_node()
        except ApiException as e:
            print(e)
            print("get nodes error")

        for i in response.items:
            node_names.append(i.metadata.labels.get("cloud.google.com/gke-nodepool"))   
        
        return node_names

    def getNodeMaxResources(self, node):
        kubectl = client.CoreV1Api()
        
        try:
            response = kubectl.read_node(node) # requires full node name e.g gke-thesis-cloud-090892f5-7qk0 (acquired from getNodes function)
        except ApiException as e:
            print(e)
            print("error reading node")
        
        allocatable = response.status.allocatable
        # capacity = response.status.capacity

        max_cpu = allocatable.get("cpu")
        max_ram = allocatable.get("memory")

        max_cpu = re.findall("[0-9]+", max_cpu)[0]
        max_ram = re.findall("[0-9]+", max_ram)[0]

        max_cpu = int(max_cpu)
        max_ram = int(max_ram) * 1024

        return max_cpu, max_ram
    
    def getNodeCurrentResources(self, node):
        kubectl = client.CoreV1Api()

        try:
            response = kubectl.list_pod_for_all_namespaces(pretty=True)
        except ApiException as e:
            print(e)
        
        total_cpu = 0
        total_ram = 0
        containers = []

        for i in response.items:
            for j in i.spec.containers:
                if i.spec.node_name == node and j.resources.requests:
                    containers.append(j.name)
                    if j.resources.requests.get("cpu"):
                        this_cpu = j.resources.requests.get("cpu")
                        this_cpu = re.findall("[0-9]+", this_cpu)[0]
                        print("ADDING CPU "+this_cpu)
                        total_cpu += int(this_cpu)
                    if j.resources.requests.get("memory"):
                        this_ram = j.resources.requests.get("memory")
                        this_ram = re.findall("[0-9]+", this_ram)[0]
                        print("ADDING RAM"+this_ram)
                        total_ram += int(this_ram)
        print("TOTALS FOR NODE")
        print(node, total_cpu, total_ram)
        print("CONTAINERS")
        print(containers)
        return total_cpu, total_ram


    def deploy(self, dep_path, name, node):
        names = []
        kubectl = client.AppsV1Api()
        # add nodeSelector to deployment file
        node_name = node.split("-")[2]
        addNodeSelector(dep_path, name, node_name)

        if "proxy" in name:
            tmp = name.split("proxy")
            name = "".join(tmp)
        body = readYaml(dep_path, name)
        try:
            for item in body[0]:
                api_response = kubectl.create_namespaced_deployment(self.namespace, item)
                names.append(item["metadata"]["name"])
        except ApiException as e:
            print(e)
            print("breaks in deploy")
        for name in names:
            self.wait_for_deployment_complete(name)
            # self.splitService(name, 0)

    def wait_for_deployment_complete(self, deployment_name):
        kubectl = client.AppsV1Api()
        stat = False

        while True:
            time.sleep(2)

            try:
                response = kubectl.read_namespaced_deployment_status(
                    deployment_name, self.namespace)
                status = response.status
                spec = response.spec
                meta = response.metadata
                stat = (status.updated_replicas == spec.replicas and status.replicas == spec.replicas
                        and status.available_replicas == spec.replicas and status.observed_generation >= meta.generation)
            except ApiException as e:
                print(e)

            if stat:
                return

    def deleteDeploy(self, name):
        self.splitService(name, 100)
        kubectl = client.AppsV1Api()
        try:
            response = kubectl.delete_namespaced_deployment(
                name, self.namespace)
            self.wait_for_deployment_deletion(name)

        except ApiException as e:
            print(e)
        try:
            response = kubectl.delete_namespaced_deployment(
                name+"proxy", self.namespace)
            self.wait_for_deployment_deletion(name+"proxy")
        except ApiException as e:
            print(e)

        try:
            response = kubectl.delete_namespaced_deployment(name.strip("proxy"), self.namespace)
            self.wait_for_deployment_deletion(name+"proxy")
        except ApiException as e:
            print(e)

    def wait_for_deployment_deletion(self, deployment_name):
        kubectl = client.AppsV1Api()

        while True:
            deploys = []
            time.sleep(2)

            try:
                deployments = kubectl.list_namespaced_deployment(
                    self.namespace)
                for i in deployments.items:
                    deploys.append(i.metadata.name)
                if deployment_name not in deploys:
                    return
                else:
                    print("Waiting for delete...")

            except ApiException as e:
                print(e)
            

    def checkEndpoint(self, svc):
        kubectl = client.CoreV1Api()
        response = None
        try:
            response = kubectl.read_namespaced_endpoints(svc, self.namespace)
        except ApiException as e:
            print(e)
        if response is None:
            return False
        if response.subsets is None:
            return False
        else:
            return True

    def updateSplits(self):
        services, _ = self.getServices()
        ts = self.getTrafficSplits()
        deploys = self.getDeploy()
        for svc in services:
            if svc not in deploys:
                if not self.checkSplit(svc):
                    self.splitService(svc, 1)


    def getPrometheus(self):

        kubectl = client.CoreV1Api()
        try:
            response = kubectl.read_namespaced_endpoints("prometheus", "istio-system")  # , "linkerd-viz" 
        except ApiException as e:
            print(e)
        return response.subsets[0].addresses[0].ip
    
    def getKiali(self):
        kubectl = client.CoreV1Api()
        try:
            response = kubectl.read_namespaced_endpoints("kiali", "istio-system")  
        except ApiException as e:
            print(e)
        return response.subsets[0].addresses[0].ip
    

