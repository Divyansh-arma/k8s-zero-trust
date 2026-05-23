# Kubernetes RBAC Implementation Guide

## 📋 Overview

This directory contains a complete RBAC (Role-Based Access Control) implementation for your Kubernetes cluster following the **principle of least privilege**.

## 🎯 Roles Implemented

### 1. **Admin Role** (`01-admin-role.yaml`)
- **Scope**: Cluster-wide (ClusterRole)
- **Permissions**: Full access to all resources
- **Use Case**: Cluster administrators, DevOps team leads
- **Access**:
  - All API groups
  - All resources
  - All verbs (get, list, watch, create, update, patch, delete)

### 2. **Developer Role** (`02-developer-role.yaml`)
- **Scope**: Namespace-specific (Role) - `development` and `staging`
- **Permissions**: Limited to development/staging operations
- **Use Case**: Development team members
- **Access**:
  - ✅ Deploy and manage deployments
  - ✅ Manage StatefulSets and DaemonSets
  - ✅ View and execute into pods
  - ✅ Manage services and ingresses
  - ✅ Manage ConfigMaps
  - ❌ Read-only access to Secrets (security)
  - ✅ Manage PersistentVolumeClaims
  - ✅ Auto-scaling configuration

### 3. **Read-Only Role** (`03-readonly-role.yaml`)
- **Scope**: Namespace-specific (Role) - `development`, `staging`, and `production`
- **Permissions**: View-only access
- **Use Case**: Monitoring teams, audit personnel, QA
- **Access**:
  - ✅ Get, list, watch pods and logs
  - ✅ View services and endpoints
  - ✅ View deployments and statuses
  - ✅ View jobs and cronjobs
  - ✅ View events
  - ❌ No create, update, or delete permissions
  - **Production**: Extra restricted (only pods, services, deployments, events)

## 📁 File Structure

```
.
├── 00-namespaces.yaml         # Development, staging, production namespaces
├── 01-admin-role.yaml         # Admin ClusterRole
├── 02-developer-role.yaml     # Developer Role (development & staging)
├── 03-readonly-role.yaml      # Read-Only Role (all namespaces)
├── 04-service-accounts.yaml   # ServiceAccounts for each role
├── 05-role-bindings.yaml      # RoleBindings and ClusterRoleBindings
├── apply-rbac.sh              # Automated deployment script
├── verify-rbac.sh             # Verification script
└── README.md                  # This file
```

## 🚀 Deployment Steps

### Option 1: Automated Deployment (Recommended)

```bash
# Make the script executable
chmod +x apply-rbac.sh

# Run the deployment script
./apply-rbac.sh
```

### Option 2: Manual Deployment

```bash
# 1. Create namespaces
kubectl apply -f 00-namespaces.yaml

# 2. Create roles
kubectl apply -f 01-admin-role.yaml
kubectl apply -f 02-developer-role.yaml
kubectl apply -f 03-readonly-role.yaml

# 3. Create service accounts
kubectl apply -f 04-service-accounts.yaml

# 4. Create role bindings
kubectl apply -f 05-role-bindings.yaml
```

### Option 3: Apply All at Once

```bash
kubectl apply -f .
```

## 🔍 Verification

```bash
# View ClusterRoles
kubectl get clusterroles admin-role

# View Roles
kubectl get roles -n development
kubectl get roles -n staging
kubectl get roles -n production

# View ServiceAccounts
kubectl get serviceaccounts -n kube-system
kubectl get serviceaccounts -n development
kubectl get serviceaccounts -n staging

# View RoleBindings
kubectl get rolebindings -A

# Test permissions
kubectl auth can-i --list --as=system:serviceaccount:development:developer-user -n development
kubectl auth can-i --list --as=system:serviceaccount:development:readonly-user -n development
```

## 👥 ServiceAccounts Created

### Admin User
- **Name**: `admin-user`
- **Namespace**: `kube-system`
- **Binding**: ClusterRoleBinding to `admin-role`

### Developer User
- **Names**: `developer-user` in `development` and `staging`
- **Binding**: RoleBinding to `developer-role`

### Read-Only User
- **Names**: `readonly-user` in `development`, `staging`, and `production`
- **Binding**: RoleBinding to `read-only-role`

## 🔐 Least Privilege Highlights

1. **Namespace Isolation**: Developers and read-only users are restricted to specific namespaces
2. **Resource Restrictions**: 
   - Secrets are read-only for developers
   - Cluster-wide operations restricted to admins only
3. **Action Restrictions**: 
   - Read-only users cannot execute any modifications
   - Developers cannot access production directly
4. **Progressive Restrictions**: 
   - Production has the most restrictive read-only policy
   - Development allows maximum developer flexibility

## 📝 Usage Examples

### Get Kubeconfig for Developer

```bash
# Extract token for developer user
kubectl -n development create token developer-user

# Add to kubeconfig
kubectl config set-credentials developer-user --token=<TOKEN>
kubectl config set-context developer-context --cluster=kind-kind --user=developer-user
kubectl config use-context developer-context
```

### Test Permissions

```bash
# Can developer create deployments in development?
kubectl auth can-i create deployments --as=system:serviceaccount:development:developer-user -n development
# Output: yes

# Can developer access production namespace?
kubectl auth can-i list pods --as=system:serviceaccount:development:developer-user -n production
# Output: no

# Can read-only user delete anything?
kubectl auth can-i delete pods --as=system:serviceaccount:development:readonly-user -n development
# Output: no
```

## 🛠️ Customization

### Add New Developer
```yaml
# In 04-service-accounts.yaml, add:
apiVersion: v1
kind: ServiceAccount
metadata:
  name: developer-user-2
  namespace: development
```

### Restrict Developer Further
Edit `02-developer-role.yaml` to remove specific resources or verbs.

### Expand Read-Only Access
Add more API groups in `03-readonly-role.yaml` as needed.

## ⚠️ Important Notes

1. **Production Access**: No developers have write access to production (by design)
2. **Secret Management**: Developers can only read secrets, not modify them
3. **Token Expiry**: Generated tokens should be refreshed periodically
4. **Audit Logging**: Enable audit logging to track role usage
5. **Regular Review**: Review and update RBAC policies quarterly

## 📚 References

- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Principle of Least Privilege](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
- [KinD Documentation](https://kind.sigs.k8s.io/)

## 🤝 Support

For issues or customization needs, review the Kubernetes RBAC documentation or consult with your DevOps team.
