# ☸️ Kubernetes Configuration Files

This directory contains all Kubernetes manifests for deploying the AI-Powered DevOps Pipeline to a production Kubernetes cluster.

## 📁 Files Overview:

| File | Description |
|------|-------------|
| `namespace.yaml` | Creates the `ai-devops` namespace for resource isolation |
| `configmap.yaml` | Application configuration (non-sensitive) |
| `secret.yaml` | Sensitive data (passwords, tokens, keys) |
| `database.yaml` | PostgreSQL database deployment + service + PVC |
| `backend.yaml` | FastAPI backend deployment + service + HPA |
| `frontend.yaml` | React frontend deployment + service + HPA |
| `ingress.yaml` | Ingress for external traffic routing |
| `deploy.sh` | Automated deployment script |
| `undeploy.sh` | Cleanup script |

## 🚀 Quick Deploy:

```bash
# Make sure kubectl is configured
kubectl cluster-info

# Deploy everything
./deploy.sh

# Cleanup
./undeploy.sh
```

## 📊 Resources Created:

- **1 Namespace**: ai-devops
- **1 ConfigMap**: Application configuration  
- **1 Secret**: Sensitive credentials
- **3 Deployments**: Database, Backend, Frontend
- **3 Services**: Internal cluster networking
- **2 HPAs**: Auto-scaling for Backend and Frontend
- **1 Ingress**: External access routing
- **1 PVC**: Persistent storage for database

## 🔧 Customization:

### Update Docker Images:
Edit deployment files and change:
```yaml
image: ai-devops-backend:latest
```
to your registry:
```yaml
image: your-registry.com/ai-devops-backend:v2.0.0
```

### Change Resource Limits:
Edit `backend.yaml` or `frontend.yaml`:
```yaml
resources:
  requests:
    memory: "512Mi"  # Change as needed
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

### Adjust Auto-Scaling:
Edit HPA sections:
```yaml
minReplicas: 2    # Minimum pods
maxReplicas: 10   # Maximum pods
```

## 📚 More Information:

See [KUBERNETES_DEPLOYMENT.md](../KUBERNETES_DEPLOYMENT.md) for detailed instructions.