# AWS amd64 EC2 and S3 deployment

The deployment helper builds the NuriVoyage application image for `linux/amd64`, pushes it to an existing ECR repository, uploads the UI and supported application extensions to an existing S3 release bucket, and sends an installation command to an existing SSM-managed EC2 instance. It never creates AWS resources and runs in dry-run mode unless `--apply` is supplied.

## Prerequisites

- AWS CLI profile `HoldMyCoffee` authenticated with `aws login`.
- Selected Region `eu-north-1`.
- Docker Desktop with `buildx`.
- An ECR repository, private S3 bucket and SSM-managed EC2 instance already provisioned in `eu-north-1`.
- The EC2 instance role can pull from ECR, read the release prefix in S3 and run Docker. Runtime secrets must come from Secrets Manager or Parameter Store.

## Dry-run build

```bash
AWS_PROFILE=HoldMyCoffee \
ECR_REPOSITORY=nurivoyage \
S3_BUCKET=replace-with-private-release-bucket \
EC2_INSTANCE_ID=i-replace-with-ssm-instance \
scripts/aws/deploy-amd64.sh
```

The dry run builds the `linux/amd64` image locally and performs no AWS upload or remote command.

## Apply an existing deployment

```bash
AWS_PROFILE=HoldMyCoffee \
ECR_REPOSITORY=nurivoyage \
S3_BUCKET=replace-with-private-release-bucket \
EC2_INSTANCE_ID=i-replace-with-ssm-instance \
scripts/aws/deploy-amd64.sh --apply
```

The apply path pushes the image to ECR, uploads a release archive to S3 with server-side encryption, pulls the image on EC2 through SSM and stages the archive. It does not put `.env`, database dumps or local Docker volumes into S3. Use an approved backup/restore procedure for production data migration and verify the S3 bucket policy, versioning, access logging, CloudTrail data events and lifecycle retention before use.

To upload an explicit local backup created by `scripts/local backup`, add `BACKUP_DIR=backups/<timestamp>` to the apply command. The script requires the backup manifest and database dump, syncs the backup under the bucket's `backups/` prefix with server-side encryption, and still excludes environment files.

The current project has no ECR repository, S3 bucket or EC2 instance in `eu-north-1`; those resources must be provisioned and reviewed before applying this command.
