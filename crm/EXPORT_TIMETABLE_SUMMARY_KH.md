# សង្ខេបការបន្ថែម Export/Print និងកាលវិភាគកម្ពុជា
## Export/Print Features & Cambodia Timetable System

---

## ✅ អ្វីដែលបានធ្វើរួច

### 1️⃣ **Export/Print Buttons នៅ Topbar**

បានបន្ថែម buttons នៅ topbar សម្រាប់គ្រប់ទំព័រ:
- ✅ **Excel Export** - នាំចេញជា CSV/Excel format
- ✅ **Print** - បោះពុម្ពដោយផ្ទាល់
- ✅ Responsive design (លាក់នៅលើ mobile)
- ✅ Cambodia colors (green Excel, blue Print)

**របៀបប្រើ:**
```html
{% block top_actions %}
<button onclick="exportToExcel()" class="top-btn success">
  <i class="bi bi-file-earmark-excel"></i>
  <span>Excel</span>
</button>
<button onclick="window.print()" class="top-btn">
  <i class="bi bi-printer"></i>
  <span>Print</span>
</button>
{% endblock %}
```

**ត្រូវបានបន្ថែមនៅ:**
- ✓ Student List (បញ្ជីសិស្ស)
- ✓ Timetable (កាលវិភាគ)
- អាចបន្ថែមនៅទំព័រផ្សេងៗទៀត

---

### 2️⃣ **Cambodia Standard Timetable Structure**

បានបង្កើតរចនាសម្ព័ន្ធកាលវិភាគស្តង់ដារកម្ពុជា:

#### 📅 **រចនាសម្ព័ន្ធម៉ោង**

**វេនព្រឹក (Morning Session):**
```
07:00 - 07:50  |  ម៉ោងទី១
07:50 - 08:40  |  ម៉ោងទី២
08:40 - 08:55  |  សម្រាក (Break)
08:55 - 09:45  |  ម៉ោងទី៣
09:45 - 10:35  |  ម៉ោងទី៤
10:35 - 11:25  |  ម៉ោងទី៥
```

**វេនល្ងាច (Afternoon Session):**
```
13:30 - 14:20  |  ម៉ោងទី៦
14:20 - 15:10  |  ម៉ោងទី៧
15:10 - 15:25  |  សម្រាក (Break)
15:25 - 16:15  |  ម៉ោងទី៨
16:15 - 17:05  |  ម៉ោងទី៩
```

**ថ្ងៃរៀន:** ច័ន្ទ - សៅរ៍ (6 ថ្ងៃ)

---

### 3️⃣ **Management Command - Setup Timetable**

បានបង្កើត command ដើម្បី setup timeslots:

```bash
python manage.py setup_cambodia_timetable
```

**លទ្ធផល:**
- ✓ បង្កើត 54 time slots (9 periods × 6 days)
- ✓ ម៉ោងត្រឹមត្រូវតាមប្រព័ន្ធកម្ពុជា
- ✓ រួមទាំងថ្ងៃសៅរ៍
- ✓ លុបកាលវិភាគចាស់ទាំងអស់

---

### 4️⃣ **Weekly Grid View - ប្រភេទកម្ពុជា**

បានបង្កើតតារាងកាលវិភាគរាប់សប្តាហ៍:

#### 🎨 **ការរចនា (Design)**

**ពណ៌ Cambodia School:**
- 🔵 Blue header: `#003893` (ពណ៌ធង់ជាតិ)
- 🔴 Red border: `#e00025` (ពណ៌ធង់ជាតិ)
- 🟡 Gold break: `#ffd700` (សម្រាប់ពេលសម្រាក)

**ពណ៌មុខវិជ្ជា (Subject Colors):**
```css
គណិតវិទ្យា (Math)     - Blue #3b82f6
ភាសាខ្មែរ (Khmer)      - Red #dc2626
វិទ្យាសាស្ត្រ (Science)  - Green #10b981
សង្គមវិទ្យា (Social)    - Orange #f59e0b
ភាសាអង់គ្លេស (English) - Purple #8b5cf6
ពលកម្ម (PE)            - Orange-Red #f97316
សិល្បៈ (Art)           - Pink #ec4899
រូបវិទ្យា (Physics)    - Cyan #06b6d4
គីមីវិទ្យា (Chemistry)  - Teal #14b8a6
ជីវៈវិទ្យា (Biology)    - Lime #84cc16
```

#### 📊 **Layout**

```
┌────────────────────────────────────────────────────┐
│ Header (Blue Cambodia colors + Red border)        │
├────────────────────────────────────────────────────┤
│ Filter (Select Classroom + Year)                  │
├─────┬──────┬──────┬──────┬──────┬──────┬──────────┤
│ម៉ោង│ ច័ន្ទ │អង្គារ│  ពុធ │ព្រហ.│ សុក្រ│  សៅរ៍   │
├─────┼──────┼──────┼──────┼──────┼──────┼──────────┤
│  ១  │Subject│      │      │      │      │          │
│07-08│Teacher│      │      │      │      │          │
├─────┼──────┼──────┼──────┼──────┼──────┼──────────┤
│  ២  │      │      │      │      │      │          │
│08-09│      │      │      │      │      │          │
├─────┴──────┴──────┴──────┴──────┴──────┴──────────┤
│      សម្រាក (Break) 08:40 - 08:55                │
├─────┬──────┬──────┬──────┬──────┬──────┬──────────┤
│  ៣  │      │      │      │      │      │          │
│     │      │      │      │      │      │          │
└─────┴──────┴──────┴──────┴──────┴──────┴──────────┘
```

---

### 5️⃣ **Excel Export Function**

បានបន្ថែម JavaScript function សម្រាប់ export:

```javascript
function exportToExcel() {
  // Convert table to CSV
  // UTF-8 BOM for Khmer support
  // Auto download
}
```

**Features:**
- ✓ UTF-8 encoding (support Khmer characters)
- ✓ CSV format (open in Excel)
- ✓ Auto-download
- ✓ Include all timetable data

---

### 6️⃣ **Print-Friendly Styles**

```css
@media print {
  /* Hide navigation */
  .no-print, .top, .sb { display: none !important; }
  
  /* Full width */
  .main { margin-left: 0 !important; }
  
  /* A4 Landscape */
  @page { size: A4 landscape; }
  
  /* Smaller fonts */
  .weekly-grid { font-size: 9pt; }
}
```

---

## 📁 Files ដែលបានបង្កើត/កែប្រែ

### បង្កើតថ្មី (New Files):
1. **`school/management/commands/setup_cambodia_timetable.py`**
   - Management command setup timeslots

2. **`school/templates/school/timetable_grid.html`**
   - Weekly grid view template

3. **`CAMBODIA_TIMETABLE_SYSTEM.md`**
   - Documentation ពេញលេញ

4. **`EXPORT_TIMETABLE_SUMMARY_KH.md`**
   - ឯកសារនេះ (summary)

### កែប្រែ (Modified Files):
1. **`school/templates/school/base.html`**
   - បន្ថែម `{% block top_actions %}{% endblock %}`
   - បន្ថែម `.top-btn` CSS styles

2. **`school/templates/school/student_list.html`**
   - បន្ថែម Export/Print buttons

3. **`school/templates/school/timetable_list.html`**
   - កែទៅជា Cambodia style

4. **`school/views.py`**
   - Update `timetable_list` view
   - បន្ថែម periods និង period_times

---

## 🎯 របៀបប្រើប្រាស់

### 1. Setup Cambodia Timetable (ដំបូងតែម្តង)

```bash
cd d:\Monday-Friday-Year3S1\Monday\python\crm
python manage.py setup_cambodia_timetable
```

### 2. មើលកាលវិភាគ

1. ចូលទៅ **School → តារាងម៉ោង**
2. ជ្រើសរើស **ថ្នាក់រៀន**
3. (Optional) ជ្រើសរើស **ឆ្នាំសិក្សា**
4. ចុច **បង្ហាញតារាង**

### 3. Export ឬ Print

**នៅលើ topbar:**
- 🟢 ចុច **Excel** → Export CSV file
- 🔵 ចុច **Print** → Print preview

### 4. បន្ថែម Timetable Entries

1. ចូលទៅ **Admin Panel**
2. ជ្រើស **Timetable → Add**
3. បំពេញ:
   - Classroom
   - Subject
   - Teacher
   - Time Slot (ម៉ោងទី១-៩, ថ្ងៃច័ន្ទ-សៅរ៍)
   - Room (optional)
4. Save

---

## 📊 ឧទាហរណ៍កាលវិភាគ

### ថ្នាក់ទី៦ A - បឋមសិក្សា

| ម៉ោង | ច័ន្ទ | អង្គារ | ពុធ | ព្រហស្បតិ៍ | សុក្រ | សៅរ៍ |
|--------|--------|---------|------|-------------|--------|--------|
| **១** 07:00 | គណិត | ភាសាខ្មែរ | គណិត | វិទ្យា | ភាសាខ្មែរ | គណិត |
| **២** 07:50 | ភាសាខ្មែរ | គណិត | អង់គ្លេស | គណិត | វិទ្យា | សង្គម |
| **សម្រាក** | | | | | | |
| **៣** 08:55 | វិទ្យា | អង់គ្លេស | សង្គម | ភាសាខ្មែរ | គណិត | អង់គ្លេស |
| **៤** 09:45 | សង្គម | វិទ្យា | ភាសាខ្មែរ | អង់គ្លេស | សង្គម | ពលកម្ម |
| **៥** 10:35 | អង់គ្លេស | សិល្បៈ | គណិត | សិល្បៈ | ពលកម្ម | ទំនៀម |

---

## 🔧 Technical Details

### Database Changes
```
TimeSlot model:
- day: 1-6 (Monday-Saturday)
- period: 1-9
- start_time: time field
- end_time: time field
```

### View Logic
```python
periods = [1, 2, 'break1', 3, 4, 5, 6, 7, 'break2', 8, 9]

period_times = {
    1: '07:00-07:50',
    2: '07:50-08:40',
    # ... etc
}
```

### Template Logic
```django
{% for period in periods %}
  {% if period == 'break1' %}
    <!-- Break row -->
  {% else %}
    <!-- Period row with 6 day columns -->
  {% endif %}
{% endfor %}
```

---

## 🎨 Customization

### កែពណ៌ (Change Colors)

នៅក្នុង template CSS:
```css
:root {
  --cam-blue: #003893;  /* Header color */
  --cam-red: #e00025;   /* Border color */
  --cam-gold: #ffd700;  /* Break color */
}
```

### បន្ថែមមុខវិជ្ជាថ្មី (Add New Subject Color)

```css
.subject-economics { 
  background: linear-gradient(135deg, #6366f1, #4f46e5); 
  color: white; 
}
```

### កែម៉ោង (Change Time)

ដំណើរការ command ម្តងទៀត:
```bash
python manage.py setup_cambodia_timetable
```

---

## 📞 Support & Resources

### Documentation
- `CAMBODIA_TIMETABLE_SYSTEM.md` - Full technical documentation
- `CAMBODIA_PROMOTION_SYSTEM.md` - Promotion system
- `API_DOCUMENTATION.md` - API reference

### ឯកសារយោង
- [World Bank - Cambodia Instruction Time](https://www.worldbank.org/en/country/cambodia/publication/instruction-time-and-student-learning)
- [MoEYS Cambodia](http://www.moeys.gov.kh/)

---

## ✨ Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| **Export Excel** | ✅ | នាំចេញ CSV/Excel with Khmer |
| **Print** | ✅ | Print-friendly layout |
| **Cambodia Hours** | ✅ | 7AM-11AM, 1:30PM-5PM |
| **6-Day Week** | ✅ | Monday-Saturday |
| **9 Periods** | ✅ | 5 morning + 4 afternoon |
| **2 Breaks** | ✅ | Morning & afternoon |
| **Subject Colors** | ✅ | 10+ predefined colors |
| **Weekly Grid** | ✅ | Visual timetable |
| **Auto-Setup** | ✅ | Management command |
| **Responsive** | ✅ | Mobile-friendly |

---

## 🚀 Next Steps (Optional)

### អាចធ្វើបន្ថែម:

1. **PDF Export**
   - Generate PDF with school logo
   - Better formatting

2. **Teacher View**
   - Show all classes for one teacher
   - Personal schedule

3. **Conflict Detection**
   - Check double-booking
   - Teacher availability

4. **Statistics**
   - Hours per subject
   - Teacher workload

---

**ចុងក្រោយធ្វើបច្ចុប្បន្នភាព:** ថ្ងៃទី 04/08/2026  
**កំណែ:** 1.0  
**Status:** ✅ រួចរាល់ និង Deployed

---

**🎓 ប្រព័ន្ធកាលវិភាគស្របតាមប្រព័ន្ធអប់រំកម្ពុជា ✅**  
**📊 Export/Print មានស្រាប់នៅ Topbar ✅**
