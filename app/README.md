# E-commerce Infrastructure with Terraform

[![Terraform](https://img.shields.io/badge/Terraform-v1.0+-623CE4?logo=terraform)](https://terraform.io)
[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?logo=amazon-aws)](https://aws.amazon.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A comprehensive Infrastructure as Code (IaC) solution for deploying a scalable e-commerce platform on AWS using Terraform. This project implements best practices for cloud infrastructure, security, and automation.

## 🏗️ Architecture Overview

This project creates a complete AWS infrastructure for an e-commerce application with the following components:

- **VPC**: Multi-AZ Virtual Private Cloud with public and private subnets
- **Elastic Beanstalk**: Managed application hosting with auto-scaling
- **RDS MySQL**: Managed database in private subnets with security groups
- **S3**: Object storage for static assets and application deployment
- **EC2**: Additional compute resources with key pair authentication
- **Security Groups**: Network-level security controls

![Architecture Diagram](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/8626787b-7791-4fe3-99e8-f41f30ba370d.png)

## 🚀 Features

- **Modular Design**: Organized into reusable Terraform modules
- **Multi-AZ Deployment**: High availability across multiple availability zones
- **Security-First**: Private subnets for database, security groups, and IAM roles
- **Auto-Scaling**: Elastic Beanstalk with configurable auto-scaling policies
- **Database Integration**: RDS MySQL with environment variable injection
- **Static Asset Management**: S3 bucket with proper IAM policies
- **Infrastructure Monitoring**: CloudWatch integration for monitoring

## 📁 Project Structure

```
├── main.tf                     # Root configuration
├── variables.tf               # Input variables
├── output.tf                  # Output values
├── provider.tf               # AWS provider configuration
├── README.md                 # This file
└── modules/
    ├── vpc/                  # VPC module
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── ec2/                  # EC2 instance module
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   ├── key-pair.tf
    │   └── SG.tf
    ├── EB/                   # Elastic Beanstalk module
    │   ├── main.tf
    │   ├── variable.tf
    │   ├── output.tf
    │   └── iamrole.tf
    ├── rds/                  # RDS database module
    │   ├── rds.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── sg.tf
    └── S3/                   # S3 bucket module
        ├── main.tf
        ├── variable.tf
        └── outputs.tf
```

## 🛠️ Prerequisites

Before deploying this infrastructure, ensure you have:

1. **AWS Account**: Active AWS account with appropriate permissions
2. **Terraform**: Version 1.0 or later installed
3. **AWS CLI**: Configured with your credentials
4. **SSH Key Pair**: For EC2 instance access

### Required AWS Permissions

Your AWS user/role needs the following services permissions:
- VPC (full access)
- EC2 (full access)
- RDS (full access)
- S3 (full access)
- Elastic Beanstalk (full access)
- IAM (roles and policies)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Divyansh-arma/Ecommerce_CI-CD.git
cd Ecommerce_CI-CD
```

### 2. Configure Variables

Create a `terraform.tfvars` file:

```hcl
# AWS Configuration
aws_region = "us-east-1"
access_key = "your-aws-access-key"
secret_key = "your-aws-secret-key"

# VPC Configuration
vpc_name = "ecommerce-vpc"
vpc_cidr = "10.0.0.0/16"
public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]

# EC2 Configuration
instance_name = "ecommerce-web"
instance_type = "t3.micro"
key_name = "ecommerce-key"

# S3 Configuration
bucket_name = "your-unique-bucket-name"

# Database Configuration
db_name = "ecommerce"
db_username = "admin"
db_password = "your-secure-password"

# Common Tags
common_tags = {
  Environment = "production"
  Project     = "ecommerce"
  ManagedBy   = "terraform"
}
```

### 3. Update SSH Key Path

Edit the `public_key_path` in `main.tf`:

```hcl
public_key_path = "/path/to/your/ssh/public/key.pub"
```

### 4. Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Review the execution plan
terraform plan

# Apply the configuration
terraform apply
```

### 5. Verify Deployment

After successful deployment, you'll receive outputs including:
- VPC ID and subnet information
- Elastic Beanstalk application URL
- RDS endpoint
- S3 bucket name

## 🔧 Configuration Details

### VPC Configuration

- **CIDR Block**: 10.0.0.0/16
- **Public Subnets**: For Elastic Beanstalk and Load Balancers
- **Private Subnets**: For RDS database instances
- **Internet Gateway**: For public subnet internet access
- **NAT Gateway**: For private subnet outbound traffic

### Elastic Beanstalk Configuration

- **Platform**: Python 3.13 on Amazon Linux 2023
- **Instance Type**: t3.micro (configurable)
- **Auto Scaling**: Min 1, Max 2 instances
- **Load Balancer**: Application Load Balancer
- **Environment Variables**: 
  - `DB_HOST`: RDS endpoint
  - `DB_USER`: Database username
  - `DB_PASSWORD`: Database password
  - `STATIC_BUCKET`: S3 bucket name

### RDS Configuration

- **Engine**: MySQL
- **Instance Class**: db.t3.micro
- **Storage**: 20GB (configurable)
- **Multi-AZ**: Disabled (can be enabled for production)
- **Backup**: 7-day retention
- **Security**: Private subnets only

### Security Groups

- **EB Security Group**: HTTP/HTTPS access, SSH for debugging
- **RDS Security Group**: MySQL access from EB instances only
- **EC2 Security Group**: SSH and HTTP access

## 🔒 Security Considerations

1. **Database Security**: RDS instances are deployed in private subnets
2. **Network Isolation**: Security groups restrict access between tiers
3. **IAM Roles**: Least privilege access for EB instances
4. **Secrets Management**: Use AWS Secrets Manager for production passwords
5. **SSL/TLS**: Configure HTTPS in production environments

## 📈 Monitoring and Logging

The infrastructure includes:
- CloudWatch monitoring for all services
- Elastic Beanstalk health monitoring
- RDS performance insights
- Application logs via CloudWatch Logs

## 🔄 CI/CD Integration

This infrastructure is designed to support CI/CD pipelines:
- Application deployment via Elastic Beanstalk
- Blue/green deployments supported
- Rolling deployments with health checks
- Integration with AWS CodePipeline/CodeDeploy

## 🧹 Cleanup

To destroy the infrastructure:

```bash
terraform destroy
```

**Warning**: This will delete all resources and data. Ensure you have backups if needed.

## 📝 Customization

### Scaling Configuration

Modify auto-scaling settings in `modules/EB/main.tf`:

```hcl
setting {
  namespace = "aws:autoscaling:asg"
  name      = "MinSize"
  value     = "2"  # Minimum instances
}

setting {
  namespace = "aws:autoscaling:asg"
  name      = "MaxSize"
  value     = "10"  # Maximum instances
}
```

### Environment-Specific Configurations

Use workspace or separate tfvars files:

```bash
# Development environment
terraform apply -var-file="dev.tfvars"

# Production environment
terraform apply -var-file="prod.tfvars"
```

## 🐛 Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure AWS credentials have required permissions
2. **Resource Limit**: Check AWS service limits in your region
3. **Key Pair Issues**: Verify SSH key path and permissions
4. **Subnet Conflicts**: Ensure CIDR blocks don't overlap

### Debugging

```bash
# Enable detailed logging
export TF_LOG=DEBUG
terraform apply

# Check AWS resources
aws elasticbeanstalk describe-environments
aws rds describe-db-instances
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or issues:
- Create an issue in this repository
- Contact: sharmadivyansh003@gmail.com

## 🙏 Acknowledgments

- AWS for cloud services
- Terraform community for best practices
- Contributors to this project

---

**Note**: This infrastructure is designed for educational and development purposes. For production use, additional security hardening and monitoring should be implemented.
