#!/bin/bash

# 🗑️  Kubernetes Cleanup Script for AI-Powered DevOps Pipeline

set -e

RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}⚠️  Warning: This will delete the entire AI DevOps Pipeline deployment${NC}"
echo -e "${YELLOW}All data will be lost!${NC}\n"

read -p "Are you sure you want to continue? (yes/no): " -r
echo

if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo -e "${RED}🗑️  Deleting AI-Powered DevOps Pipeline...${NC}\n"

# Delete in reverse order
kubectl delete -f ingress.yaml --ignore-not-found=true
kubectl delete -f frontend.yaml --ignore-not-found=true
kubectl delete -f backend.yaml --ignore-not-found=true
kubectl delete -f database.yaml --ignore-not-found=true
kubectl delete -f secret.yaml --ignore-not-found=true
kubectl delete -f configmap.yaml --ignore-not-found=true
kubectl delete -f namespace.yaml --ignore-not-found=true

echo -e "\n${YELLOW}✅ Cleanup complete!${NC}"