# កាលវិភាគតាមប្រព័ន្ធអប់រំកម្ពុជា
# Cambodia School Timetable System

## 📅 រចនាសម្ព័ន្ធកាលវិភាគ | Timetable Structure

### ម៉ោងរៀនស្តង់ដារ | Standard School Hours

#### 🌅 វេនព្រឹក (Morning Session)
```
07:00 - 07:50  |  ម៉ោងទី១ (Period 1)
07:50 - 08:40  |  ម៉ោងទី២ (Period 2)
08:40 - 08:55  |  សម្រាក (Break)
08:55 - 09:45  |  ម៉ោងទី៣ (Period 3)
09:45 - 10:35  |  ម៉ោងទី៤ (Period 4)
10:35 - 11:25  |  ម៉ោងទី៥ (Period 5)
```

#### 🌞 វេនល្ងាច (Afternoon Session)  
```
13:30 - 14:20  |  ម៉ោងទី៦ (Period 6)
14:20 - 15:10  |  ម៉ោងទី៧ (Period 7)
15:10 - 15:25  |  សម្រាក (Break)
15:25 - 16:15  |  ម៉ោងទី៨ (Period 8)
16:15 - 17:05  |  ម៉ោងទី៩ (Period 9)
```

### 📆 ថ្ងៃរៀនក្នុងមួយសប្តាហ៍ | School Days

```
ថ្ងៃច័ន្ទ     (Monday)    - ១
ថ្ងៃអង្គារ    (Tuesday)   - ២
ថ្ងៃពុធ       (Wednesday) - ៣
ថ្ងៃព្រហស្បតិ៍ (Thursday)  - ៤
ថ្ងៃសុក្រ     (Friday)    - ៥
ថ្ងៃសៅរ៍      (Saturday)  - ៦
```

## 📚 តារាងមុខវិជ្ជាតាមកម្រិត | Subject Schedule by Level

### 🎒 បឋមសិក្សា (Primary: Grade 1-6)

**មុខវិជ្ជាចម្បង:**
- គណិតវិទ្យា (Mathematics)
- ភាសាខ្មែរ (Khmer Language)
- វិទ្យាសាស្ត្រ (Science)
- សង្គមវិទ្យា (Social Studies)
- ភាសាអង្គ្លេស (English)
- ពលកម្ម (Physical Education)
- សិល្បៈ (Art)
- ទំនៀមទំលាប់ល្អ (Moral Education)

**ចំនួនម៉ោង/សប្តាហ៍:**
- គណិតវិទ្យា: 6-7 ម៉ោង
- ភាសាខ្មែរ: 7-8 ម៉ោង  
- វិទ្យាសាស្ត្រ: 3-4 ម៉ោង
- សង្គមវិទ្យា: 3 ម៉ោង
- ភាសាអង្គ្លេស: 3-4 ម៉ោង
- ពលកម្ម: 2 ម៉ោង
- សិល្បៈ: 2 ម៉ោង

### 📚 បឋមភូមិ (Lower Secondary: Grade 7-9)

**មុខវិជ្ជាចម្បង:**
- គណិតវិទ្យា (Mathematics)
- រូបវិទ្យា (Physics)
- គីមីវិទ្យា (Chemistry)  
- ជីវវិទ្យា (Biology)
- ភាសាខ្មែរ (Khmer Language)
- ភាសាអង្គ្លេស (English)
- ប្រវត្តិសាស្ត្រ (History)
- ភូមិសាស្ត្រ (Geography)
- ពលកម្ម (Physical Education)
- វិចិត្រសិល្បៈ (Fine Arts)

**ចំនួនម៉ោង/សប្តាហ៍:**
- គណិតវិទ្យា: 5-6 ម៉ោង
- វិទ្យាសាស្ត្រ (រូប គីមី ជីវ): 6-8 ម៉ោង
- ភាសាខ្មែរ: 5 ម៉ោង
- ភាសាអង្គ្លេស: 4 ម៉ោង
- សង្គមវិទ្យា: 4 ម៉ោង

### 🎓 មធ្យមភូមិ (Upper Secondary: Grade 10-12)

**ធារា (Streams):**

#### A. ធារាវិទ្យាសាស្ត្រ (Science Stream)
- គណិតវិទ្យា (Mathematics)
- រូបវិទ្យា (Physics)
- គីមីវិទ្យា (Chemistry)
- ជីវវិទ្យា (Biology)
- ភាសាខ្មែរ
- ភាសាអង្គ្លេស

#### B. ធារាសង្គមវិទ្យា (Social Science Stream)
- គណិតវិទ្យា
- ប្រវត្តិសាស្ត្រ (History)
- ភូមិសាស្ត្រ (Geography)
- សេដ្ឋកិច្ច (Economics)
- ភាសាខ្មែរ
- ភាសាអង្គ្លេស

## 🔧 Technical Implementation

### TimeSlot Model - Cambodia Standard

```python
# Default periods for Cambodia schools
CAMBODIA_PERIODS = [
    # Morning Session
    (1, "07:00", "07:50", "ម៉ោងទី១"),
    (2, "07:50", "08:40", "ម៉ោងទី២"),
    # Break: 08:40-08:55
    (3, "08:55", "09:45", "ម៉ោងទី៣"),
    (4, "09:45", "10:35", "ម៉ោងទី៤"),
    (5, "10:35", "11:25", "ម៉ោងទី៥"),
    
    # Afternoon Session
    (6, "13:30", "14:20", "ម៉ោងទី៦"),
    (7, "14:20", "15:10", "ម៉ោងទី៧"),
    # Break: 15:10-15:25
    (8, "15:25", "16:15", "ម៉ោងទី៨"),
    (9, "16:15", "17:05", "ម៉ោងទី៩"),
]
```

### Days of Week

```python
CAMBODIA_SCHOOL_DAYS = [
    (1, 'ច័ន្ទ', 'Monday'),
    (2, 'អង្គារ', 'Tuesday'),
    (3, 'ពុធ', 'Wednesday'),
    (4, 'ព្រហស្បតិ៍', 'Thursday'),
    (5, 'សុក្រ', 'Friday'),
    (6, 'សៅរ៍', 'Saturday'),
]
```

## 📊 Sample Weekly Timetable

### ថ្នាក់ទី៦ A (Grade 6 A) - បឋមសិក្សា

| ម៉ោង | ច័ន្ទ | អង្គារ | ពុធ | ព្រហស្បតិ៍ | សុក្រ | សៅរ៍ |
|--------|--------|---------|------|-------------|--------|--------|
| **07:00-07:50** | គណិត | ភាសាខ្មែរ | គណិត | វិទ្យា | ភាសាខ្មែរ | គណិត |
| **07:50-08:40** | ភាសាខ្មែរ | គណិត | ភាសាអង់ | គណិត | វិទ្យា | សង្គម |
| *សម្រាក* | | | | | | |
| **08:55-09:45** | វិទ្យា | ភាសាអង់ | សង្គម | ភាសាខ្មែរ | គណិត | ភាសាអង់ |
| **09:45-10:35** | សង្គម | វិទ្យា | ភាសាខ្មែរ | ភាសាអង់ | សង្គម | ពលកម្ម |
| **10:35-11:25** | ភាសាអង់ | សិល្បៈ | គណិត | សិល្បៈ | ពលកម្ម | ទំនៀម |

### ថ្នាក់ទី៩ A (Grade 9 A) - បឋមភូមិ

| ម៉ោង | ច័ន្ទ | អង្គារ | ពុធ | ព្រហស្បតិ៍ | សុក្រ | សៅរ៍ |
|--------|--------|---------|------|-------------|--------|--------|
| **07:00-07:50** | គណិត | រូបវិទ្យា | គណិត | ជីវវិទ្យា | ភាសាខ្មែរ | គណិត |
| **07:50-08:40** | រូបវិទ្យា | គណិត | ភាសាអង់ | គណិត | គីមីវិទ្យា | ប្រវត្តិ |
| *សម្រាក* | | | | | | |
| **08:55-09:45** | ភាសាខ្មែរ | ភាសាអង់ | រូបវិទ្យា | ភាសាខ្មែរ | គណិត | ភាសាអង់ |
| **09:45-10:35** | គីមីវិទ្យា | ជីconsectវិទ្យា | ភាសាខ្មែរ | ភាសាអង់ | ប្រវត្តិ | ភូមិសាស្ត្រ |
| **10:35-11:25** | ភូមិសាស្ត្រ | ប្រវត្តិ | គីមីវិទ្យា | រូបវិទ្យា | ពលកម្ម | សិល្បៈ |

## 🎨 UI Design - Cambodia Style

### Color Coding

```css
/* Subject Colors */
.subject-math { background: #3b82f6; color: white; }        /* គណិតវិទ្យា - Blue */
.subject-khmer { background: #dc2626; color: white; }       /* ភាសាខ្មែរ - Red */
.subject-science { background: #059669; color: white; }     /* វិទ្យា - Green */
.subject-social { background: #d97706; color: white; }      /* សង្គម - Orange */
.subject-english { background: #7c3aed; color: white; }     /* អង់គ្លេស - Purple */
.subject-pe { background: #ea580c; color: white; }          /* ពលកម្ម - Orange-Red */
.subject-art { background: #ec4899; color: white; }         /* សិល្បៈ - Pink */

/* Period Cells */
.period-cell {
    padding: 12px 8px;
    text-align: center;
    border: 1px solid #e5e7eb;
    min-height: 60px;
}

/* Break Time */
.break-row {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    font-weight: 600;
}
```

### Print-Friendly Layout

```css
@media print {
    .no-print { display: none !important; }
    .timetable-print {
        font-size: 11pt;
        color: black !important;
    }
    .subject-cell {
        border: 1px solid #000 !important;
        padding: 8px !important;
    }
}
```

## 📋 Features

### ✅ Already Implemented
- ✓ TimeSlot model with day/period
- ✓ Timetable model linking classroom, subject, teacher
- ✓ Basic timetable list view
- ✓ CRUD operations for admin

### 🔄 To Be Enhanced
- [ ] Cambodia standard time slots (7AM-11AM, 1:30PM-5PM)
- [ ] Saturday included (6-day week)
- [ ] Subject color coding
- [ ] Print-friendly layout
- [ ] Excel export
- [ ] Weekly grid view (primary/secondary optimized)
- [ ] Break time indicators
- [ ] Period labels in Khmer

## 🚀 Implementation Steps

### Step 1: Update TimeSlot Data
```bash
python manage.py shell
from school.models import TimeSlot
from datetime import time

# Clear existing
TimeSlot.objects.all().delete()

# Create Cambodia standard periods
periods = [
    (1, 1, time(7, 0), time(7, 50)),
    (1, 2, time(7, 50), time(8, 40)),
    (1, 3, time(8, 55), time(9, 45)),
    # ... etc
]

for day, period, start, end in periods:
    TimeSlot.objects.create(
        day=day,
        period=period,
        start_time=start,
        end_time=end
    )
```

### Step 2: Update Template
- Add 6-day week support
- Show break times
- Color code subjects
- Make print-friendly

### Step 3: Add Export
- Excel format
- PDF format (optional)
- Print CSS

## 📞 Resources

- [World Bank - Cambodia Instruction Time](https://www.worldbank.org/en/country/cambodia/publication/instruction-time-and-student-learning)
- [MoEYS Curriculum Guidelines](http://www.moeys.gov.kh/)

---

**ចុងក្រោយធ្វើបច្ចុប្បន្នភាព:** ថ្ងៃទី 04/08/2026  
**កំណែ:** 1.0 - Cambodia Timetable System Design

---

**🎓 ប្រព័ន្ធកាលវិភាគស្របតាមប្រព័ន្ធអប់រំកម្ពុជា**
