ray job submit --address http://localhost:8265 -- python -c "import ray; ray.init(); print(ray.cluster_resources())"

export RAY_ADDRESS="http://127.0.0.1:8265"
ray job submit --working-dir . -- python script.py
