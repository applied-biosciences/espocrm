# AWS production handoff

This directory is the handoff boundary. Stage 19 prepares the application for AWS but does not provision or modify AWS resources.

The production design requires private networking, HTTPS termination, a managed MariaDB-compatible database, private versioned S3 storage, secrets management, centralized logs and metrics, scheduled backups, restore testing and an explicit rollback path. Use [the Stage 19 readiness checklist](../../docs/nurivoyage/stage-19-production-readiness.md) before adding provider-specific Terraform.

Do not commit AWS account IDs, state backends, access keys, private keys, `.tfvars` files or production secret values. Terraform implementation and `apply` require a separately approved AWS change and CI role.
