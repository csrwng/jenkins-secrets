import os
from oc_requester import OpenShiftRequester
from jenkinsapi.jenkins import Jenkins 
import kubernetes.client

def connect_to_jenkins():
    url = os.environ.get("JENKINS_SERVICE_URL", "http://jenkins")
    r = OpenShiftRequester(url)
    j = Jenkins(baseurl=url, requester=r)
    return j

def connect_to_kube_core():
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as token_file:
        api_token = token_file.read()
    ca_crt = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'

    kubernetes.client.configuration.api_key['authorization'] = api_token
    kubernetes.client.configuration.api_key_prefix['authorization'] = "Bearer"
    kubernetes.client.configuration.ssl_ca_cert = ca_crt
    kubernetes.client.configuration.host = 'https://kubernetes.default.svc'

    core_instance = kubernetes.client.CoreV1Api()
    return core_instance