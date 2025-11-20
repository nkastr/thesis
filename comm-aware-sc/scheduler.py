from math import ceil
import os
import time
from reader import getDeploymentResources
from utils import Utils
from metrics import Metrics

NAMESPACE = os.environ["target_namespace"]
CPU_PERCENTAGE = (float(os.environ["cpu_percentage"]))
RAM_PERCENTAGE = (float(os.environ["ram_percentage"]))
WEIGHT_A = int(float(os.environ["weight_a"]))
WEIGHT_B = int(float(os.environ["weight_b"]))
WEIGHT_C = int(float(os.environ["weight_c"]))


PERIOD = "30s"
YAMLPATH = "./manifests/robot-and-eshop/deployments/" # "manifests/deployments"
IGNORE = ["frontend", "frontend-external", "mongo", "mongo-statefulset", "mysql", "apache", "keyrock", "loki", "loki-memberlist", "scheduler", "kubernetes"]
MIBTOBYTE = 1048576



class Scheduler:
    def __init__(self, period, deletion_period, namespace, max_cpu_percentage, max_ram_percentage, deployment_path, weight_a, weight_b, weight_c):
        self.period = period
        self.deletion_period = deletion_period
        self.namespace = namespace
        # useless ?
        # self.total_ram = total_ram
        # self.total_cpu = total_cpu
        self.max_cpu_percentage = max_cpu_percentage
        self.max_ram_percentage = max_ram_percentage
        self.requests = dict()
        self.limits = dict()
        # 
        self.deployment_path = deployment_path
        self.utilsObj = None
        self.metricsObj = None
        self.ignore = IGNORE
        self.weight_a = weight_a
        self.weight_b = weight_b
        self.weight_c = weight_c

    def initConnect(self):
        self.utilsObj = Utils(self.namespace)
        prom_ip = self.utilsObj.getPrometheus()
        kiali_ip = self.utilsObj.getKiali()
        self.metricsObj = Metrics(prom_ip, kiali_ip, self.namespace, self.period, self.deletion_period)
        # self.metricsObj.initMachineData()
        # self.requests, self.limits = getResources(self.deployment_path)
        
    def availableResources(self, service, node):
        current_cpu, current_ram = self.utilsObj.getNodeCurrentResources(node) # self.metricsObj.getNodeUsedResources(node)
        max_cpu, max_ram = self.utilsObj.getNodeMaxResources(node)
        
        print(current_cpu, current_ram, max_cpu, max_ram)

        available_cpu = max_cpu * self.max_cpu_percentage - current_cpu
        available_ram = max_ram * self.max_ram_percentage - current_ram
        requests, limits = getDeploymentResources(self.deployment_path, service)
        required_cpu = float(requests[service]["cpu"])
        required_ram = float(requests[service]["memory"]) * MIBTOBYTE

        print(service, node, available_cpu, required_cpu, available_ram, required_ram)

        if available_cpu > required_cpu and available_ram > required_ram:
            return True
        else: 
            return False

    def filterNodes(self, service, nodes):
        filtered = []

        for node in nodes:
            if self.availableResources(service, node):
                filtered.append(node)

        return filtered
        
    def commAwareDeploy(self, svc, filtered_nodes, all_nodes, services):
        top_score = 0
        top_node = None
        for node in filtered_nodes:
            score = self.scoreNode(svc, node, all_nodes)
            if score > top_score:
                top_node = node
                top_score = score
        if top_node is not None and top_score != 0:
            services.remove(svc)
            self.utilsObj.deploy(self.deployment_path, svc, top_node)
            


    def scoreNode(self, svc, node, all_nodes):
        score = 0
        for cn in all_nodes:
            pScore = 0
            services = self.utilsObj.getNodeServices(cn) # get services of pods scheduled on node cn
            for service in services:
                channel = self.metricsObj.getChannel(svc, service)
                # print("CHANNEL:")
                # print(channel)
                channel_prio = self.getPriority(channel.get("request_protocol"))
                static_contr = self.weight_a * channel_prio
                channel_traffic = channel.get("requests")
                dynamic_contr = self.weight_b * channel_traffic
                pScore = pScore + static_contr + dynamic_contr
            if cn == node:
                score = score + self.weight_c * pScore
            else:
                # node_latency = self.metricsObj.getNodeLatency(node, cn)
                weight_d = 1/50 # latency in ms (20 - 50)
                score = score + weight_d * pScore

        return score

    def getPriority(self, protocol):
        if protocol == "http":
            return 100
        elif protocol == "grpc":
            return 50
        elif protocol == "tcp":
            return 25
        else:
            return 0
        # more can be added for different protocols
            
        
    def schedule(self):
        cluster_nodes = self.utilsObj.getNodes()
        services = self.utilsObj.getServices(self.ignore)
        # node_latencies = self.metricsObj.getNodeLatency()

        while(services):
            for svc in services:
                filtered_nodes = self.filterNodes(svc, cluster_nodes)
                self.commAwareDeploy(svc, filtered_nodes, cluster_nodes, services)
                # time.sleep(0.2)


def main():
    sc = Scheduler(PERIOD, PERIOD, NAMESPACE, CPU_PERCENTAGE, RAM_PERCENTAGE, YAMLPATH, int(WEIGHT_A), int(WEIGHT_B), int(WEIGHT_C))
    sc.initConnect()
    sc.schedule()


if __name__ == '__main__':
    main()


### Scheduler structure
    # Connect w/ Cluster, Prometheus, Kiali APIs 
        # cluster - utils object 
        # prometheus & kiali - metrics object
    
    # Deploy frontend services in edge nodes            (can be done from scripts)
    # Deploy database & server services in cloud node   (can be done from scripts)

    # Get all needed inputs: cluster_nodes, cluster_services, channels, latencies
        # cluster_nodes & cluster_services - from utils object
        # channels & latencies - from metrics object
            # Metrics object functions:
            # 1 - traffic between all services ()
    # For each pod calculate the score of each node using the algorithm
        # Get all algorithm inputs: pod/service, node, cluster_nodes, channels, latencies
        # Score the nodes w/ comm aware
        # Place pod in highest scored node 