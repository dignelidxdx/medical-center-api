# AWS End-to-End Architecture Specification

## Objective

Extend Medical Center API from a local Docker/PostgreSQL application into a public, reproducible AWS learning environment. The architecture must demonstrate networking, containers, managed PostgreSQL, IAM, secrets, encryption, certificates, asynchronous messaging, observability, cost controls, and infrastructure as code without using real medical data.

## Phases

1. Local baseline: Django, PostgreSQL, Docker Compose, tests, and coverage.
2. AWS container baseline: ECR, VPC, ECS/Fargate, ALB, RDS PostgreSQL, Secrets Manager, KMS, and CloudWatch.
3. Messaging: SNS publishes domain events; SQS buffers work for a separate worker.
4. Delivery and governance: Terraform, CI/CD, CloudTrail, tags, budgets, alarms, and rollback runbooks.
5. Kubernetes migration: Helm and EKS using the same application image and external RDS.

## In scope

- One AWS development environment in one region.
- Private subnets for ECS tasks and RDS.
- Public subnets only for the Application Load Balancer and controlled egress components.
- ECR image storage.
- ECS/Fargate API task and worker task.
- RDS PostgreSQL.
- SNS and SQS for asynchronous appointment events.
- IAM roles with least privilege.
- Secrets Manager and KMS encryption.
- ACM certificate and HTTPS at the ALB.
- CloudWatch logs, metrics, alarms, and retention.
- Terraform modules and environment configuration.
- Cost tags, AWS Budgets, and a destroy procedure.
- SVG architecture diagram and operational runbooks.

## Out of scope

- Real patient data.
- Public production medical service.
- Mobile application.
- Multi-region disaster recovery.
- Redshift, EMR, SageMaker, IoT, Kinesis, and Control Tower.
- Full healthcare compliance certification.
- EKS before ECS/Fargate is working.

## Service flow

```text
Client → Route 53/ALB → ECS Django API → RDS PostgreSQL
                                      └→ SNS → SQS → ECS worker
```

The API remains the source of truth for appointment state. SNS/SQS handle asynchronous work such as notifications, audit events, or reporting jobs. Consumers must be idempotent and messages must be safely retryable.

## Security model

- No long-lived AWS access keys in the repository or container.
- Human access uses named IAM identities with MFA; workloads use IAM roles.
- ECS API and worker roles have separate policies.
- RDS is private and accepts traffic only from the ECS security group.
- Secrets are injected from Secrets Manager.
- RDS, S3 if introduced, logs, and queues use encryption where supported.
- HTTPS uses ACM and terminates at the ALB.
- `DJANGO_DEBUG=0` is mandatory outside local development.
- Authentication and authorization must be implemented before any public medical-data deployment.

## Terraform structure

```text
infra/terraform/
  modules/
    networking/
    ecr/
    ecs/
    rds/
    messaging/
    security/
    observability/
  environments/
    dev/
    staging/
```

Terraform state must use a protected remote backend in a real shared environment. State files, `.terraform/`, credentials, and private keys must never be committed.

## Verification

- `terraform fmt -check` passes.
- `terraform validate` passes.
- A plan can be reviewed before apply.
- The API health check works through the ALB.
- A deployment can run migrations as a controlled release step.
- An appointment event reaches SNS and an SQS consumer processes it once or safely retries it.
- CloudWatch receives application logs and alarms on failed health checks.
- A rollback and destroy procedure are documented and tested in the development environment.

## Service specifications

The service decisions are summarized in the matrix below. Detailed implementation notes should be added to this document only when they affect the end-to-end design.

| Capability | AWS services | Learning outcome |
|---|---|---|
| Networking | VPC, public/private subnets, security groups | Private application and database paths |
| Identity and secrets | IAM, Secrets Manager, KMS | Least privilege and encrypted runtime configuration |
| Containers | ECR, ECS, Fargate | Build, store, run, update, and roll back images |
| Database | RDS PostgreSQL | Managed persistence, backups, and migrations |
| Edge and certificates | ALB, ACM, optional Route 53 | HTTPS ingress and health-based routing |
| Messaging | SNS, SQS, dead-letter queue | Decoupled, retryable, idempotent work |
| Operations | CloudWatch, CloudTrail, AWS Budgets | Logs, alarms, auditability, and cost control |
| Kubernetes stage | EKS, Helm, ALB Controller, IRSA | Migrate the same workload to Kubernetes |

Each capability must have Terraform, verification, least-privilege, and rollback notes in the implementation plan before it is deployed.
