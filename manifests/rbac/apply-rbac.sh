#!/bin/bash

# RBAC Deployment Script for KinD Cluster
# This script applies all RBAC configurations to your Kubernetes cluster

set -e

echo "🔐 Starting RBAC Setup..."

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Create namespaces
echo -e "${BLUE}1. Creating namespaces...${NC}"
kubectl apply -f namespaces.yaml
echo -e "${GREEN}✓ Namespaces created${NC}\n"

# 2. Create Admin Role
echo -e "${BLUE}2. Creating Admin role...${NC}"
kubectl apply -f admin-role.yaml
echo -e "${GREEN}✓ Admin role created${NC}\n"

# 3. Create Developer Role
echo -e "${BLUE}3. Creating Developer role...${NC}"
kubectl apply -f developer-role.yaml
echo -e "${GREEN}✓ Developer role created${NC}\n"

# 4. Create Read-Only Role
echo -e "${BLUE}4. Creating Read-Only role...${NC}"
kubectl apply -f readonly-role.yaml
echo -e "${GREEN}✓ Read-Only role created${NC}\n"

# 5. Create Service Accounts
echo -e "${BLUE}5. Creating Service Accounts...${NC}"
kubectl apply -f service-accounts.yaml
echo -e "${GREEN}✓ Service accounts created${NC}\n"

# 6. Create Role Bindings
echo -e "${BLUE}6. Creating Role Bindings...${NC}"
kubectl apply -f role-bindings.yaml
echo -e "${GREEN}✓ Role bindings created${NC}\n"

echo -e "${GREEN}✅ RBAC setup complete!${NC}\n"

# Display created resources
echo "📋 Verifying created resources:"
echo -e "${BLUE}ClusterRoles:${NC}"
kubectl get clusterroles | grep -E "admin-role"

echo -e "\n${BLUE}Roles:${NC}"
kubectl get roles -A | grep -E "developer-role|read-only-role"

echo -e "\n${BLUE}ServiceAccounts:${NC}"
kubectl get serviceaccounts -A | grep -E "admin-user|developer-user|readonly-user"

echo -e "\n${BLUE}RoleBindings:${NC}"
kubectl get rolebindings -A | grep -E "binding"

echo -e "\n${GREEN}🎉 All RBAC configurations applied successfully!${NC}"
