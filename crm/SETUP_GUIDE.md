# School Management System - Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit the `.env` file with your settings:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Optional: Cloudinary for image storage
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 3. Initialize Database
```bash
python manage.py migrate
```

### 4. Create Admin User
```bash
python create_admin.py
```
Or manually:
```bash
python manage.py createsuperuser
```

### 5. Setup School Data (Optional)
```bash
python manage.py setup_school
```
This creates:
- Default academic years
- Sample grades
- Sample classrooms

### 6. Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000/school/`

## Features Overview

### User Roles
1. **Admin** - Full access to all features
   - Manage users, teachers, students
   - Configure academic years and classes
   - Setup timetables and subjects
   - Generate reports

2. **Teacher** - Teaching and monitoring access
   - View assigned classes
   - Record attendance
   - Enter scores
   - View timetables

3. **Parent** - Limited access to child's information
   - View child's attendance
   - View child's scores
   - View notifications and events

4. **Student** - Personal information access
   - View own attendance
   - View own scores
   - View timetables
   - View notifications

### Key Modules

#### 📚 Academic Management
- **Academic Years** - Define and manage school years
- **Grades** - Configure grade levels (Grade 1, Grade 2, etc.)
- **Classrooms** - Create classes with homeroom teachers
- **Subjects** - Define subjects for each grade level

#### 👨‍🎓 Student & Teacher Management
- **Students** - Complete student profiles with photos
- **Teachers** - Teacher information and qualifications
- **User Accounts** - Link users to teachers/students

#### 📅 Scheduling
- **Timetable** - Class schedules by day and period
- **Time Slots** - Define period times (start/end)

#### ✅ Attendance
- **Student Attendance** - Daily attendance tracking
- **Teacher Attendance** - Staff attendance monitoring
- **Bulk Attendance** - Record entire class at once

#### 📝 Assessments
- **Exams** - Define exam types (Midterm, Final, etc.)
- **Scores** - Record and track student scores
- **Report Cards** - Generate student report cards

#### 📢 Communication
- **Notifications** - Announcements to different audiences
- **Events** - School calendar events

#### 📊 Reports
- **Student Reports** - Comprehensive student listings
- **Attendance Reports** - Attendance summaries
- **Score Reports** - Grade and performance reports
- **Teacher Reports** - Teacher information summaries

## System Configuration

### School Settings
Navigate to: **Settings** → **School Settings**

Configure:
- School name (Khmer & English)
- School slogan
- Logo and Favicon
- Contact information
- Color scheme (Primary, Secondary, Sidebar)

### Academic Year Setup
1. Go to **Academic Years**
2. Click **Generate Years** to create multiple years at once
3. Set one year as active (the current academic year)

### Creating a Complete Setup

#### Step 1: Academic Structure
1. Create Academic Year(s)
2. Create Grades (e.g., Grade 1, Grade 2, etc.)
3. Create Classrooms for each grade
4. Create Subjects for each grade

#### Step 2: People
1. Add Teachers with their information
2. Add Students and assign to classrooms
3. Create user accounts for teachers/students (optional)

#### Step 3: Scheduling
1. Create Time Slots (e.g., Period 1: 07:00-07:45)
2. Create Timetable entries linking:
   - Classroom
   - Subject
   - Teacher
   - Time Slot
   - Academic Year

#### Step 4: Daily Operations
1. Record attendance daily
2. Create exams
3. Enter scores
4. Send notifications

## Tips & Best Practices

### Performance
- Use Cloudinary for image storage in production
- Enable database connection pooling for PostgreSQL
- Use WhiteNoise for static files (already configured)

### Security
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use strong passwords for admin accounts
- Keep `ALLOWED_HOSTS` restricted

### Data Management
- Backup database regularly
- Export data before major changes
- Use the bulk attendance feature for efficiency

### User Experience
- Upload school logo and favicon for branding
- Customize colors to match school identity
- Send regular notifications to keep users informed
- Generate report cards at end of each term

## Common Tasks

### Resetting Student Password
```bash
python manage.py changepassword student_username
```

### Importing Bulk Data
Use Django admin or create custom management commands

### Exporting Reports
Navigate to Reports section and use browser's print function (PDF)

### Changing School Branding
Go to Settings → School Settings and upload new logo/favicon

## Troubleshooting

### Images Not Loading
- Check `MEDIA_URL` and `MEDIA_ROOT` settings
- Verify Cloudinary credentials if using cloud storage
- Ensure proper file permissions

### Database Errors
- Run migrations: `python manage.py migrate`
- Check database connection settings in `.env`

### Missing User Profiles
The system auto-creates profiles, but if needed:
- Go to Django admin
- Check Users and UserProfiles
- Ensure signals are working

### Style Issues
- Clear browser cache
- Check if static files are collected: `python manage.py collectstatic`
- Verify CSS variables are loading

## Production Deployment

### Using Render.com (Configured)
The project includes Render-specific files:
- `build.sh` - Build script
- `Procfile` - Process configuration
- `RENDER_DEPLOYMENT.md` - Detailed deployment guide

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=generate-a-strong-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/dbname
ALLOWED_HOSTS=yourdomain.com
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

## Support & Documentation

### Django Documentation
- https://docs.djangoproject.com/

### Bootstrap 5
- https://getbootstrap.com/docs/5.3/

### Bootstrap Icons
- https://icons.getbootstrap.com/

## License
This is a school management system built with Django.
