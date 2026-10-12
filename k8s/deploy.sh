#!/bin/bash

# 🚀 Kubernetes Deployment Script for AI-Powered DevOps Pipeline
# This script deploys the entire application to a Kubernetes cluster

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}☸️  AI-Powered DevOps Pipeline - Kubernetes Deployment${NC}"
echo -e "${BLUE}========================================================${NC}\n"

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed. Please install kubectl first.${NC}"
    echo -e "   Install: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

echo -e "${GREEN}✅ kubectl found${NC}"

# Check kubectl connection
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Cannot connect to Kubernetes cluster${NC}"
    echo -e "   Make sure you have a cluster running and kubectl is configured"
    exit 1
fi

echo -e "${GREEN}✅ Connected to Kubernetes cluster${NC}\n"

# Show cluster info
echo -e "${BLUE}📊 Cluster Information:${NC}"
kubectl cluster-info | grep -E "Kubernetes|running"
echo ""

# Step 1: Create Namespace
echo -e "${YELLOW}📦 Step 1: Creating namespace...${NC}"
kubectl apply -f namespace.yaml
echo -e "${GREEN}✅ Namespace created${NC}\n"

# Step 2: Create ConfigMap
echo -e "${YELLOW}⚙️  Step 2: Creating ConfigMap...${NC}"
kubectl apply -f configmap.yaml
echo -e "${GREEN}✅ ConfigMap created${NC}\n"

# Step 3: Create Secrets
echo -e "${YELLOW}🔐 Step 3: Creating Secrets...${NC}"
kubectl apply -f secret.yaml
echo -e "${GREEN}✅ Secrets created${NC}\n"

# Step 4: Deploy Database
echo -e "${YELLOW}🗄️  Step 4: Deploying PostgreSQL Database...${NC}"
kubectl apply -f database.yaml
echo -e "${GREEN}✅ Database deployment created${NC}"
echo -e "${BLUE}⏳ Waiting for database to be ready...${NC}"
kubectl wait --for=condition=ready pod -l component=database -n ai-devops --timeout=120s || true
echo ""

# Step 5: Deploy Backend
echo -e "${YELLOW}🚀 Step 5: Deploying Backend (FastAPI + AI)...${NC}"
kubectl apply -f backend.yaml
echo -e "${GREEN}✅ Backend deployment created${NC}"
echo -e "${BLUE}⏳ Waiting for backend to be ready...${NC}"
kubectl wait --for=condition=ready pod -l component=backend -n ai-devops --timeout=180s || true
echo ""

# Step 6: Deploy Frontend
echo -e "${YELLOW}🎨 Step 6: Deploying Frontend (React)...${NC}"
kubectl apply -f frontend.yaml
echo -e "${GREEN}✅ Frontend deployment created${NC}"
echo -e "${BLUE}⏳ Waiting for frontend to be ready...${NC}"
kubectl wait --for=condition=ready pod -l component=frontend -n ai-devops --timeout=120s || true
echo ""

# Step 7: Create Ingress
echo -e "${YELLOW}🌐 Step 7: Creating Ingress...${NC}"
kubectl apply -f ingress.yaml
echo -e "${GREEN}✅ Ingress created${NC}\n"

# Show deployment status
echo -e "${BLUE}========================================================${NC}"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${BLUE}========================================================${NC}\n"

echo -e "${BLUE}📊 Deployment Status:${NC}"
kubectl get all -n ai-devops
echo ""

echo -e "${BLUE}🔍 Pod Details:${NC}"
kubectl get pods -n ai-devops -o wide
echo ""

echo -e "${BLUE}📡 Services:${NC}"
kubectl get services -n ai-devops
echo ""

echo -e "${BLUE}🌐 Ingress:${NC}"
kubectl get ingress -n ai-devops
echo ""

# Get external IP/URL
echo -e "${YELLOW}🔗 Access Information:${NC}"
INGRESS_IP=$(kubectl get ingress ai-devops-ingress -n ai-devops -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")
INGRESS_HOST=$(kubectl get ingress ai-devops-ingress -n ai-devops -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || echo "")

if [ "$INGRESS_IP" != "pending" ] && [ -n "$INGRESS_IP" ]; then
    echo -e "   Frontend: ${GREEN}http://${INGRESS_IP}${NC}"
    echo -e "   Backend API: ${GREEN}http://${INGRESS_IP}/api${NC}"
    echo -e "   API Docs: ${GREEN}http://${INGRESS_IP}/docs${NC}"
elif [ -n "$INGRESS_HOST" ]; then
    echo -e "   Frontend: ${GREEN}http://${INGRESS_HOST}${NC}"
    echo -e "   Backend API: ${GREEN}http://${INGRESS_HOST}/api${NC}"
    echo -e "   API Docs: ${GREEN}http://${INGRESS_HOST}/docs${NC}"
else
    echo -e "   ${YELLOW}Ingress IP is pending. Run this to check:${NC}"
    echo -e "   kubectl get ingress -n ai-devops -w"
fi
echo ""

# Port forwarding option
echo -e "${YELLOW}💡 For local testing, use port forwarding:${NC}"
echo -e "   Frontend:  kubectl port-forward -n ai-devops svc/ai-devops-frontend-service 3000:3000"
echo -e "   Backend:   kubectl port-forward -n ai-devops svc/ai-devops-backend-service 8000:8000"
echo ""

# Useful commands
echo -e "${YELLOW}📝 Useful Commands:${NC}"
echo -e "   View logs (backend):  kubectl logs -f -l component=backend -n ai-devops"
echo -e "   View logs (frontend): kubectl logs -f -l component=frontend -n ai-devops"
echo -e "   Scale backend:        kubectl scale deployment ai-devops-backend --replicas=5 -n ai-devops"
echo -e "   Describe pod:         kubectl describe pod <pod-name> -n ai-devops"
echo -e "   Execute in pod:       kubectl exec -it <pod-name> -n ai-devops -- bash"
echo -e "   Delete deployment:    kubectl delete namespace ai-devops"
echo ""

echo -e "${GREEN}✨ Your AI-Powered DevOps Pipeline is now running on Kubernetes!${NC}"
echo -e "${BLUE}🚀 Production-grade deployment with auto-scaling and self-healing!${NC}\n"