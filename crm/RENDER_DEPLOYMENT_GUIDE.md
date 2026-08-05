# 🚀 Render Deployment Guide - Student Promotion API
# មគ្គុទ្ទេសក៍ប្រើប្រាស់ Render - API ឡើងថ្នាក់សិស្ស

## ✅ Deployment Status

### What Was Deployed:
- ✅ Student Promotion API (8 new endpoints)
- ✅ StudentHistory management system
- ✅ Complete validation and history preservation
- ✅ API documentation and test scripts

### Git Push Status:
```bash
✅ Merged to main branch
✅ Pushed to GitHub
✅ Commit: b74d107
✅ Changes: 7 files, 2,240 insertions
```

---

## 🌐 Render Auto-Deployment

Render automatically deploys when you push to the `main` branch.

### Deployment Timeline:

```
1. Git Push to Main (✅ DONE)
   ↓
2. GitHub triggers webhook to Render
   ↓ (~30 seconds)
3. Render starts build process
   ↓ (~2-3 minutes)
4. Install dependencies (requirements.txt)
   ↓ (~3-5 minutes)
5. Run build.sh script:
   - collectstatic
   - migrate (NEW: StudentHistory tables)
   - create admin user
   - load initial data
   ↓ (~2-3 minutes)
6. Deploy to production
   ↓
7. Service becomes "Live"
   
Total Time: ~8-12 minutes
```

---

## 🔍 Check Deployment Status

### Option 1: Render Dashboard

1. Go to https://dashboard.render.com/
2. Sign in to your account
3. Find your service: `school-system-com`
4. Check status:
   - 🟢 **"Live"** - Deployment successful
   - 🔵 **"Building"** - Currently deploying
   - 🔴 **"Failed"** - Check logs for errors

### Option 2: Check Logs

In Render Dashboard:
1. Click on your service
2. Go to **"Logs"** tab
3. Look for:
   ```
   ✅ Operations to perform:
   ✅ Running migrations:
   ✅ Applying school.XXXX... OK
   ✅ Starting gunicorn
   ```

### Option 3: Check Events

In Render Dashboard:
1. Click on your service
2. Go to **"Events"** tab
3. Look for recent "Deploy succeeded" event

---

## 🧪 Verify Deployment

### Method 1: Automated Verification Script

```bash
cd d:\Monday-Friday-Year3S1\Monday\python\crm
python verify_promotion_api_deployment.py
```

The script will:
- Test authentication
- Verify all 8 new endpoints
- Show detailed results
- Report success/failure

### Method 2: Manual Testing

#### Step 1: Check if server is live
```bash
curl https://your-app.onrender.com/
```

#### Step 2: Test API authentication
```bash
curl -X POST https://your-app.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

Expected response:
```json
{
  "token": "abc123...",
  "user_id": 1,
  "username": "admin",
  "role": "admin"
}
```

#### Step 3: Test promotion endpoint
```bash
curl -X GET https://your-app.onrender.com/api/student-history/ \
  -H "Authorization: Token YOUR_TOKEN"
```

Expected response:
```json
[]  // or list of history records if data exists
```

### Method 3: Browser Testing

1. **Visit Admin Panel:**
   ```
   https://your-app.onrender.com/admin/
   ```

2. **Check New Models:**
   - Go to "School" section
   - Look for "Student Histories" (ប្រវត្តិសិស្ស)
   - Click to verify model exists

3. **Test Promotion Page:**
   ```
   https://your-app.onrender.com/school/students/promote/
   ```
   - Should load without errors
   - Shows promotion form

---

## 🐛 Troubleshooting

### Issue 1: "This site can't be reached"
**Cause:** Render service is still deploying or has failed

**Solution:**
1. Check Render Dashboard status
2. Wait 10-15 minutes for build to complete
3. Check "Logs" tab for errors

### Issue 2: "500 Internal Server Error"
**Cause:** Migration failed or database error

**Solution:**
1. Check Render Logs for migration errors
2. Go to Render Dashboard → Shell
3. Run: `python manage.py migrate --check`
4. If issues, run: `python manage.py migrate school`

### Issue 3: "404 Not Found" on /api/student-history/
**Cause:** URL routing not configured

**Solution:**
1. Verify code was pushed: Check GitHub repository
2. Check Render deployed latest commit: Dashboard → Events
3. Restart service: Dashboard → Manual Deploy

### Issue 4: Authentication issues
**Cause:** Admin user not created

**Solution:**
1. Render Dashboard → Shell
2. Run: `python create_admin.py`
3. Or manually: `python manage.py createsuperuser`

---

## 📊 Database Migrations

The following migrations should run automatically:

```
school.XXXX_studenthistory - Creates StudentHistory model
school.XXXX_auto_YYYYMMDD - Any related changes
```

### Verify Migrations:

**Via Render Shell:**
```bash
python manage.py showmigrations school
```

Expected output:
```
school
 [X] 0001_initial
 [X] 0002_...
 ...
 [X] 0016_studenthistory (NEW)
 [X] 0017_... (if any)
```

### Manual Migration (if needed):

If migrations didn't run automatically:

1. Go to Render Dashboard
2. Select your service
3. Click "Shell" tab
4. Run:
   ```bash
   python manage.py migrate school
   python manage.py migrate
   ```

---

## 🔐 Environment Variables

Ensure these are set in Render Dashboard → Environment:

Required:
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection (auto-set by Render)
- `PYTHON_VERSION` - 3.11.x or higher

Optional but recommended:
- `DEBUG` - Should be `False` for production
- `ALLOWED_HOSTS` - Your Render domain
- `CLOUDINARY_URL` - If using Cloudinary for images

---

## ✅ Post-Deployment Checklist

After deployment completes:

### 1. Verify Service Status
- [ ] Render Dashboard shows "Live"
- [ ] No errors in Logs tab
- [ ] Latest commit deployed (check Events)

### 2. Test API Endpoints
- [ ] Authentication works
- [ ] `/api/student-history/` accessible
- [ ] `/api/students/check_promotion_eligibility/` works
- [ ] `/api/students/bulk_promote/` works

### 3. Test Web Interface
- [ ] Admin panel accessible
- [ ] Student History model visible
- [ ] Promotion page loads

### 4. Test with Real Data
- [ ] Create test student
- [ ] Add scores and attendance
- [ ] Try promotion workflow
- [ ] Check history records created

---

## 📱 API Endpoints Now Live

Once deployed, these endpoints are available:

### Base URL: `https://your-app.onrender.com/api`

1. **POST** `/students/check_promotion_eligibility/`
2. **POST** `/students/bulk_promote/`
3. **GET** `/students/available_promotions/`
4. **GET** `/students/{id}/history/`
5. **GET** `/student-history/`
6. **GET** `/student-history/by_student/`
7. **GET** `/student-history/by_academic_year/`
8. **GET** `/student-history/promotion_statistics/`

Full documentation: [API_PROMOTION_GUIDE.md](API_PROMOTION_GUIDE.md)

---

## 🔄 Re-deploy if Needed

### Via Render Dashboard:
1. Go to https://dashboard.render.com/
2. Select your service
3. Click "Manual Deploy" button
4. Select "Clear build cache & deploy"

### Via Git Push:
```bash
# Make a small change (e.g., update README)
git add .
git commit -m "Trigger redeploy"
git push origin main
```

---

## 📞 Support Resources

### Render Documentation:
- https://render.com/docs/deploy-django

### Check Service Health:
```bash
# Health check endpoint (if configured)
curl https://your-app.onrender.com/health/

# Or check admin
curl https://your-app.onrender.com/admin/
```

### Debug Mode:
To enable debug logging in Render:
1. Environment tab
2. Add: `LOG_LEVEL=DEBUG`
3. Redeploy

---

## 🎯 Expected Results

After successful deployment:

✅ **Service Status:** Live (Green)
✅ **Build Time:** ~8-12 minutes
✅ **Migrations:** All applied successfully
✅ **API Endpoints:** 8 new endpoints working
✅ **Admin Panel:** StudentHistory model visible
✅ **Web Interface:** Promotion page working

---

## 📊 Monitoring Deployment

### Real-time Monitoring:

**Terminal monitoring:**
```bash
# Watch Render logs (if you have render CLI)
render logs -f

# Or use curl in a loop
while true; do
  curl -s https://your-app.onrender.com/ > /dev/null && echo "✅ Live" || echo "⏳ Building..."
  sleep 10
done
```

**Dashboard monitoring:**
- Keep Render Dashboard open
- Watch "Logs" tab for progress
- Events tab shows deployment history

---

## 🚀 Next Steps After Deployment

1. **Test the API:**
   ```bash
   python verify_promotion_api_deployment.py
   ```

2. **Create test data:**
   - Add sample students
   - Add scores and attendance
   - Test promotion workflow

3. **Update documentation:**
   - Update production URL in docs
   - Share API documentation with team
   - Document any environment-specific settings

4. **Monitor for issues:**
   - Check error logs in first 24 hours
   - Monitor performance
   - Test with real user scenarios

---

## 📝 Deployment Checklist

```
✅ Code changes committed and pushed
✅ Merged to main branch
✅ Push to GitHub completed
✅ Render webhook triggered (automatic)
⏳ Render build in progress (~10 min)
⏳ Migrations running
⏳ Service deploying
⏳ Service live and healthy
⏳ API endpoints verified
⏳ Web interface tested
⏳ Real data tested
```

---

**Current Status:** 
- 🟢 Code pushed to GitHub
- ⏳ Waiting for Render auto-deployment
- ⏱️ Estimated time: 8-12 minutes

**Check status at:** https://dashboard.render.com/

---

**Last Updated:** August 5, 2026  
**Deployment Method:** Render Auto-Deploy  
**Branch:** main  
**Commit:** b74d107
