## Creating cluster
# Start local kind cluster
kind create cluster

# Set kubectl context
kubectl cluster-info --context kind-kind

## Deploying the KubeRay operator
# This creates the KubeRay operator and all of the resources it needs.
kubectl create -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"
# Note that we must use "kubectl create" in the above command. "kubectl apply" will not work due to https://github.com/ray-project/kuberay/issues/271
# You may alternatively clone the KubeRay GitHub repo and deploy the operator's configuration from your local file system.

# Confirm that the operator is running in the namespace ray-system
kubectl -n ray-system get pod --selector=app.kubernetes.io/component=kuberay-operator

## Deploying a Ray Cluster
# Deploy a sample Ray Cluster CR from the KubeRay repo:
kubectl apply -f https://raw.githubusercontent.com/ray-project/kuberay/master/ray-operator/config/samples/ray-cluster.autoscaler.yaml
# This Ray cluster is named `raycluster-autoscaler` because it has optional Ray Autoscaler support enabled.

# View RayCluster CR
kubectl get raycluster

# The KubeRay operator will detect the RayCluster object.
# The operator will then start your Ray cluster by creating head and worker pods. To view Ray cluster’s pods, run the following command:
kubectl get pods --selector=ray.io/cluster=raycluster-autoscaler

## Setup for job submission
# Identify the Ray head service for our example cluster
kubectl get service raycluster-autoscaler-head-svc

# Forward port
kubectl port-forward service/raycluster-autoscaler-head-svc 8265:8265