#!/usr/bin/env bash
set -euo pipefail

# Build and optionally deploy the NuriVoyage amd64 release to an existing EC2 host.
# Dry-run is the default. This script never creates AWS resources and never reads .env secrets.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REGION="${AWS_REGION:-eu-north-1}"
PROFILE="${AWS_PROFILE:-HoldMyCoffee}"
IMAGE_TAG="${IMAGE_TAG:-v10.0.10.01}"
ECR_REPOSITORY="${ECR_REPOSITORY:-}"
S3_BUCKET="${S3_BUCKET:-}"
EC2_INSTANCE_ID="${EC2_INSTANCE_ID:-}"
BACKUP_DIR="${BACKUP_DIR:-}"
APPLY=0

usage() { echo "Usage: AWS_PROFILE=HoldMyCoffee ECR_REPOSITORY=name S3_BUCKET=name EC2_INSTANCE_ID=i-... $0 [--apply]"; }
for arg in "$@"; do case "$arg" in --apply) APPLY=1 ;; -h|--help) usage; exit 0 ;; *) usage; exit 2 ;; esac; done

command -v aws >/dev/null || { echo 'aws CLI is required' >&2; exit 1; }
command -v docker >/dev/null || { echo 'Docker with buildx is required' >&2; exit 1; }
test "$REGION" = eu-north-1 || { echo 'AWS_REGION must be eu-north-1 for this project' >&2; exit 1; }
test -n "$ECR_REPOSITORY" -a -n "$S3_BUCKET" -a -n "$EC2_INSTANCE_ID" || { usage >&2; exit 2; }
test -z "${AWS_SECRET_ACCESS_KEY:-}" || { echo 'Do not pass long-lived AWS secret keys in the environment; use aws login/profile credentials' >&2; exit 1; }

ACCOUNT_ID="$(aws sts get-caller-identity --profile "$PROFILE" --query Account --output text)"
REGISTRY="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
IMAGE="$REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
ARCHIVE="$ROOT/.aws-release/nurivoyage-$IMAGE_TAG.tgz"

echo "AWS profile: $PROFILE"
echo "AWS region: $REGION"
echo "Target image: $IMAGE"
echo "Target EC2: $EC2_INSTANCE_ID"
echo "Target S3 bucket: s3://$S3_BUCKET"
echo "Platform: linux/amd64"

if [ "$APPLY" -eq 0 ]; then
  echo 'DRY RUN: no image push, S3 upload, EC2 command or AWS resource creation will occur.'
  docker buildx build --platform linux/amd64 --provenance=false --sbom=false --file "$ROOT/infrastructure/aws/Dockerfile" --tag "$IMAGE" "$ROOT" --load
  exit 0
fi

mkdir -p "$ROOT/.aws-release"
aws ecr get-login-password --profile "$PROFILE" --region "$REGION" | docker login --username AWS --password-stdin "$REGISTRY"
docker buildx build --platform linux/amd64 --provenance=false --sbom=false --file "$ROOT/infrastructure/aws/Dockerfile" --tag "$IMAGE" "$ROOT" --push
COPYFILE_DISABLE=1 tar --no-xattrs --exclude='./.git' --exclude='./.env' --exclude='./data' --exclude='./backups' -czf "$ARCHIVE" -C "$ROOT" custom client/custom scripts/nurivoyage compose.yaml infrastructure/aws
aws s3 cp "$ARCHIVE" "s3://$S3_BUCKET/releases/$(basename "$ARCHIVE")" --profile "$PROFILE" --region "$REGION" --sse AES256
if [ -n "$BACKUP_DIR" ]; then
  test -f "$BACKUP_DIR/manifest.json" -a -f "$BACKUP_DIR/database.sql" || { echo 'BACKUP_DIR must contain manifest.json and database.sql' >&2; exit 1; }
  aws s3 sync "$BACKUP_DIR" "s3://$S3_BUCKET/backups/$(basename "$BACKUP_DIR")/" --profile "$PROFILE" --region "$REGION" --sse AES256 --exclude '*.env'
fi
aws ssm send-command --profile "$PROFILE" --region "$REGION" --instance-ids "$EC2_INSTANCE_ID" --document-name AWS-RunShellScript --parameters commands="$(cat <<EOF
set -euo pipefail
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $REGISTRY
docker pull $IMAGE
mkdir -p /opt/nurivoyage/releases
aws s3 cp s3://$S3_BUCKET/releases/$(basename "$ARCHIVE") /opt/nurivoyage/releases/$(basename "$ARCHIVE")
tar -xzf /opt/nurivoyage/releases/$(basename "$ARCHIVE") -C /opt/nurivoyage/releases
echo 'Image and release archive installed. Configure Secrets Manager-backed runtime values before restart.'
EOF
)" --comment "NuriVoyage $IMAGE_TAG amd64 release" >/tmp/nurivoyage-ssm-command.json
echo "Applied release. SSM command: $(python3 -c 'import json; print(json.load(open("/tmp/nurivoyage-ssm-command.json"))["Command"]["CommandId"])')"
