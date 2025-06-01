# Google Cloud Deployment Guide for Viraa Care

This guide walks you through deploying the Viraa Care FastAPI application on Google Cloud using Cloud Run and Docker.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud SDK** installed locally
3. **Docker** installed locally
4. **Git** repository access

## Setup Steps

### 1. Initialize Google Cloud Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"

# Login to Google Cloud
gcloud auth login

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Set Environment Variables

```bash
# Set your Google API key for Gemini
export GOOGLE_API_KEY="your-google-gemini-api-key"

# Create a secret in Google Secret Manager (recommended)
gcloud secrets create google-api-key --data-file=- <<< "$GOOGLE_API_KEY"
```

### 3. Local Testing

Test the Docker container locally before deploying:

```bash
# Build the Docker image
docker build -t viraa-care .

# Run locally
docker run -p 8080:8080 -e GOOGLE_API_KEY="$GOOGLE_API_KEY" viraa-care

# Test the application
curl http://localhost:8080/health
```

### 4. Deploy to Google Cloud Run

#### Option A: Using Cloud Build (Recommended)

1. Update the `cloudbuild.yaml` file with your Google API key:
```yaml
substitutions:
  _GOOGLE_API_KEY: 'your-actual-google-api-key'
```

2. Trigger the build and deployment:
```bash
gcloud builds submit --config cloudbuild.yaml .
```

#### Option B: Manual Deployment

```bash
# Build and push the image
docker build -t gcr.io/$PROJECT_ID/viraa-care .
docker push gcr.io/$PROJECT_ID/viraa-care

# Deploy to Cloud Run
gcloud run deploy viraa-care \
    --image gcr.io/$PROJECT_ID/viraa-care \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars GOOGLE_API_KEY="$GOOGLE_API_KEY"
```

### 5. Set Up Custom Domain (Optional)

```bash
# Map a custom domain
gcloud run domain-mappings create \
    --service viraa-care \
    --domain your-domain.com \
    --region us-central1
```

## Configuration Options

### Environment Variables

- `GOOGLE_API_KEY`: Your Google Gemini API key (required)
- `PORT`: Port number (automatically set by Cloud Run)

### Resource Limits

- **Memory**: 1Gi (can be adjusted based on usage)
- **CPU**: 1 vCPU (can be scaled up if needed)
- **Max Instances**: 10 (adjust based on expected traffic)

## Monitoring and Logging

### View Logs
```bash
gcloud run services logs read viraa-care --region us-central1
```

### Monitor Performance
- Visit Google Cloud Console > Cloud Run > viraa-care
- Check metrics, logs, and performance

## Security Best Practices

1. **Use Secret Manager** for sensitive data:
```bash
# Store API key in Secret Manager
gcloud secrets create google-api-key --data-file=- <<< "$GOOGLE_API_KEY"

# Update Cloud Run to use the secret
gcloud run services update viraa-care \
    --update-secrets GOOGLE_API_KEY=google-api-key:latest \
    --region us-central1
```

2. **Enable IAM authentication** if needed:
```bash
gcloud run services update viraa-care \
    --no-allow-unauthenticated \
    --region us-central1
```

## Troubleshooting

### Common Issues

1. **Build Fails**: Check Dockerfile syntax and dependencies
2. **Health Check Fails**: Ensure `/health` endpoint is accessible
3. **Memory Issues**: Increase memory allocation in Cloud Run
4. **API Key Issues**: Verify the Google API key is correct and has Gemini access

### Debug Commands

```bash
# Check service status
gcloud run services describe viraa-care --region us-central1

# View recent logs
gcloud run services logs tail viraa-care --region us-central1

# Test health endpoint
curl https://your-service-url.run.app/health
```

## Cost Optimization

- **CPU Allocation**: Only allocated during request processing
- **Memory**: Pay only for allocated memory during requests
- **Scaling**: Automatically scales to zero when no traffic
- **Request Timeout**: Set appropriate timeout values

## Media Files Consideration

The current Docker setup excludes large media files. For production:

1. **Use Google Cloud Storage** for media files
2. **Update the application** to serve media from Cloud Storage
3. **Consider CDN** for better performance

## Updating the Application

```bash
# Make changes to your code
git add .
git commit -m "Update application"
git push

# Rebuild and redeploy
gcloud builds submit --config cloudbuild.yaml .
```

## Support

- Google Cloud Run Documentation: https://cloud.google.com/run/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- Docker Documentation: https://docs.docker.com 