# Deployment Guide

## VM

Install Docker Engine and Docker Compose, provide environment variables through the host secret mechanism, and run the web service with PostgreSQL hosted separately or as a persistent service. Use a reverse proxy for HTTPS.

## AWS

The image can run on ECS/Fargate, App Runner, or another container service. Store secrets in AWS Secrets Manager or Systems Manager Parameter Store, use Amazon RDS for PostgreSQL, configure health checks against `/health/`, and place the service behind an HTTPS load balancer.

Production requirements include `DJANGO_DEBUG=0`, a strong secret key, restricted allowed hosts, TLS, database backups, observability, and a release process that applies migrations before serving new application code.

