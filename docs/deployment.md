# Deployment

## Local Docker

Use Backend/docker-compose.yml for API, worker, Redis, and Postgres.

## Production Recommendations

- Use managed Postgres and Redis
- Store generated files in object storage
- Use environment-based CORS and secret configuration
- Add health checks and observability dashboards

## Release Flow

1. Merge to main
2. Run CI checks
3. Build and publish container images
4. Deploy to staging
5. Promote to production
