# Based on https://docs.ray.io/en/latest/cluster/kubernetes/getting-started.html

## Deploying the KubeRay operator
# This creates the KubeRay operator and all of the resources it needs.
kubectl create -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"

# Note that we must use "kubectl create" in the above command. "kubectl apply" will not work due to https://github.com/ray-project/kuberay/issues/271

# You may alternatively clone the KubeRay GitHub repo and deploy the operator's configuration from your local file system.

kubectl -n ray-system get pod --selector=app.kubernetes.io/component=kuberay-operator

# NAME                                READY   STATUS    RESTARTS   AGE
# kuberay-operator-557c6c8bcd-t9zkz   1/1     Running   0          XXs

## Deploying a Ray Cluster
# Deploy a sample Ray Cluster CR from the KubeRay repo:
kubectl apply -f https://raw.githubusercontent.com/ray-project/kuberay/master/ray-operator/config/samples/ray-cluster.autoscaler.yaml

kubectl get raycluster

# NAME                    AGE
# raycluster-autoscaler   XXs

# View the pods in the Ray cluster named "raycluster-autoscaler"
kubectl get pods --selector=ray.io/cluster=raycluster-autoscaler

# NAME                                             READY   STATUS    RESTARTS   AGE
# raycluster-autoscaler-head-xxxxx                 2/2     Running   0          XXs
# raycluster-autoscaler-worker-small-group-yyyyy   1/1     Running   0          XXs

# If you're on MacOS, first `brew install watch`.
# Run in a separate shell:
watch -n 1 kubectl get pod

## Running Applications on a Ray Cluster

kubectl get service raycluster-autoscaler-head-svc

# NAME                             TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                       AGE
# raycluster-autoscaler-head-svc   ClusterIP   10.96.114.20   <none>        6379/TCP,8265/TCP,10001/TCP   XXs

# Execute this in a separate shell.
# kubectl port-forward service/raycluster-autoscaler-head-svc 8265:8265

# The following job's logs will show the Ray cluster's total resource capacity, including 3 CPUs.

ray job submit --address http://localhost:8265 -- python -c "import ray; ray.init(); print(ray.cluster_resources())"

## Cleanup

# Delete by reference to the RayCluster custom resource
# kubectl delete raycluster raycluster-autoscaler
# kubectl get pods

# kubectl delete -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"