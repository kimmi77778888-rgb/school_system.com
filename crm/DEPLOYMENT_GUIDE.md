# 🚀 Automated Deployment Guide

This project is configured for **automated deployment** to Render using GitHub Actions.

## 📋 Prerequisites

1. ✅ GitHub repository connected
2. ✅ Render account with web service created
3. ⚠️ GitHub secret configured (see setup below)

## 🔧 Initial Setup

### Step 1: Get Render Deploy Hook

1. Go to your Render Dashboard: https://dashboard.render.com/
2. Select your web service
3. Go to **Settings** tab
4. Scroll down to **Deploy Hook**
5. Click **Create Deploy Hook**
6. Copy the webhook URL (looks like: `https://api.render.com/deploy/srv-xxxxx?key=xxxxx`)

### Step 2: Add GitHub Secret

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `RENDER_DEPLOY_HOOK`
5. Value: Paste the webhook URL from Step 1
6. Click **Add secret**

## 🎯 How Automated Deployment Works

### Automatic Deployment
When you push to the `main` branch:
1. ✅ GitHub Actions runs tests
2. ✅ Checks migrations
3. ✅ Validates Django configuration
4. ✅ Triggers Render deployment
5. ✅ Your app goes live automatically!

### Pull Request Testing
When you create a PR:
- ✅ Runs all tests and checks
- ✅ No deployment (safety check)
- ✅ Shows results in PR

## 📝 Deployment Commands

### Deploy Latest Changes
```bash
# Make your changes
git add .
git commit -m "Your changes"
git push origin main
# ✅ Deployment happens automatically!
```

### Deploy Feature Branch
```bash
# Create feature branch
git checkout -b feature/new-feature
git add .
git commit -m "New feature"
git push origin feature/new-feature

# Create PR and merge to main
# ✅ Deployment happens when merged!
```

### Manual Deployment Trigger
You can also manually trigger deployment from GitHub:
1. Go to **Actions** tab
2. Select **CI/CD Pipeline** workflow
3. Click **Run workflow**
4. Select `main` branch
5. Click **Run workflow** button

## 🔍 Monitor Deployment

### Check GitHub Actions
1. Go to your repository
2. Click **Actions** tab
3. See latest workflow runs
4. Green ✅ = Success
5. Red ❌ = Failed (check logs)

### Check Render Deployment
1. Go to Render Dashboard
2. Select your web service
3. Click **Events** tab
4. See deployment progress
5. View logs for any issues

## 🛠️ Current Deployment Configuration

### Files Involved
- `.github/workflows/ci-cd.yml` - Main CI/CD pipeline
- `build.sh` - Render build script
- `Procfile` - Web server configuration
- `requirements.txt` - Python dependencies

### Build Steps (Render)
1. Install dependencies from `requirements.txt`
2. Collect static files
3. Run database migrations
4. Create admin user (if needed)
5. Fix images and load initial data
6. Fix user profiles
7. Start gunicorn server

## 🚨 Troubleshooting

### Deployment Failed
**Check GitHub Actions logs:**
1. Go to Actions tab
2. Click failed workflow
3. Expand failed step
4. Read error message

**Common issues:**
- ❌ Missing environment variables → Add in Render dashboard
- ❌ Migration errors → Check models.py changes
- ❌ Dependency issues → Update requirements.txt
- ❌ Static files → Check STATIC_ROOT settings

### Secret Not Set
If you see "RENDER_DEPLOY_HOOK secret not set":
1. Follow Step 2 in Initial Setup
2. Make sure secret name is exactly `RENDER_DEPLOY_HOOK`
3. Re-run workflow

## 🎉 Success Indicators

✅ GitHub Actions workflow completes successfully
✅ Render shows "Deploy succeeded" 
✅ Website loads without errors
✅ Can login with admin credentials
✅ Database is migrated properly

## 📚 Additional Resources

- [Render Docs](https://render.com/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## 🔄 Workflow Diagram

```
┌─────────────────┐
│  Make Changes   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Git Commit     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Git Push       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  GitHub Actions Runs    │
│  - Install Dependencies │
│  - Run Tests            │
│  - Check Migrations     │
│  - Validate Config      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Trigger Render Deploy  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Render Builds & Runs   │
│  - Run build.sh         │
│  - Start gunicorn       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│  ✅ LIVE!       │
└─────────────────┘
```

## 💡 Best Practices

1. **Always test locally first**
   ```bash
   python manage.py check
   python manage.py migrate --check
   ```

2. **Use feature branches**
   ```bash
   git checkout -b feature/new-feature
   # Make changes
   # Create PR
   # Review → Merge → Auto-deploy
   ```

3. **Monitor deployments**
   - Check GitHub Actions after push
   - Verify Render deployment status
   - Test live site after deployment

4. **Environment variables**
   - Keep secrets in Render environment variables
   - Never commit `.env` file
   - Use `.env.example` for documentation

## 🎊 You're All Set!

Your deployment is now automated! Every push to `main` will automatically deploy to Render. 🚀
