# Security policy

This public repository is an educational Django API. Use fictional data only. The current MVP has no authentication or authorization on API endpoints, so it must not be exposed publicly as a production medical system.

## Never commit

- AWS access keys, session tokens, or private keys.
- Django secret keys or production database passwords.
- `.env` files.
- Terraform state files or `.terraform/` directories.
- Certificates, private keys, service-account files, or credential JSON files.
- Real patient, specialist, or appointment data.

The repository ignores common local credential and infrastructure files. Before publishing, inspect `git status --short` and the tracked-file list for `.env`, `.aws`, `.terraform`, secret, credential, token, private-key, `.pem`, or `.key` names.

## Local development

Copy `.env.example` to `.env` and keep it untracked. Compose defaults are local-only placeholders, not production credentials. Use AWS Secrets Manager, IAM roles, KMS, and secret injection in AWS environments.

`DJANGO_DEBUG=0` requires an explicit `DJANGO_SECRET_KEY`, preventing an accidental production start with Django's insecure development fallback.

## Before AWS deployment

- Add authentication and role-based authorization.
- Restrict `DJANGO_ALLOWED_HOSTS`.
- Use HTTPS through an AWS load balancer and ACM certificate.
- Keep RDS private and restrict security groups.
- Use IAM roles instead of long-lived access keys.
- Enable encryption, backups, CloudTrail, and CloudWatch logging.
- Scan dependencies and container images.
- Keep real health or patient data out of logs, fixtures, examples, and backups.

If a secret is ever committed, rotate it immediately. Removing it from the latest file is not enough; inspect history and revoke the credential.
