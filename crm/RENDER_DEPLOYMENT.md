# Render Deployment Guide - Image Upload Fix

## Problem
Images cannot be uploaded on Render because the filesystem is ephemeral (resets on every deploy). Your app is already configured to use Cloudinary, but needs environment variables set on Render.

## Solution: Set Cloudinary Environment Variables

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Log in to your account
3. Click on your web service (the one running your Django app)

### Step 2: Add Environment Variables
1. Click **Environment** in the left sidebar
2. Click **Add Environment Variable** button
3. Add these **3 required variables**:

```
Key: CLOUDINARY_CLOUD_NAME
Value: dglgeig8q

Key: CLOUDINARY_API_KEY
Value: 897781257575616

Key: CLOUDINARY_API_SECRET
Value: TGo9vNJKgtmRc863BAJ7mBWon68
```

4. Click **Save Changes**

### Step 3: Add DEBUG Variable (Recommended)
While you're there, also set:

```
Key: DEBUG
Value: False
```

This disables debug mode in production (security best practice).

### Step 4: Wait for Automatic Redeploy
- Render will automatically redeploy your app after saving
- Wait 2-3 minutes for the build to complete
- Check the "Logs" tab to confirm deployment succeeded

---

## Verify It Works

### Option 1: Check the /health/ endpoint
Visit: `https://your-app.onrender.com/health/`

You should see:
```json
{
  "cloudinary": true,
  ...
}
```

If `"cloudinary": true`, image upload is working!

### Option 2: Check the /debug/ endpoint (Admin only)
1. Visit: `https://your-app.onrender.com/debug/`
2. Login as admin
3. Check the response:

```json
{
  "cloudinary_configured": true,
  "media_backend": "crm.cloudinary_storage.MediaCloudinaryStorage"
}
```

### Option 3: Test Upload
1. Go to your deployed app
2. Login as admin
3. Try uploading a student photo or school logo
4. If it works, the image will be stored on Cloudinary (not on Render's disk)

---

## How It Works

### Your Code (Already Done)
1. ✅ `cloudinary_storage.py` - Custom storage backend
2. ✅ `settings.py` - Auto-switches to Cloudinary when env vars exist
3. ✅ `fix_images.py` - Cleans broken local paths on every deploy
4. ✅ `requirements.txt` - Has `cloudinary==1.44.2` installed

### What Happens When You Set Env Vars
1. Django reads `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
2. `settings.py` detects them and sets `_CLOUDINARY_CONFIGURED = True`
3. `STORAGES["default"]` switches from `FileSystemStorage` to `MediaCloudinaryStorage`
4. All image uploads now go to Cloudinary instead of disk
5. Image URLs are automatically generated from Cloudinary CDN

---

## Troubleshooting

### Problem: Still getting errors after setting env vars
**Check Render logs:**
1. Go to Render Dashboard → your service → **Logs** tab
2. Look for errors like:
   ```
   Cloudinary upload failed for 'xxx': ...
   ```
3. Common issues:
   - Wrong API key/secret (double-check the values)
   - Cloudinary account issue (check https://cloudinary.com dashboard)

### Problem: Images uploaded before fix are broken
**Solution:** Already handled!
- `fix_images.py` runs on every deploy via `build.sh`
- It automatically clears broken local file paths from the database
- Old images will show as blank until re-uploaded

### Problem: Can't see uploaded images
**Check:**
1. Visit `/health/` - is `"cloudinary": true`?
2. Check the Cloudinary dashboard at https://cloudinary.com
3. Look in the "Media Library" - are the images there?
4. If images are in Cloudinary but not showing, check browser console for URL errors

---

## Complete Environment Variable Checklist

Your Render service should have these environment variables:

| Variable | Value | Required? |
|----------|-------|-----------|
| `SECRET_KEY` | (your secret key) | ✅ Required |
| `DEBUG` | `False` | ✅ Recommended |
| `DATABASE_URL` | (set by Render) | ✅ Required |
| `CLOUDINARY_CLOUD_NAME` | `dglgeig8q` | ✅ Required for uploads |
| `CLOUDINARY_API_KEY` | `897781257575616` | ✅ Required for uploads |
| `CLOUDINARY_API_SECRET` | `TGo9vNJKgtmRc863BAJ7mBWon68` | ✅ Required for uploads |

---

## After Deployment

### Test All Image Upload Features
- [ ] Student photo upload
- [ ] Teacher photo upload
- [ ] User profile photo upload
- [ ] School logo upload (in School Settings)
- [ ] School favicon upload (in School Settings)

### Monitor Logs
Keep the Render logs tab open while testing to see any errors in real-time.

---

## Summary

**You only need to do 1 thing:**
1. Add the 3 Cloudinary env vars on Render Dashboard → Environment

That's it! Your code is already configured correctly. Once the env vars are set, image upload will work immediately.
