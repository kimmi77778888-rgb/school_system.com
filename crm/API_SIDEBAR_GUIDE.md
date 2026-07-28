# 📍 REST API Sidebar Access Guide

## ✅ API Link Added to Your Dashboard!

The REST API documentation is now integrated into your school management system sidebar for easy access.

## 🎯 Where to Find It

### Location 1: Main Navigation (DEVELOPER Section)

When logged in as **admin**, you'll see:

```
SIDEBAR NAVIGATION
├── ផ្ទាំងគ្រប់គ្រង (Dashboard)
├── គ្រប់គ្រង (Management)
│   ├── អ្នកប្រើប្រាស់ (Users)
│   └── ឆ្នាំសិក្សា (Academic Year)
├── សិក្សា (Education) ▼
│   ├── សិស្ស (Students)
│   ├── គ្រូបង្រៀន (Teachers)
│   ├── ថ្នាក់រៀន (Classrooms)
│   ├── មុខវិជ្ជា (Subjects)
│   └── តារាងម៉ោង (Timetable)
├── ការបង្រៀន (Teaching) ▼
│   ├── វត្តមានសិស្ស (Attendance)
│   ├── វត្តមានក្រុម (Bulk Attendance)
│   ├── វត្តមានគ្រូ (Teacher Attendance)
│   ├── ការប្រឡង (Exams)
│   └── លទ្ធផលប្រឡង (Scores)
├── ទំនាក់ទំនង (Communication) ▼
│   ├── ជូនដំណឹង (Notifications)
│   └── ព្រឹត្តិការណ៍ (Events)
├── លទ្ធផល (Reports) ▼
│   ├── សៀវភៅប័ណ្ណ (Report Cards)
│   ├── របាយការណ៍សិស្ស (Student Reports)
│   ├── របាយការណ៍វត្តមាន (Attendance Reports)
│   ├── របាយការណ៍ពិន្ទុ (Score Reports)
│   └── របាយការណ៍គ្រូ (Teacher Reports)
│
├── 🆕 DEVELOPER                          <-- NEW SECTION
│   └── 📝 REST API Documentation        <-- CLICK HERE!
│
└── FOOTER
    ├── ការកំណត់ (Settings)
    └── 🆕 API Docs                       <-- ALSO HERE!
```

## 👁️ Visual Preview

### Collapsed Sidebar:
```
┌─────┐
│  🎓 │  Logo
├─────┤
│  📊 │  Dashboard
│  👥 │  Management
│  📚 │  Education
│  ✏️  │  Teaching
│  💬 │  Communication
│  📊 │  Reports
│     │
│ 💻  │  DEVELOPER      <-- Shows tooltip "REST API" on hover
│     │
├─────┤
│  ⚙️  │  Settings
│  📝 │  API Docs
└─────┘
```

### Expanded Sidebar:
```
┌─────────────────────────────┐
│  🎓  BELTEI School          │
│      School MS               │
├─────────────────────────────┤
│  ...                        │
│  📊 Reports ▼               │
│     └─ Report Cards         │
│     └─ Student Reports      │
│     └─ Score Reports        │
│                             │
│  DEVELOPER                  │  <-- NEW SECTION
│  💻 REST API Documentation  │  <-- CLICK THIS!
│                             │
├─────────────────────────────┤
│  ⚙️  Settings               │
│  📝 API Docs                │  <-- OR THIS!
└─────────────────────────────┘
```

## 🔍 Icon Details

- **Icon**: `bi-code-square` (Bootstrap Icons)
- **Color**: Light gray (matches sidebar theme)
- **Hover**: Highlights in blue
- **Tooltip**: Shows "REST API" when collapsed

## 🎯 What Happens When You Click

1. **Opens in New Tab** - Doesn't disrupt your work
2. **Shows API Root** - http://localhost:8000/api/
3. **Browsable Interface** - Beautiful Django REST Framework UI
4. **All Endpoints Listed** - 60+ endpoints with descriptions
5. **Interactive Testing** - Can test API calls directly

## 👥 Visibility Rules

| User Role | Can See API Link? | Reason |
|-----------|------------------|--------|
| **Admin** | ✅ YES | Full system access |
| Teacher   | ❌ NO | Not needed for teaching |
| Parent    | ❌ NO | Only need student info |
| Student   | ❌ NO | Limited access |

## 📱 Responsive Behavior

### Desktop
- Shows in main sidebar
- Both locations visible
- Full text labels

### Tablet
- Sidebar auto-collapses
- Icons with tooltips
- Both locations accessible

### Mobile
- Bottom navigation shown
- API link in collapsed sidebar
- Access by opening sidebar menu

## ✨ Usage Examples

### For Developers
1. Click "REST API Documentation"
2. Browse available endpoints
3. Click any endpoint (e.g., `/students/`)
4. See data and test operations
5. Use for building apps

### For Admins
1. Check API status
2. Verify data accessibility
3. Test integrations
4. Monitor API health
5. Share API with developers

## 🎨 Design Integration

The API link seamlessly integrates with your existing UI:

- ✅ Matches sidebar color scheme
- ✅ Uses consistent iconography
- ✅ Follows spacing standards
- ✅ Respects hover states
- ✅ Adapts to collapsed state
- ✅ Works on all devices

## 🚀 Quick Access Steps

### Method 1: Main Navigation
```
Login as Admin
    ↓
Look at Sidebar
    ↓
Scroll down to "DEVELOPER" section
    ↓
Click "REST API Documentation"
    ↓
API opens in new tab!
```

### Method 2: Footer Link
```
Login as Admin
    ↓
Scroll sidebar to bottom
    ↓
Click "API Docs" (below Settings)
    ↓
API opens in new tab!
```

## 📊 What You'll See

When you click the link, you'll see:

```
┌────────────────────────────────────────────┐
│ School Management System API              │
├────────────────────────────────────────────┤
│                                            │
│ API Root                                   │
│                                            │
│ Available Endpoints:                       │
│   • /auth/login/                          │
│   • /dashboard/overview/                  │
│   • /students/                            │
│   • /teachers/                            │
│   • /attendance/                          │
│   • /scores/                              │
│   • ... and 54 more!                      │
│                                            │
│ [Log in] to access full API               │
│                                            │
└────────────────────────────────────────────┘
```

## 🔗 Related Documentation

Once in the API interface, you can also access:

- **START_HERE.md** - Quick start guide
- **API_DOCUMENTATION.md** - Complete reference
- **API_EXAMPLES.md** - Code examples
- **API_QUICK_REFERENCE.md** - Cheat sheet

## 💡 Pro Tips

1. **Bookmark the API page** for quick access
2. **Keep it open in separate tab** while developing
3. **Use browser DevTools** to inspect API responses
4. **Login first** to see protected endpoints
5. **Test before implementing** - verify data structure

## ✅ Checklist

- [x] API link added to sidebar
- [x] Visible only to admins
- [x] Opens in new tab
- [x] Matches UI design
- [x] Works on mobile
- [x] Pushed to GitHub
- [x] Documentation updated

## 🎉 You're All Set!

Your REST API is now just **one click away** from your dashboard!

Login as admin and look for:
- **DEVELOPER** section in sidebar
- **API Docs** in footer

Happy coding! 🚀
