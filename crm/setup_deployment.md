# ⚡ Quick Deployment Setup

## 🚀 Setup in 3 Steps

### 1️⃣ Get Render Deploy Hook
```
1. Go to: https://dashboard.render.com/
2. Select your web service
3. Settings → Deploy Hook → Create Deploy Hook
4. Copy the URL
```

### 2️⃣ Add to GitHub Secrets
```
1. Go to: https://github.com/kimmi77778888-rgb/school_system.com/settings/secrets/actions
2. Click "New repository secret"
3. Name: RENDER_DEPLOY_HOOK
4. Value: [Paste your Render hook URL]
5. Add secret
```

### 3️⃣ Push Changes
```bash
cd d:\Monday-Friday-Year3S1\Monday\python\crm
git add .
git commit -m "Setup automated deployment"
git push origin feature/teacher-student-promotion
```

## ✅ Then Merge to Main
```
1. Create Pull Request on GitHub
2. Review changes
3. Merge to main
4. ✨ Auto-deployment starts!
```

## 🎯 Verify It's Working

After merging to main:
1. Go to: https://github.com/kimmi77778888-rgb/school_system.com/actions
2. See workflow running (orange dot 🟠)
3. Wait for green checkmark (✅)
4. Check your Render dashboard
5. Your site is LIVE! 🎉

## 📍 Current Status

✅ Workflow files created
✅ Deployment guide ready
⚠️ Need to add GitHub secret
⚠️ Need to merge to main

## 🆘 Need Help?

Read the full guide: `DEPLOYMENT_GUIDE.md`
