# Delete by reference to the RayCluster custom resource
kubectl delete raycluster raycluster-autoscaler

# Delete the KubeRay operator
kubectl delete -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"

# Delete local kind cluster
kind delete cluster
