# Timetable Interface Update

## Overview
Updated the timetable interface to provide a clean, modern, and easy-to-use experience similar to the reference design provided.

## Key Features

### 1. **Modern Header Design**
- Gradient background with clear title and description
- Prominent "Add New" button for admins
- Clean, professional appearance

### 2. **Enhanced Filters**
- Larger, more accessible filter controls
- Classroom and Academic Year filters
- Auto-submit on selection for better UX
- Clear visual hierarchy with icons

### 3. **Dual View Modes**

#### List View (Default)
- Organized by day of the week
- Clean table layout with:
  - Period numbers with gradient badges
  - Time display (start - end)
  - Subject names (bold and prominent)
  - Teacher information with icons
  - Classroom and room information
  - Action buttons (Edit/Delete for admins only)
- Day headers with:
  - Day name in Khmer
  - Total period count badge
  - Calendar icon

#### Grid View
- Card-based layout
- Responsive grid (adapts to screen size)
- Shows periods as individual items
- Compact display ideal for mobile devices

### 4. **Visual Improvements**
- Color-coded period badges (gradient blue)
- Hover effects on table rows
- Modern rounded corners and shadows
- Consistent spacing and typography
- Icon-based action buttons with hover states

### 5. **Responsive Design**
- Works seamlessly on all screen sizes
- Grid view automatically adjusts columns
- Mobile-friendly touch targets
- Clean empty state with guidance

### 6. **Role-Based Display**
- Admins see all action buttons (Edit/Delete)
- Teachers and Students see read-only view
- Automatic filtering for students (shows only their class schedule)

## Color Scheme

The interface uses your existing CSS variables:
- `--ac`: Primary color (default: #2563eb - Blue)
- `--ac2`: Secondary color (default: #7c3aed - Purple)
- `--mu`: Muted text color (#64748b)
- `--tx`: Primary text color (#1e293b)
- `--br`: Border color (#e2e8f0)

## Technical Details

### Files Modified
- `school/templates/school/timetable_list.html` - Complete redesign with dual view modes

### JavaScript Features
- View switcher function (`switchView`)
- Tab state management
- Smooth transitions between views

### CSS Features
- Custom styling for timetable components
- Gradient backgrounds and badges
- Hover effects and animations
- Responsive breakpoints
- Print-friendly styles

## Usage

### Switching Views
Click the tab buttons at the top:
- **បញ្ជី (List)** - Detailed table view
- **ក្រឡា (Grid)** - Compact card view

### Filtering
1. Select a classroom from the dropdown
2. Select an academic year (optional)
3. Results update automatically

### Admin Actions
Admins can:
- Add new timetable entries via the "បន្ថែមថ្មី" button
- Edit entries using the pencil icon
- Delete entries using the trash icon

## Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Responsive design works on all screen sizes

## Future Enhancements (Optional)
- Weekly calendar grid view
- Conflict detection (same teacher, two places)
- Drag-and-drop period rearrangement
- PDF export of timetables
- Color coding by subject
- Teacher availability tracking

## Notes
- The interface maintains consistency with your existing design system
- All Khmer text is preserved and properly displayed
- The design is print-friendly (hides unnecessary elements when printing)
- Empty states provide helpful guidance to users
