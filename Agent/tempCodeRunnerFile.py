import pandas as pd
from kubernetes import client, config
import os

# Load predictions
csv_path = os.path.join(os.path.dirname(__file__), "predictions.csv")
df = pd.read_csv(csv_path)

# Load Kubernetes config (assumes you have kubectl configured)
try:
    config.load_kube_config()
    print("✅ Kubernetes config loaded.")
except Exception as e:
    print(f"❌ Could not load config: {e}")

v1 = client.CoreV1Api()

# Check for issues
if (df["Predicted"] == 1).any():
    print("⚠️ Issue detected — restarting pod...")

    pod_name = "your-pod-name"  # Replace with your real pod name
    namespace = "default"

    try:
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        print(f"✅ Pod '{pod_name}' deleted and will auto-restart.")
    except Exception as e:
        print(f"❌ Error restarting pod: {e}")
else:
    print("✅ No issue detected.")
