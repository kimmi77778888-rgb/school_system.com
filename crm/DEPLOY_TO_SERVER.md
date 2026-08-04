# Deploy Exam Result System to Server
## ដំណើរការដាក់ឡើងប្រព័ន្ធលទ្ធផលប្រឡងទៅ Server

## ✅ Pre-Deployment Checklist

Before deploying, make sure:
- [x] All code is pushed to GitHub ✅
- [x] Database migrations are created ✅
- [x] Server environment variables are set
- [ ] Production settings are configured
- [ ] Static files are collected
- [ ] Database is backed up (if updating existing server)

---

## 🚀 Deployment Steps

### Step 1: Verify GitHub Push

Check that all changes are on GitHub:

```bash
cd d:\Monday-Friday-Year3S1\Monday\python
git status
git log --oneline -5
```

**Expected**: "Your branch is up to date with 'origin/main'"

✅ **Status**: Already pushed! Commit `1cb454f`

---

### Step 2: Connect to Your Server

Depending on your hosting platform:

#### Option A: Render.com
1. Go to https://dashboard.render.com/
2. Select your service
3. Go to "Manual Deploy" → Click "Deploy latest commit"
4. Wait for build to complete

#### Option B: Railway.app
1. Go to https://railway.app/dashboard
2. Select your project
3. Go to "Deployments"
4. Railway auto-deploys from GitHub (no action needed)

#### Option C: Heroku
```bash
git push heroku main
```

#### Option D: Your Own Server (VPS/Linux)
```bash
ssh user@your-server-ip
cd /path/to/your/project
git pull origin main
```

---

### Step 3: Run Deployment Commands on Server

If using **Render/Railway**, the `build.sh` script runs automatically.

If using **your own server**, run these commands:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations (IMPORTANT for ExamResult table!)
python manage.py migrate

# Create superuser (if needed)
python create_admin.py

# Fix any data issues
python fix_profiles.py
```

---

### Step 4: Run the NEW Migration

**CRITICAL**: Make sure migration 0017 runs on the server!

```bash
# SSH into your server
ssh user@your-server

# Go to project directory
cd /path/to/project

# Run migrations
python manage.py migrate school

# Verify ExamResult table exists
python manage.py shell -c "from school.models import ExamResult; print(f'ExamResult table exists: {ExamResult.objects.count()} records')"
```

**Expected Output**: "ExamResult table exists: X records"

---

### Step 5: Create Sample Exam Data (Optional)

If you want sample data on the server for testing:

```bash
# On your server
python setup_exam_data.py
```

This will create:
- 2 exam types (Midterm, Final)
- 2 exams (Math, Khmer)
- Exam results for students

---

### Step 6: Verify Deployment

Test these URLs on your production server:

1. **Main site**: `https://your-domain.com/`
2. **Login**: `https://your-domain.com/login/`
3. **Exams list**: `https://your-domain.com/exams/`
4. **Exam detail**: `https://your-domain.com/exams/1/`

**Check for**:
- ✅ Pages load without errors
- ✅ No 500 errors
- ✅ Static files (CSS, JS) load correctly
- ✅ Eye icons (👁️) appear in exam list
- ✅ Can click to view exam details
- ✅ Statistics display correctly

---

## 🔧 Server Configuration

### Environment Variables (.env on server)

Make sure your server has these variables set:

```bash
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=your-database-url  # if using PostgreSQL

# Cloudinary (for image storage)
CLOUDINARY_CLOUD_NAME=dglgeig8q
CLOUDINARY_API_KEY=897781257575616
CLOUDINARY_API_SECRET=TGo9vNJKgtmRc863BAJ7mBWon68
```

---

## 📝 Platform-Specific Instructions

### For Render.com

1. **Auto-Deploy Setup**:
   - Render automatically deploys when you push to GitHub
   - Build command: `./build.sh`
   - Start command: `gunicorn crm.wsgi:application`

2. **Manual Deploy**:
   - Dashboard → Your Service → "Manual Deploy"
   - Select branch: `main`
   - Click "Deploy"

3. **Environment Variables**:
   - Dashboard → Your Service → Environment
   - Add all variables from `.env.example`

4. **View Logs**:
   - Dashboard → Your Service → Logs
   - Check for migration success

### For Railway.app

1. **Auto-Deploy**: 
   - Railway detects GitHub pushes automatically
   - No manual action needed

2. **Check Deployment**:
   - Dashboard → Your Project → Deployments
   - View build logs for migration status

3. **Environment Variables**:
   - Dashboard → Your Project → Variables
   - Add from `.env.example`

4. **Run Commands**:
   - Cannot run commands directly
   - Use `build.sh` for setup commands

### For Heroku

1. **Deploy**:
   ```bash
   git push heroku main
   ```

2. **Run Migrations**:
   ```bash
   heroku run python manage.py migrate
   ```

3. **Create Admin**:
   ```bash
   heroku run python create_admin.py
   ```

4. **View Logs**:
   ```bash
   heroku logs --tail
   ```

5. **Open App**:
   ```bash
   heroku open
   ```

---

## 🐛 Troubleshooting

### Error: "no such table: school_examresult"

**Solution**: Migration didn't run. Manually run:
```bash
python manage.py migrate school 0017
```

### Error: 500 Internal Server Error

**Solution**: Check server logs:
- **Render**: Dashboard → Logs
- **Railway**: Dashboard → Deployments → View Logs
- **Heroku**: `heroku logs --tail`
- **Own Server**: Check `/var/log/nginx/error.log`

### Error: Static files not loading (no CSS)

**Solution**: Run collectstatic:
```bash
python manage.py collectstatic --no-input
```

Make sure `STATIC_ROOT` and `STATIC_URL` are set in settings.

### Error: "Permission denied"

**Solution**: 
```bash
chmod +x build.sh
```

### Pages work but Exam detail shows empty

**Solution**: No exam data. Run setup script:
```bash
python setup_exam_data.py
```

---

## 📊 Post-Deployment Verification

### Checklist

Run through this checklist after deployment:

#### Basic Functionality
- [ ] Homepage loads
- [ ] Can login as admin
- [ ] Dashboard displays
- [ ] Navigation menu works

#### Exam Result System
- [ ] Can access `/exams/` page
- [ ] Exam list displays (even if empty)
- [ ] Can click "Add Exam" button
- [ ] Can create a new exam
- [ ] Eye icon (👁️) appears in list
- [ ] Can click eye icon to view exam detail
- [ ] Exam detail page loads without errors
- [ ] Statistics cards display
- [ ] Grade distribution shows
- [ ] Can add exam results through admin
- [ ] Individual result detail page works

#### Database
- [ ] ExamResult table exists (check with Django shell)
- [ ] Can query ExamResult.objects.all()
- [ ] Migrations are up to date

---

## 🔄 Updating the Server (Future Updates)

When you make changes and want to deploy:

1. **Commit and push**:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```

2. **Deploy**:
   - **Render/Railway**: Auto-deploys (wait 2-5 minutes)
   - **Heroku**: `git push heroku main`
   - **Own Server**: `ssh` in and `git pull origin main`

3. **Run migrations** (if you added/changed models):
   ```bash
   python manage.py migrate
   ```

4. **Restart server** (if needed):
   - **Render**: Auto-restarts
   - **Railway**: Auto-restarts
   - **Heroku**: `heroku restart`
   - **Own Server**: `sudo systemctl restart gunicorn`

---

## 📞 Quick Reference

### Important URLs
- GitHub Repo: https://github.com/kimmi77778888-rgb/school_system.com
- Your Server: [Add your server URL here]

### Important Commands

```bash
# Check status
git status

# Push changes
git push origin main

# SSH to server
ssh user@your-server

# Run migrations
python manage.py migrate

# Create admin
python create_admin.py

# Collect static files
python manage.py collectstatic --no-input

# View logs (Railway/Render: use dashboard)
tail -f /var/log/gunicorn/error.log
```

---

## 🎯 Deployment Workflow Summary

```
┌─────────────────────────────────────────┐
│  1. Code Changes (Local)                │
│     - Develop features                  │
│     - Test locally                      │
│     - Commit changes                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. Push to GitHub                      │
│     git push origin main                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. Auto-Deploy (Render/Railway)        │
│     - Runs build.sh automatically       │
│     - Installs requirements             │
│     - Collects static files             │
│     - Runs migrations                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. Verify Deployment                   │
│     - Check logs                        │
│     - Test URLs                         │
│     - Verify features work              │
└─────────────────────────────────────────┘
```

---

## ✅ Current Status

- [x] Code pushed to GitHub (commit `1cb454f`)
- [x] Migration 0017 created
- [x] Sample data script ready
- [x] Build script configured
- [ ] Deployed to server (← **YOU ARE HERE**)
- [ ] Verified on production

---

## 🚀 Ready to Deploy!

**Next Step**: Choose your deployment method above and follow the instructions!

If you're using **Render** or **Railway**, just:
1. Go to your dashboard
2. Click "Manual Deploy" or wait for auto-deploy
3. Check logs for "Migration 0017 applied successfully"
4. Visit your site and go to `/exams/`

**That's it!** 🎉

---

**Last Updated**: August 4, 2026  
**Git Commit**: 1cb454f  
**Features Added**: Exam Result Detail System with migrations
