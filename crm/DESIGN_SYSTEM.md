# Design System - Timetable Interface

## Color Palette

### Primary Colors
```css
--ac: #2563eb         /* Primary Blue - Buttons, badges, links */
--ac2: #7c3aed        /* Secondary Purple - Gradients, accents */
--tx: #1e293b         /* Text Primary - Main content */
--mu: #64748b         /* Text Muted - Secondary text */
--br: #e2e8f0         /* Border - Dividers, borders */
--bg: #f1f5f9         /* Background - Page background */
--card: #ffffff       /* Card - Card backgrounds */
```

### Status Colors
```css
Present:  #dcfce7 / #166534  (Light green / Dark green)
Absent:   #fee2e2 / #991b1b  (Light red / Dark red)
Late:     #fef9c3 / #854d0e  (Light yellow / Dark yellow)
Excused:  #dbeafe / #1e40af  (Light blue / Dark blue)
```

### Gradient Combinations
```css
Primary Gradient:     linear-gradient(135deg, #2563eb, #764ba2)
Header Gradient:      linear-gradient(135deg, #667eea, #764ba2)
Badge Gradient:       linear-gradient(135deg, #3b82f6, #2563eb)
Success Gradient:     linear-gradient(135deg, #059669, #065f46)
Warning Gradient:     linear-gradient(135deg, #d97706, #92400e)
```

## Typography

### Font Family
```css
Primary: 'Noto Sans Khmer' (Khmer text)
Secondary: 'Inter' (English text)
Fallback: sans-serif
```

### Font Sizes
```css
Page Title:       1.1rem   (Large headings)
Card Header:      0.92rem  (Card titles)
Body Text:        0.82rem  (Normal text)
Small Text:       0.75rem  (Labels, captions)
Tiny Text:        0.68rem  (Table headers)
```

### Font Weights
```css
Extra Bold:  900  (Page titles)
Bold:        700  (Headings, labels)
Semi-Bold:   600  (Buttons, emphasized text)
Medium:      500  (Navigation)
Regular:     400  (Body text)
Light:       300  (Muted text)
```

## Spacing

### Padding Scale
```css
xs:   4px    (Badge padding)
sm:   8px    (Button padding)
md:   12px   (Card padding)
lg:   18px   (Container padding)
xl:   24px   (Section padding)
2xl:  32px   (Large sections)
```

### Margin Scale
```css
xs:   4px    (Tight spacing)
sm:   8px    (Default spacing)
md:   16px   (Medium spacing)
lg:   24px   (Large spacing)
xl:   32px   (Section separation)
```

### Gap (Flexbox/Grid)
```css
xs:   0.5rem  (4px - Tight elements)
sm:   0.75rem (6px - Close elements)
md:   1rem    (8px - Normal spacing)
lg:   1.5rem  (12px - Comfortable spacing)
```

## Border Radius

### Radius Scale
```css
Small:    6px   (Badges, small elements)
Default:  8px   (Buttons, inputs)
Medium:   10px  (Small cards)
Large:    12px  (Cards, main containers)
X-Large:  18px  (Featured elements)
Circle:   50%   (Avatars, circular elements)
Pill:     20px  (Status badges)
```

## Shadows

### Box Shadow Scale
```css
Subtle:   0 1px 2px rgba(0,0,0,0.05)
Light:    0 2px 4px rgba(0,0,0,0.05)
Default:  0 2px 8px rgba(0,0,0,0.08)
Medium:   0 4px 16px rgba(0,0,0,0.12)
Heavy:    0 8px 32px rgba(0,0,0,0.24)
```

### Focus Shadow
```css
Primary:  0 0 0 3px rgba(37, 99, 235, 0.12)
Success:  0 0 0 3px rgba(5, 150, 105, 0.12)
Danger:   0 0 0 3px rgba(239, 68, 68, 0.12)
```

## Components

### Header
```css
Background:     linear-gradient(135deg, #667eea, #764ba2)
Color:          white
Padding:        2rem
Border Radius:  12px
Shadow:         0 4px 6px rgba(0,0,0,0.1)
```

### Filter Card
```css
Background:     white
Border:         1px solid #e5e7eb
Border Radius:  12px
Padding:        1.25rem
Shadow:         0 2px 4px rgba(0,0,0,0.05)
```

### Day Section Card
```css
Background:     white
Border:         1px solid #e5e7eb
Border Radius:  12px
Shadow:         0 2px 8px rgba(0,0,0,0.08)
Overflow:       hidden
```

### Day Header
```css
Background:     linear-gradient(135deg, #f8fafc, #f1f5f9)
Border Bottom:  2px solid #e5e7eb
Padding:        1rem 1.5rem
Font Weight:    600
Color:          #1e293b
```

### Period Badge
```css
Background:     linear-gradient(135deg, #3b82f6, #2563eb)
Color:          white
Padding:        0.5rem 0.75rem
Border Radius:  8px
Font Weight:    600
Font Size:      0.875rem
Min Width:      50px
```

### Action Buttons
```css
Width:          36px
Height:         36px
Border Radius:  8px
Border:         1px solid #e5e7eb
Background:     white
Color:          #64748b

Hover (Edit):
  Background:   #3b82f6
  Color:        white

Hover (Delete):
  Background:   #ef4444
  Color:        white
```

### View Tabs
```css
Background:     white
Padding:        0.5rem
Border Radius:  12px
Shadow:         0 2px 4px rgba(0,0,0,0.05)

Tab Button:
  Padding:      0.75rem 1rem
  Border Radius: 8px
  Font Weight:  500

Active Tab:
  Background:   linear-gradient(135deg, #667eea, #764ba2)
  Color:        white
```

## Buttons

### Primary Button
```css
Background:     #2563eb
Color:          white
Padding:        0.5rem 1rem
Border Radius:  8px
Font Weight:    600
Font Size:      0.82rem

Hover:
  Background:   #1d4ed8
  Transform:    translateY(-1px)
```

### Secondary Button
```css
Background:     transparent
Border:         1px solid #e5e7eb
Color:          #64748b
Padding:        0.5rem 1rem
Border Radius:  8px
Font Weight:    600

Hover:
  Background:   #f8fafc
```

### Small Button
```css
Padding:        0.28rem 0.65rem
Font Size:      0.75rem
```

## Forms

### Input/Select
```css
Border:         1px solid #e2e8f0
Border Radius:  8px
Padding:        7px 11px
Font Size:      0.82rem

Focus:
  Border Color: #2563eb
  Shadow:       0 0 0 3px rgba(37, 99, 235, 0.12)
```

### Label
```css
Font Weight:    700
Font Size:      0.78rem
Color:          #374151
Margin Bottom:  4px
```

## Tables

### Table Header
```css
Background:     #f8fafc
Color:          #64748b
Font Weight:    600
Font Size:      0.68rem
Text Transform: uppercase
Letter Spacing: 0.5px
Padding:        0.875rem 1rem
Border Bottom:  2px solid #e5e7eb
```

### Table Row
```css
Border Bottom:  1px solid #f1f5f9
Padding:        1rem

Hover:
  Background:   #f8fafc
```

### Table Cell
```css
Padding:        1rem
Font Size:      0.82rem
Vertical Align: middle
```

## Responsive Breakpoints

### Desktop (> 992px)
```css
Main Padding:   calc(56px + 22px) 22px 44px
Sidebar:        260px (expanded)
Font Size:      13.5px (base)
```

### Tablet (768px - 992px)
```css
Main Padding:   calc(56px + 18px) 16px 76px
Font Size:      13px (base)
Some columns hidden
```

### Mobile (< 768px)
```css
Main Padding:   calc(52px + 12px) 10px 58px
Sidebar:        Hidden/Overlay
Bottom Nav:     Visible
Font Size:      13px (base)
Single column layouts
```

### Small Mobile (< 480px)
```css
Main Padding:   calc(52px + 10px) 8px 58px
Font Size:      13px (base)
Very compact layouts
Hide less critical columns
```

## Icons

### Icon Sizes
```css
Extra Small:  0.75rem   (Inline icons)
Small:        0.88rem   (Navigation)
Default:      1rem      (General use)
Large:        1.25rem   (Headers)
X-Large:      2rem      (Feature icons)
```

### Icon Spacing
```css
With Text:    margin-right: 0.5rem
In Button:    margin-right: 0.25rem
In Badge:     margin-right: 0.25rem
```

## Animations

### Transitions
```css
Fast:       0.15s   (Hover effects)
Default:    0.2s    (General transitions)
Medium:     0.3s    (Sidebar, modals)
Slow:       0.5s    (Page transitions)
```

### Easing Functions
```css
Default:    ease
Smooth:     cubic-bezier(0.4, 0, 0.2, 1)
Bounce:     cubic-bezier(0.34, 1.2, 0.64, 1)
```

### Hover Effects
```css
Transform:  translateY(-1px)
Scale:      scale(1.05)
Shadow:     Increase shadow intensity
Color:      Brighten/darken colors
```

## Accessibility

### Minimum Touch Targets
```css
Mobile:     44px × 44px
Desktop:    36px × 36px
```

### Contrast Ratios
```css
Normal Text:    4.5:1 (WCAG AA)
Large Text:     3:1 (WCAG AA)
Icons:          4.5:1
```

### Focus Indicators
```css
Outline:    2px solid #2563eb
Offset:     2px
Shadow:     0 0 0 3px rgba(37, 99, 235, 0.12)
```

## Print Styles

### Page Setup
```css
Background:     white
Font Size:      11px
No shadows
No animations
```

### Hide on Print
```css
- Sidebar
- Top navigation
- Bottom navigation
- Action buttons
- Background images
```

### Show on Print
```css
- School header
- Page title
- Content
- Table borders
```

## Usage Guidelines

### When to Use Gradients
✅ Headers and hero sections
✅ Primary action buttons
✅ Feature badges
✅ Avatars and icons
❌ Body text backgrounds
❌ Form inputs
❌ Regular cards

### When to Use Shadows
✅ Cards and containers
✅ Dropdown menus
✅ Modal dialogs
✅ Focus states
❌ Flat buttons
❌ Background elements
❌ Disabled elements

### When to Use Icons
✅ Navigation items
✅ Action buttons
✅ Status indicators
✅ Input prefixes
❌ Alone without context
❌ Decorative only
❌ Too many at once

## Customization

### How to Change Colors
1. Edit `base.html` CSS variables:
```css
:root {
  --ac: #2563eb;      /* Your primary color */
  --ac2: #7c3aed;     /* Your secondary color */
}
```

2. Or use School Settings admin panel

### How to Change Typography
1. Update Google Fonts import in `base.html`
2. Change `font-family` in root styles
3. Adjust font sizes if needed

### How to Adjust Spacing
1. Modify padding/margin values in components
2. Use consistent spacing scale
3. Test on different screen sizes

---

**This design system ensures:**
- ✅ Visual consistency
- ✅ Easy maintenance
- ✅ Scalability
- ✅ Accessibility
- ✅ Brand identity
