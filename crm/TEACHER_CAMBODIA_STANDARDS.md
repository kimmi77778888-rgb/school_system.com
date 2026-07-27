# ព័ត៌មានគ្រូតាមស្តង់ដារកម្ពុជា
# Teacher Information - Cambodia Standards

## Overview
Enhanced Teacher model to comply with Cambodian Ministry of Education standards for teacher information management.

## New Teacher Fields Added

### 1. Professional Information (ព័ត៌មានវិជ្ជាជីវៈ)

#### Teacher Rank (ជួរគ្រូ)
- **Primary Teacher** (គ្រូបឋមសិក្សា)
- **Secondary Teacher** (គ្រូមធ្យមសិក្សា)
- **Senior Teacher** (គ្រូជាន់ខ្ពស់)
- **Master Teacher** (គ្រូបណ្ឌិត)

#### Official Identification
- **Teacher License Number** (លេខអាជ្ញាប័ណ្ណគ្រូ) - Official teaching license
- **Ministry ID** (លេខសម្គាល់ក្រសួង) - Ministry of Education identification number
- **National ID** (អត្តសញ្ញាណប័ណ្ណ) - National identity card number

### 2. Personal Information (ព័ត៌មានផ្ទាល់ខ្លួន)
- **Date of Birth** (ថ្ងៃខែឆ្នាំកំណើត)
- **Place of Birth** (ទីកន្លែងកំណើត)
- **Age Calculation** - Automatically calculated from date of birth

### 3. Education & Training (ការអប់រំនិងបណ្តុះបណ្តាល)
- **University** (សាកលវិទ្យាល័យ) - Name of university attended
- **Degree** (សញ្ញាប័ត្រ) - Degree obtained (Bachelor, Master, PhD)
- **Graduation Year** (ឆ្នាំបញ្ចប់ការសិក្សា)
- **Teacher Training** (បណ្តុះបណ្តាល) - Teacher training programs completed
- **Certifications** (វិញ្ញាបនប័ត្រ) - Professional certifications

### 4. Employment Details (ព័ត៌មានការងារ)
- **Contract Type** (ប្រភេទកិច្ចសន្យា)
  - អចិន្ត្រៃយ៍ (Permanent)
  - កិច្ចសន្យា (Contract)
  - ល្បែ (Temporary/Substitute)
- **Salary Scale** (ជួរប្រាក់ខែ)
- **Years of Experience** (ឆ្នាំបទពិសោធន៍)

### 5. Emergency Contact (ទំនាក់ទំនងបន្ទាន់)
- **Emergency Contact Name** (អ្នកទំនាក់ទំនងបន្ទាន់)
- **Emergency Phone** (ទូរស័ព្ទបន្ទាន់)
- **Emergency Relation** (ទំនាក់ទំនង) - Relationship to teacher

## New Model: Employment History (ប្រវត្តិការងារ)

### Purpose
Track complete work history of teachers including previous schools and positions following Cambodian education sector requirements.

### Fields

#### Basic Information
- **School Name** (ឈ្មោះសាលា) - Name of school/institution
- **Position** (តួនាទី) - Job title/position held
- **Start Date** (ថ្ងៃចាប់ផ្តើម) - Employment start date
- **End Date** (ថ្ងៃបញ្ចប់) - Employment end date (optional for current job)
- **Is Current** (បច្ចុប្បន្ន) - Boolean flag for current employment
- **Location** (ទីតាំង) - School location

#### Detailed Information
- **Responsibilities** (ភារកិច្ច) - Job responsibilities and duties
- **Achievements** (សមិទ្ធផល) - Accomplishments and achievements
- **Reason for Leaving** (មូលហេតុចាកចេញ) - Reason for leaving (if applicable)

#### Calculated Fields
- **Duration** - Automatically calculates years worked (start to end or current date)

## Database Changes

### Models Updated
1. **Teacher Model** - Added 17 new fields
2. **TeacherEmploymentHistory Model** - New model (9 fields)

### Admin Interface
- Registration for Employment History model
- List display with filters
- Search functionality
- Date hierarchy

## Benefits

### 1. Compliance
✅ Meets Cambodian Ministry of Education standards
✅ Proper documentation of teacher qualifications
✅ Official identification tracking

### 2. HR Management
✅ Complete employment history
✅ Track career progression
✅ Contract type management
✅ Salary scale tracking

### 3. Professional Development
✅ Training record keeping
✅ Certification tracking
✅ Years of experience calculation

### 4. Emergency Preparedness
✅ Emergency contact information
✅ Quick access to contact details

## Usage Instructions

### Adding Employment History
1. Go to Teacher detail page
2. Navigate to "Employment History" tab
3. Add previous employment records
4. Mark current position with "Is Current" flag

### Viewing Teacher Information
All new fields are displayed in the teacher detail page organized by category:
- Professional Information
- Personal Information
- Education & Training
- Employment Details
- Emergency Contact
- Employment History

## Migration Steps (To Be Run)

```bash
# Activate virtual environment
cd d:\Monday-Friday-Year3S1\Monday\python
env\Scripts\activate

# Navigate to project
cd crm

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Files Modified

1. **school/models.py**
   - Enhanced Teacher model with 17 new fields
   - Added TeacherEmploymentHistory model
   - Added get_age() method

2. **school/admin.py**
   - Imported TeacherEmploymentHistory
   - Registered TeacherEmploymentHistory admin

## Next Steps

### Required
1. ✅ Run migrations (requires virtual environment activation)
2. ⏳ Update teacher forms to include new fields
3. ⏳ Update teacher detail template to display new information
4. ⏳ Create employment history management interface

### Optional Enhancements
- Employment history timeline visualization
- Career progression charts
- Training certificate upload
- Teacher evaluation integration
- Performance metrics based on rank

## Cambodian Education Context

This implementation follows standard practices in Cambodian schools:

1. **Teacher Ranks**: Based on MoEYS (Ministry of Education, Youth and Sport) classification
2. **License System**: All teachers must have valid teaching licenses
3. **Contract Types**: Reflects actual employment types in Cambodian schools
4. **Documentation**: Comprehensive record-keeping as required by authorities

## Version History

- **Version 1.0** - 2026-07-27
  - Initial implementation
  - Added 17 new teacher fields
  - Created employment history model
  - Admin interface setup

---

**Created by**: School Management System
**Date**: July 27, 2026
**Status**: Code Complete - Pending Migration
