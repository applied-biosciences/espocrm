# NuriVoyage development rules

- Stage 3 implementation belongs on `codex/nurivoyage-stage-3`, based on the approved Stage 1–2 commit `24a945c5a31a03981303e75dd25e5ccb220f6882`. Do not merge Stage 3 until its human UAT is accepted.
- The user overrides the Stage 3 task palette: every web page canvas is #C2F9FF; gold browser theme colour is #C9A227; use the supplied unchanged company logo and plane.png favicon.
- Stage 1–2 work belongs on `codex/nurivoyage-stage-1-2`; never modify master directly.
- Do not edit EspoCRM core unless unavoidable; explain the reason and upgrade impact first.
- Use supported `custom/Espo/Custom` and `client/custom` resources and extensions.
- Never commit credentials, runtime config, database exports or `.env`.
- Use only synthetic development data, never production customer/passport data.
- Run `scripts/local smoke` before committing and include its actual result.
- Do not silently upgrade EspoCRM (10.0.10), MariaDB (11.4.5), or other pinned services.
- Preserve and document schema migrations in `docs/nurivoyage/migrations.md`.
- Document custom entities, fields and permissions in `docs/nurivoyage/stage-1-design.md`.
- Keep future AWS infrastructure in `infrastructure/terraform`; no AWS deployment in Stage 1–2.
- Use Espo's storage interface for documents: MinIO locally, S3-compatible configuration later.
- Human UAT is pending until a human records completion. Automated browser checks do not replace it.

<!-- BEGIN AWS Agent Toolkit rules -->
# AWS Guidance for the new AWS experience

This user has signed up for the new AWS experience. This experience lets you sign into AWS using a social provider and requires the following additional context.

Where this guidance conflicts with the project's own instructions, the project's instructions take precedence.

## Context
### Terminology:
- Say "project" instead of "account" — a project contains an AWS account and settings for sharing with other collaborators
- Say "team member" instead of "IAM user" — users are invited by email, not created or federated in IAM
- Say "AWS Settings" when referring to management tasks at https://settings.aws.com/ (project management, billing, team members, spend limits). Users view their actual AWS resources in the AWS Management Console.
- The user has a managed IAM experience. This includes managed service control policies (SCP) and resource control policies (RCP) that govern the use of AWS. IAM policies are still needed for service-to-service access.

### Constraints:
- All projects share a single AWS Region determined by the user's contact address. Resources cannot be created in other Regions.
- Create all Regional resources in the selected Region, `eu-north-1`.
- WAF and CloudWatch Logs may use `us-east-1` only when required by a global resource; do not use it for ordinary regional resources.
- Do not create Lambda, API Gateway or other Regional resources outside `eu-north-1`.
- Do not use Lambda@Edge, CloudFormation StackSets, cross-Region replication, multi-Region KMS keys or Route 53 cross-Region routing.
- CloudFront is global and may be managed through `us-east-1`, but its regional origins must remain in `eu-north-1`.
- Amazon Rekognition, Textract, Personalize and App Runner are unavailable in `eu-north-1`.
- Do not assign roles to team members unless absolutely necessary.
- If access is suddenly denied, check the project spend limit in AWS Settings > Billing.
- Before starting a task, check for a relevant installed AWS skill and prefer its guidance.

### Help level
The user must choose LOW, MEDIUM or HIGH guidance for AWS work. LOW flags security risks only. MEDIUM asks up to two clarifying questions for ambiguity or risk. HIGH explains each step, suggests alternatives and flags best practices while still executing the user's choice.
<!-- END AWS Agent Toolkit rules -->
