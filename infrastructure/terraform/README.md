# AWS provisioning foundation

This directory contains the repeatable `eu-north-1` provisioning foundation for the amd64 EC2/S3 deployment. It creates an immutable ECR repository, a private versioned encrypted S3 release/backup bucket, an SSM-managed x86_64 EC2 host, and least-privilege instance access.

The application host is intentionally provisioned without public IP or inbound access by default. Set `allowed_ingress_cidr_blocks` only for an approved HTTPS edge or restricted office network. Runtime secrets, database, HTTPS termination, monitoring, backups, restore testing and rollback still require the Stage 19 readiness work before production use.

Example (use a local, uncommitted tfvars file):

```sh
terraform -chdir=infrastructure/terraform init
terraform -chdir=infrastructure/terraform plan \
  -var='vpc_id=vpc-...' \
  -var='subnet_id=subnet-...' \
  -var='ami_id=ami-...' \
  -out=/tmp/nurivoyage-foundation.tfplan
```

Apply only after reviewing that plan. Do not commit AWS account IDs, state backends, access keys, private keys, `.tfvars` files or production secret values.
