from prometheus_api_client import PrometheusConnect

# GLOBAL VARS
PROMETHEUS = "localhost"  # if u use istioctl dashboard prometheus

def main():
    prometheus_url = "http://" + PROMETHEUS + ":9090"
    prom = PrometheusConnect(prometheus_url, disable_ssl=True)


    query = ""
    response = prom.custom_query(query)

    query_egress = "sum(istio_requests_total{source_app=~\"" + svc1 + "\", destination_service_name=~\"" + svc2 + "\"}) by (source_app, destination_service_name, request_protocol)"



if __name__ == "__main__":
    main()