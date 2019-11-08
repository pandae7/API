from kubernetes import config, client
import kubernetes.client
import requests, json
config.load_kube_config()
configuration = kubernetes.client.Configuration()


api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
y = api_instance.list_service_for_all_namespaces(label_selector='app=e0ef407d89d9459ea30d71b9112cfe4e' )
entry = y.items[0]
print(entry.spec.ports[0].node_port)
