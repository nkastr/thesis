from prometheus_api_client import PrometheusConnect
# from kiali import KialiClient

GBTOBYTE = 1073741824

# https://pypi.org/project/prometheus-api-client/
def testQuery(input):
    # test_url = "http://demo.robustperception.io:9090/"
    test_url = "http://localhost:9090/"
    prom = PrometheusConnect(test_url, disable_ssl=True)

    # query = "alertmanager_alerts{job = \"" + input + "\"}"
    svc2 = "cartservice"
    svc1 = "redis-cart"
    query = "sum(istio_tcp_sent_bytes_total{source_app=~\"" + svc2 + "\", destination_service_name=~\"" + svc1 + "\"}) by (source_app, destination_service_name, request_protocol)"

    response = prom.custom_query(query)
    response = response[0]
    metric = response.get("metric")
    value = response.get("value")[1]
    print(metric)
    print(value)

# testQuery("alertmanager")

class Metrics:
    def __init__(self, prom_ip, kiali_ip, namespace, period, deletion_period): # , total_cpu, total_ram):

        self.prometheus_url = "http://" + prom_ip + ":9090"
        self.prom = PrometheusConnect(url=self.prometheus_url, disable_ssl=True)
       
        # maybe needed
        # self.kiali_url = "http://" + kiali_ip + ":20001"
        # self.kiali = KialiClient(host=self.kiali_url, username="admin", password="admin")

        self.period = period
        self.deletion_period = deletion_period

        self.namespace = namespace
        # self.cluster_total_cpu = total_cpu
        # self.cluster_total_ram = total_ram * GBTOBYTE

    def getTraffic(self):
        channels = []
        query = "sum(istio_requests_total) by (source_app, destination_service_name, request_protocol)"

        traffic = self.prom.custom_query(query)

        for item in traffic:
            metric = item.get("metric")
            source_app = metric.get("source_app")
            destination_service = metric.get("destination_service_name")
            protocol = metric.get("request_protocol")
            requests = int(float(item.get("value")[1]))
            channel = {
                "source_app": source_app,
                "destination_service": destination_service,
                "request_protocol": protocol,
                "requests": requests 
            }
            channels.append(channel)

        return channels
    
    # Request found from: https://kiali.io/docs/faq/graph/  (how kiali gets traffic from prometheus)
    def getChannel(self, svc1, svc2):
        query_egress = "sum(istio_requests_total{source_app=~\"" + svc1 + "\", destination_service_name=~\"" + svc2 + "\"}) by (source_app, destination_service_name, request_protocol)"
        query_ingress = "sum(istio_requests_total{source_app=~\"" + svc2 + "\", destination_service_name=~\"" + svc1 + "\"}) by (source_app, destination_service_name, request_protocol)"

        # add - istio_tcp_sent_bytes_total - for tcp traffic
        tcp_egress = "sum(istio_tcp_sent_bytes_total{source_app=~\"" + svc1 + "\", destination_service_name=~\"" + svc2 + "\"}) by (source_app, destination_service_name, request_protocol)"
        tcp_ingress = "sum(istio_tcp_sent_bytes_total{source_app=~\"" + svc2 + "\", destination_service_name=~\"" + svc1 + "\"}) by (source_app, destination_service_name, request_protocol)"

        traffic_egress = self.prom.custom_query(query_egress)
        traffic_ingress = self.prom.custom_query(query_ingress)     
        print("PROMETHEUS EGRESS SVC1="+svc1+"  SVC2="+svc2)
        print(traffic_egress)
        print(traffic_ingress)
        traffic_tcp_egress = self.prom.custom_query(tcp_egress)
        traffic_tcp_ingress = self.prom.custom_query(tcp_ingress)

        channel = {
            "service1": svc1,
            "service2": svc2,
            "requests": 0,
            "request_protocol": "N/A"
        }

        if traffic_egress:
            traffic_egress = traffic_egress[0]
            print("TRAFFIC EGRESS")
            print(traffic_egress)
            metric = traffic_egress.get("metric")
            print("METRIC")
            print(metric)
            print("VALUE")
            print(traffic_egress.get("value")[1])
            channel["requests"] += int(float(traffic_egress.get("value")[1]))
            channel["request_protocol"] = metric.get("request_protocol")
        
        if traffic_ingress:
            traffic_ingress = traffic_ingress[0]
            print("TRAFFIC INGRESS")
            print(traffic_ingress)
            metric = traffic_ingress.get("metric")
            channel["requests"] += int(float(traffic_ingress.get("value")[1]))
            channel["request_protocol"] = metric.get("request_protocol")

        if traffic_tcp_egress:
            traffic_tcp_egress = traffic_tcp_egress[0]
            metric = traffic_tcp_egress.get("metric")
            channel["requests"] += int(float(traffic_tcp_egress.get("value")[1]))
            channel["request_protocol"] = metric.get("request_protocol")

        if traffic_tcp_ingress:
            traffic_tcp_ingress = traffic_tcp_ingress[0]
            metric = traffic_tcp_ingress.get("metric")
            channel["requests"] += int(float(traffic_tcp_ingress.get("value")[1]))
            channel["request_protocol"] = metric.get("request_protocol")

        return channel

    # def checkDeletion(self, svc):

    #     request_query_deletion = "sum(increase(request_total{namespace=~\"" + self.namespace + \
    #         "\", deployment=~\".*\", dst_target_cluster=\"\", dst_service=\"" + \
    #         svc + "\"}[" + self.deletion_period + "])) by (dst_service)"
    #     linkerd_g_request_deletion = "sum(increase(request_total{deployment=~\"linkerd-gateway\",  dst_target_cluster=\"\", dst_service=\"" + \
    #         svc + "\"}[" + self.deletion_period + "])) by (dst_service )"

    #     deletion_1 = self.prom.custom_query(request_query_deletion)
    #     deletion_2 = self.prom.custom_query(linkerd_g_request_deletion)
    #     tmp = 0

    #     for item in deletion_1 + deletion_2:
    #         if item.get("value"):
    #             if item.get("value")[1]:
    #                 tmp += int(float(item["value"][1]))

    #     return tmp

    def getNodeUsedResources(self, node):
        node_name = node.split("-")[2]
        cpu_query = "sum(container_cpu_usage_seconds_total{cloud_google_com_gke_nodepool=\"" + node_name + "\"}) by (cloud_google_com_gke_nodepool)"
        # "sum(rate(container_cpu_usage_seconds_total{cloud_google_com_gke_nodepool=" + node + "}[30s])) by (cloud_google_com_gke_nodepool)" w/ rate 
        ram_query = "sum(container_memory_working_set_bytes{cloud_google_com_gke_nodepool=\"" + node_name + "\"}) by (cloud_google_com_gke_nodepool)"

        cpu_response = self.prom.custom_query(cpu_query)
        ram_response = self.prom.custom_query(ram_query)

        try:
            cpu = float(cpu_response[0].get("value")[1])
            ram = float(ram_response[0].get("value")[1])
            print("RAM NODE="+node_name)
            print(ram)
            print("CPU NODE="+node_name)
            print(cpu)
        except IndexError as e:
            cpu = 0
            ram = 0

        return cpu, ram

    # def getMachineData(self):
    #     query = "sum(rate(container_cpu_usage_seconds_total{id=\"/\"}[" + self.period + "]))"
    #     metrics = self.prom.custom_query(query)
    #     cpu_usage = 0.0
    #     memory_usage_bytes = 0.0
    #     for item in metrics:
    #         cpu_usage = float(item["value"][1]) * 1000

    #     query = "sum(rate(container_cpu_usage_seconds_total{id=\"/\"}[" + self.period + "]))"
    #     metrics = self.prom.custom_query(query)
    #     cpu_percentage = 0.0
    #     memory_usage_bytes = 0.0
    #     for item in metrics:
    #         cpu_percentage = (
    #             float(item["value"][1]) / self.cluster_total_cpu) * 100

    #     query = "sum(container_memory_working_set_bytes{id=\"/\"})"
    #     metrics = self.prom.custom_query(query)
    #     for item in metrics:
    #         memory_usage_bytes = float(item["value"][1])

    #     memory_percentage = (memory_usage_bytes / self.cluster_total_ram) * 100

    #     return cpu_usage, memory_usage_bytes, cpu_percentage, memory_percentage

