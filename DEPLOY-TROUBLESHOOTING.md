# Deployment Troubleshooting Guide

## ❌ Issue: "No branch matching the configured branch pattern could be found"

You're encountering this because Cloud Build Trigger was created but is looking for a different branch pattern than your current `master` branch.

## 🔧 Solution Options

### Option 1: Direct Deployment (Recommended - No Triggers)

**Step 1: Install Google Cloud SDK**
Download and install from: https://cloud.google.com/sdk/docs/install

**Step 2: Authenticate and Set Project**
```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace with your actual project ID)
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

**Step 3: Deploy Directly**
```bash
# Use the manual deployment file
gcloud builds submit --config cloudbuild-manual.yaml .
```

### Option 2: Fix the Trigger (For Continuous Deployment)

If you want to keep the trigger for automatic deployments:

**Step 1: Update Trigger to Use 'master' Branch**
```bash
# List existing triggers
gcloud builds triggers list

# Update trigger to use master branch
gcloud builds triggers update TRIGGER_NAME \
    --branch-pattern="^master$"
```

**Step 2: Or Rename Your Branch to 'main'**
```bash
# Rename local branch from master to main
git branch -m master main

# Push the new main branch
git push -u origin main

# Delete old master branch (optional)
git push origin --delete master
```

### Option 3: Delete Trigger and Use Manual Deployment

**Step 1: Delete the Trigger**
```bash
# List triggers
gcloud builds triggers list

# Delete the problematic trigger
gcloud builds triggers delete TRIGGER_NAME
```

**Step 2: Use Direct Deployment**
```bash
gcloud builds submit --config cloudbuild-manual.yaml .
```

## 🚀 Quick Start Commands (After Installing gcloud)

1. **Set up your project:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

2. **Deploy immediately:**
```bash
gcloud builds submit --config cloudbuild-manual.yaml .
```

## 🔍 Debug Commands

**Check your current configuration:**
```bash
# Check current project
gcloud config get-value project

# Check active account
gcloud auth list

# List existing Cloud Run services
gcloud run services list

# List build triggers
gcloud builds triggers list
```

**Check your repository:**
```bash
# Check current branch
git branch --show-current

# Check remote repository
git remote -v

# Check recent commits
git log --oneline -5
```

## 📝 Expected Output

After successful deployment, you should see:
```
✅ Service [viraa-care] deployed successfully
✅ Service URL: https://viraa-care-xxxxx-uc.a.run.app
```

## 🆘 Common Issues & Solutions

### Issue: "gcloud command not found"
**Solution:** Install Google Cloud SDK from https://cloud.google.com/sdk/docs/install

### Issue: "Permission denied" 
**Solution:** Run `gcloud auth login` and ensure you have proper permissions

### Issue: "Project not found"
**Solution:** Verify project ID with `gcloud projects list`

### Issue: "API not enabled"
**Solution:** Enable required APIs:
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

### Issue: "Insufficient memory"
**Solution:** The deployment config uses 1Gi memory. For debugging, you can increase:
```yaml
- '--memory'
- '2Gi'
```

## 🔄 Alternative: GitHub Actions Deployment

If you prefer GitHub Actions over Cloud Build, I can create a workflow file that deploys on push to master.

## 📞 Next Steps

1. **Install Google Cloud SDK** if not already installed
2. **Run authentication**: `gcloud auth login`
3. **Set your project**: `gcloud config set project YOUR_PROJECT_ID`
4. **Enable services**: `gcloud services enable cloudbuild.googleapis.com run.googleapis.com`
5. **Deploy**: `gcloud builds submit --config cloudbuild-manual.yaml .`

Your API key is already configured in the deployment file, so it should work immediately after these steps! 