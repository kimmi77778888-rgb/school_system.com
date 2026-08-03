# ប្រព័ន្ធតាមដានស្ថានភាពសិស្ស (Student Status Tracking System)

## 🎯 គោលបំណង

ប្រព័ន្ធនេះអនុញ្ញាតឱ្យតាមដាន និងរក្សាទុកប្រវត្តិសិស្សពេញលេញ រួមទាំងព័ត៌មានពីការឡើងថ្នាក់, បញ្ចប់ការសិក្សា, ផ្ទេរសាលា ឬឈប់រៀន។

---

## 📊 ស្ថានភាពសិស្ស (Student Status)

### ប្រភេទស្ថានភាព

| ស្ថានភាព | English | ពណ៌នា |
|---------|---------|--------|
| **សកម្ម** | ACTIVE | សិស្សកំពុងរៀននៅសាលា (លំនាំដើម) |
| **ឡើងថ្នាក់** | PROMOTED | សិស្សត្រូវបានដាក់ឡើងថ្នាក់ថ្មី |
| **បញ្ចប់ការសិក្សា** | GRADUATED | សិស្សបានបញ្ចប់ការសិក្សានៅសាលានេះ |
| **ផ្ទេរសាលា** | TRANSFERRED | សិស្សផ្ទេរទៅសាលាផ្សេង |
| **ឈប់រៀន** | WITHDRAWN | សិស្សឈប់រៀនបណ្តោះអាសន្ន |
| **ផ្អាកការសិក្សា** | SUSPENDED | ផ្អាកការសិក្សាបណ្តោះអាសន្ន |

---

## 🔧 មុខងារថ្មី (New Features)

### 1. ប្រវត្តិសិស្ស (Student History)

ប្រព័ន្ធរក្សាទុកព័ត៌មានដូចខាងក្រោម:

- **ថ្នាក់មុន (previous_classroom)**: ថ្នាក់រៀនដែលសិស្សធ្លាប់រៀន
- **ថ្ងៃឡើងថ្នាក់ (promotion_date)**: ថ្ងៃដែលសិស្សឡើងថ្នាក់
- **ថ្ងៃបញ្ចប់ការសិក្សា (graduation_date)**: ថ្ងៃបញ្ចប់ការសិក្សា
- **កំណត់ចំណាំ (notes)**: ព័ត៌មានបន្ថែមអំពីសិស្ស និងប្រវត្តិការផ្លាស់ប្តូរ

### 2. ការឡើងថ្នាក់ដោយស្វ័យប្រវត្តិ

នៅពេលដាក់សិស្សឡើងថ្នាក់:
- ✅ ប្រព័ន្ធរក្សាទុកឈ្មោះថ្នាក់មុនដោយស្វ័យប្រវត្តិ
- ✅ បន្ថែមកំណត់ចំណាំអំពីការឡើងថ្នាក់
- ✅ កំណត់ស្ថានភាពជា "PROMOTED"
- ✅ រក្សាទុកថ្ងៃឡើងថ្នាក់

---

## 📋 ការប្រើប្រាស់

### ជំហានទី 1: ពិនិត្យស្ថានភាពសិស្ស

នៅទំព័របញ្ជីសិស្ស (`/school/students/`) អាច:

1. **ត្រងស្ថានភាព**: ជ្រើសរើសស្ថានភាពពីដ្រុបដោន
   ```
   ┌─────────────────────────┐
   │ ស្ថានភាព: [ទាំងអស់ ▼]  │
   │          [សកម្ម    ]    │
   │          [ឡើងថ្នាក់  ]   │
   │          [បញ្ចប់ការសិក្សា]│
   └─────────────────────────┘
   ```

2. **មើលសិស្សតាមស្ថានភាព**:
   - សិស្សសកម្ម: សិស្សកំពុងរៀន
   - សិស្សឡើងថ្នាក់: សិស្សដែលទើបឡើងថ្នាក់
   - សិស្សបញ្ចប់ការសិក្សា: អតីតសិស្ស

### ជំហានទី 2: ដាក់សិស្សឡើងថ្នាក់

នៅពេលដាក់សិស្សឡើងថ្នាក់តាមរយៈ `/school/students/promote/`:

**មុនឡើងថ្នាក់:**
```
សិស្ស: សុផារ៉ា តន
ថ្នាក់បច្ចុប្បន្ន: ថ្នាក់ទី១ A
ស្ថានភាព: សកម្ម (ACTIVE)
```

**បន្ទាប់ពីឡើងថ្នាក់:**
```
សិស្ស: សុផារ៉ា តន
ថ្នាក់បច្ចុប្បន្ន: ថ្នាក់ទី២ A
ថ្នាក់មុន: ថ្នាក់ទី១ A
ស្ថានភាព: ឡើងថ្នាក់ (PROMOTED)
ថ្ងៃឡើងថ្នាក់: 03/08/2026
កំណត់ចំណាំ: ឡើងថ្នាក់ពី ថ្នាក់ទី១ A ទៅ ថ្នាក់ទី២ A នៅថ្ងៃទី 03/08/2026
```

### ជំហានទី 3: ប្តូរស្ថានភាពដោយដៃ

នៅទម្រង់កែសម្រួលសិស្ស:

1. ចូលទៅកាន់ **Students** → **Edit**
2. ស្វែងរកផ្នែក **ស្ថានភាព (Status)**
3. ជ្រើសរើសស្ថានភាពថ្មី
4. បន្ថែមកំណត់ចំណាំក្នុងវាល **notes**
5. រក្សាទុក

---

## 🎓 ឧទាហរណ៍ (Examples)

### ឧទាហរណ៍ទី 1: ឡើងថ្នាក់ពីថ្នាក់ទី១ ទៅថ្នាក់ទី២

```python
# ប្រព័ន្ធធ្វើស្វ័យប្រវត្តិ:
student.previous_classroom = "ថ្នាក់ទី១ A"
student.classroom = classroom_grade_2_a
student.status = "PROMOTED"
student.promotion_date = "2026-08-03"
student.notes += "\nឡើងថ្នាក់ពី ថ្នាក់ទី១ A ទៅ ថ្នាក់ទី២ A នៅថ្ងៃទី 03/08/2026"
student.save()
```

### ឧទាហរណ៍ទី 2: បញ្ចប់ការសិក្សា

```python
student.status = "GRADUATED"
student.graduation_date = "2026-06-15"
student.is_active = False
student.notes += "\nបញ្ចប់ការសិក្សានៅថ្ងៃទី 15/06/2026"
student.save()
```

### ឧទាហរណ៍ទី 3: ផ្ទេរសាលា

```python
student.status = "TRANSFERRED"
student.is_active = False
student.notes += "\nផ្ទេរទៅសាលា ABC នៅថ្ងៃទី 10/03/2026"
student.save()
```

---

## 📊 របាយការណ៍ និងការវិភាគ

### 1. ស្ថិតិសិស្ស

```sql
-- សិស្សសកម្ម
SELECT COUNT(*) FROM school_student WHERE status='ACTIVE' AND is_active=1;

-- សិស្សឡើងថ្នាក់ឆ្នាំនេះ
SELECT COUNT(*) FROM school_student 
WHERE status='PROMOTED' 
AND YEAR(promotion_date) = 2026;

-- សិស្សបញ្ចប់ការសិក្សា
SELECT COUNT(*) FROM school_student WHERE status='GRADUATED';
```

### 2. ប្រវត្តិសិស្សម្នាក់

```python
student = Student.objects.get(student_id='STU-0001')
print(f"សិស្ស: {student.first_name} {student.last_name}")
print(f"ថ្នាក់បច្ចុប្បន្ន: {student.classroom}")
print(f"ថ្នាក់មុន: {student.previous_classroom}")
print(f"ស្ថានភាព: {student.get_status_display()}")
print(f"កំណត់ចំណាំ:\n{student.notes}")
```

---

## 🛠️ សម្រាប់អ្នកអភិវឌ្ឍន៍ (For Developers)

### Model Fields Added

```python
class Student(models.Model):
    # New fields
    STATUS_CHOICES = [
        ('ACTIVE', 'សកម្ម (Active)'),
        ('PROMOTED', 'ឡើងថ្នាក់ (Promoted)'),
        ('GRADUATED', 'បញ្ចប់ការសិក្សា (Graduated)'),
        ('TRANSFERRED', 'ផ្ទេរសាលា (Transferred)'),
        ('WITHDRAWN', 'ឈប់រៀន (Withdrawn)'),
        ('SUSPENDED', 'ផ្អាកការសិក្សា (Suspended)'),
    ]
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ACTIVE'
    )
    previous_classroom = models.CharField(max_length=200, blank=True)
    promotion_date = models.DateField(null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
```

### API Example

```python
# views.py - Promotion logic
from django.utils import timezone

# When promoting students
for student_id in student_ids:
    student = Student.objects.get(pk=student_id)
    
    # Save history
    old_classroom = student.classroom.name if student.classroom else 'N/A'
    student.previous_classroom = old_classroom
    student.promotion_date = timezone.now().date()
    
    # Update status
    student.status = 'PROMOTED'
    
    # Move to new classroom
    student.classroom = next_classroom
    
    # Add note
    promotion_note = f"ឡើងថ្នាក់ពី {old_classroom} ទៅ {next_classroom.name} នៅថ្ងៃទី {timezone.now().strftime('%d/%m/%Y')}"
    if student.notes:
        student.notes += f"\n{promotion_note}"
    else:
        student.notes = promotion_note
    
    student.save()
```

### Filtering Students

```python
# views.py
status_filter = request.GET.get('status', '')
if status_filter:
    students = students.filter(status=status_filter)

# Template context
context = {
    'students': students,
    'status_choices': Student.STATUS_CHOICES,
    'selected_status': status_filter,
}
```

---

## 🔍 ការស្វែងរកសិស្ស

### តាមស្ថានភាព

```python
# សិស្សសកម្ម
active_students = Student.objects.filter(status='ACTIVE', is_active=True)

# សិស្សឡើងថ្នាក់
promoted_students = Student.objects.filter(status='PROMOTED')

# សិស្សបញ្ចប់ការសិក្សា
graduated_students = Student.objects.filter(status='GRADUATED')
```

### តាមថ្នាក់មុន

```python
# សិស្សដែលធ្លាប់រៀននៅថ្នាក់ទី១
former_grade1 = Student.objects.filter(
    previous_classroom__icontains='ថ្នាក់ទី១'
)
```

---

## ❓ សំណួរញឹកញាប់ (FAQ)

### Q1: តើប្រព័ន្ធរក្សាទុកប្រវត្តិសិស្សរយៈពេលប៉ុន្មាន?

**A:** ប្រព័ន្ធរក្សាទុកប្រវត្តិទាំងអស់រហូតទាល់តែអ្នកលុបសិស្សចេញ។ សូម្បីតែសិស្សបានបញ្ចប់ការសិក្សារួចហើយ ព័ត៌មានរបស់គេនៅតែមាននៅក្នុងប្រព័ន្ធ។

### Q2: តើអាចប្តូរស្ថានភាពមកវិញបានទេ?

**A:** បាន។ អ្នកអាចកែស្ថានភាពសិស្សនៅពេលណាក៏បាន តាមរយៈទម្រង់កែសម្រួលសិស្ស។

### Q3: តើស្ថានភាព "PROMOTED" និង "ACTIVE" ខុសគ្នាយ៉ាងណា?

**A:** 
- **ACTIVE**: សិស្សកំពុងរៀនធម្មតា
- **PROMOTED**: សិស្សទើបឡើងថ្នាក់ (មានព័ត៌មានថ្នាក់មុន និងថ្ងៃឡើងថ្នាក់)

### Q4: តើត្រូវប្តូរស្ថានភាពពី "PROMOTED" ទៅ "ACTIVE" ទេ?

**A:** អាចធ្វើបាន ប៉ុន្តែមិនចាំបាច់។ ប្រសិនបើចង់ កំណត់ស្ថានភាពជា "ACTIVE" វិញបន្ទាប់ពីបានចាប់ផ្តើមរៀននៅថ្នាក់ថ្មី។

### Q5: តើយ៉ាងណាបើចង់ដឹងសិស្សធ្លាប់ឡើងថ្នាក់អស់ប៉ុន្មានដង?

**A:** មើលក្នុងវាល **notes** នៃសិស្ស។ វារក្សាទុកប្រវត្តិការឡើងថ្នាក់ទាំងអស់។

---

## 📝 កំណត់ចំណាំសំខាន់

⚠️ **សំខាន់:**
- ស្ថានភាព "PROMOTED" ត្រូវបានកំណត់ដោយស្វ័យប្រវត្តិពេលប្រើមុខងារឡើងថ្នាក់
- ទិន្នន័យប្រវត្តិមិនអាចលុបបានទេ លុះត្រាតែលុបសិស្សចេញទាំងស្រុង
- វាល `is_active` និង `status` ខុសគ្នា:
  - `is_active=True`: សិស្សនៅក្នុងប្រព័ន្ធ (អាចធ្វើការជាមួយបាន)
  - `is_active=False`: សិស្សបានចាកចេញ (លែងសកម្ម)
  - `status`: បញ្ជាក់លម្អិតពីស្ថានភាពជាក់ស្តែង

---

## 🎯 អត្ថប្រយោជន៍

✅ **រក្សាទុកប្រវត្តិពេញលេញ**: មិនបាត់បង់ទិន្នន័យសិស្ស
✅ **តាមដានដំណើរការសិស្ស**: ដឹងថាសិស្សឡើងថ្នាក់ពេលណា
✅ **សម្រួលរបាយការណ៍**: ងាយស្រួលធ្វើរបាយការណ៍អំពីការឡើងថ្នាក់
✅ **គាំទ្រច្បាប់**: រក្សាទុកទិន្នន័យតាមតម្រូវការច្បាប់
✅ **មិនលុបទិន្នន័យ**: សិស្សចាស់នៅតែមាននៅក្នុងប្រព័ន្ធ

---

## 📞 ជំនួយបន្ថែម

បើមានសំណួរ ឬត្រូវការជំនួយ សូមទាក់ទង:
- Email: admin@school.com
- ឬមើល documentation ផ្សេងទៀត

---

*ឯកសារនេះត្រូវបានបង្កើតនៅថ្ងៃទី 03/08/2026*
