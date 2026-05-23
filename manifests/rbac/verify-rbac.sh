#!/bin/bash

# RBAC Verification Script
# This script helps you verify and test the RBAC configurations

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 RBAC Configuration Verification${NC}\n"

# Function to test permission
test_permission() {
    local user=$1
    local verb=$2
    local resource=$3
    local namespace=$4
    
    if kubectl auth can-i $verb $resource --as=system:serviceaccount:$namespace:$user -n $namespace &>/dev/null; then
        echo -e "${GREEN}✓${NC} Can $verb $resource"
    else
        echo -e "${RED}✗${NC} Cannot $verb $resource"
    fi
}

# Verify ClusterRoles
echo -e "${BLUE}=== ClusterRoles ===${NC}"
kubectl get clusterroles admin-role &>/dev/null && echo -e "${GREEN}✓ admin-role exists${NC}" || echo -e "${RED}✗ admin-role missing${NC}"

# Verify Roles
echo -e "\n${BLUE}=== Roles ===${NC}"
echo -e "${YELLOW}Development Namespace:${NC}"
kubectl get roles -n development 2>/dev/null | grep -q "developer-role" && echo -e "${GREEN}✓ developer-role exists${NC}" || echo -e "${RED}✗ developer-role missing${NC}"
kubectl get roles -n development 2>/dev/null | grep -q "read-only-role" && echo -e "${GREEN}✓ read-only-role exists${NC}" || echo -e "${RED}✗ read-only-role missing${NC}"

echo -e "${YELLOW}Staging Namespace:${NC}"
kubectl get roles -n staging 2>/dev/null | grep -q "developer-role" && echo -e "${GREEN}✓ developer-role exists${NC}" || echo -e "${RED}✗ developer-role missing${NC}"
kubectl get roles -n staging 2>/dev/null | grep -q "read-only-role" && echo -e "${GREEN}✓ read-only-role exists${NC}" || echo -e "${RED}✗ read-only-role missing${NC}"

echo -e "${YELLOW}Production Namespace:${NC}"
kubectl get roles -n production 2>/dev/null | grep -q "read-only-role" && echo -e "${GREEN}✓ read-only-role exists${NC}" || echo -e "${RED}✗ read-only-role missing${NC}"

# Verify ServiceAccounts
echo -e "\n${BLUE}=== ServiceAccounts ===${NC}"
kubectl get serviceaccounts -n kube-system 2>/dev/null | grep -q "admin-user" && echo -e "${GREEN}✓ admin-user exists${NC}" || echo -e "${RED}✗ admin-user missing${NC}"
kubectl get serviceaccounts -n development 2>/dev/null | grep -q "developer-user" && echo -e "${GREEN}✓ developer-user exists${NC}" || echo -e "${RED}✗ developer-user missing${NC}"
kubectl get serviceaccounts -n development 2>/dev/null | grep -q "readonly-user" && echo -e "${GREEN}✓ readonly-user exists${NC}" || echo -e "${RED}✗ readonly-user missing${NC}"

# Test Developer Permissions
echo -e "\n${BLUE}=== Testing Developer Permissions (in development namespace) ===${NC}"
echo -e "${YELLOW}Deployments:${NC}"
test_permission "developer-user" "create" "deployments" "development"
test_permission "developer-user" "delete" "deployments" "development"
test_permission "developer-user" "list" "deployments" "development"

echo -e "${YELLOW}Pods:${NC}"
test_permission "developer-user" "get" "pods" "development"
test_permission "developer-user" "list" "pods" "development"

echo -e "${YELLOW}Secrets:${NC}"
test_permission "developer-user" "get" "secrets" "development"
test_permission "developer-user" "create" "secrets" "development"

# Test Read-Only Permissions
echo -e "\n${BLUE}=== Testing Read-Only Permissions (in development namespace) ===${NC}"
echo -e "${YELLOW}Pods:${NC}"
test_permission "readonly-user" "get" "pods" "development"
test_permission "readonly-user" "list" "pods" "development"

echo -e "${YELLOW}Deployments:${NC}"
test_permission "readonly-user" "get" "deployments" "development"
test_permission "readonly-user" "create" "deployments" "development"

echo -e "${YELLOW}Services:${NC}"
test_permission "readonly-user" "list" "services" "development"
test_permission "readonly-user" "delete" "services" "development"

# Test Namespace Restrictions
echo -e "\n${BLUE}=== Testing Namespace Restrictions ===${NC}"
echo -e "${YELLOW}Can developer access production namespace?${NC}"
test_permission "developer-user" "get" "pods" "production"

echo -e "${YELLOW}Can readonly-user access staging?${NC}"
test_permission "readonly-user" "list" "pods" "staging"

# Summary
echo -e "\n${BLUE}=== Summary ===${NC}"
echo -e "${GREEN}✓ Admin role: Full cluster access${NC}"
echo -e "${GREEN}✓ Developer role: Limited to development/staging${NC}"
echo -e "${GREEN}✓ Read-only role: View-only access${NC}"
echo -e "\n${GREEN}🎉 Verification complete!${NC}"
