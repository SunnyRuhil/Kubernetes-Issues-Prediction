# agent.py
import pandas as pd
from kubernetes import client, config
import os

# Load predictions
csv_path = os.path.join(os.path.dirname(__file__), "predictions.csv")
df = pd.read_csv(csv_path)

# Load Kubernetes cluster config
try:
    config.load_kube_config()  # Use config.load_incluster_config() for inside K8s
    print("Kubernetes config loaded successfully.")
except Exception as e:
    print(f"Error loading kube config: {e}")

v1 = client.CoreV1Api()

# Check for any predicted issues
if (df["Predicted"] == 1).any():
    print("⚠️ Issue detected. Initiating pod restart...")

    pod_name = "demo-pod"      # REPLACE with real pod name
    namespace = "default"      # REPLACE with your namespace if needed

    try:
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        print(f"✅ Pod '{pod_name}' deleted. It will be restarted by deployment controller.")
    except Exception as e:
        print(f"❌ Error restarting pod: {e}")
else:
    print("✅ No issues detected.")