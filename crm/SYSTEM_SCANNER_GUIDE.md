# System Problem Scanner Guide

## Overview
The System Problem Scanner is a powerful diagnostic tool that checks your School Management System for issues across multiple areas including database integrity, templates, models, URLs, static files, security, and performance.

## How to Use

### Basic Usage

Run a quick scan (essential checks only):
```bash
python manage.py scan_system --quick
```

Run a full scan (all checks):
```bash
python manage.py scan_system --full
```

Or simply:
```bash
python manage.py scan_system
```
(defaults to full scan if no options specified)

### Individual Check Options

You can run specific checks by using these options:

```bash
# Check database integrity
python manage.py scan_system --database

# Check templates for encoding and syntax issues
python manage.py scan_system --templates

# Check model data quality
python manage.py scan_system --models

# Check URL configuration
python manage.py scan_system --urls

# Check static and media files
python manage.py scan_system --static

# Check security settings
python manage.py scan_system --security

# Check performance issues
python manage.py scan_system --performance
```

### Combine Multiple Checks

You can combine multiple check options:
```bash
python manage.py scan_system --database --templates --models
```

### Auto-Fix Mode (Use with Caution)

Some simple issues can be automatically fixed:
```bash
python manage.py scan_system --quick --fix
```

⚠️ **Warning**: Auto-fix mode will attempt to repair simple issues automatically. Always review what will be fixed before running in production.

## What Each Check Does

### 1. Database Check (`--database`)
- ✓ Tests database connectivity
- ✓ Counts tables
- ✓ Finds orphaned students (active students without classroom)
- ✓ Finds classrooms without homeroom teacher
- ✓ Detects inactive academic years with active students

### 2. Template Check (`--templates`)
- ✓ Scans all HTML templates
- ✓ Detects encoding issues (like "???" question marks)
- ✓ Checks for unbalanced Django template tags `{% %}`
- ✓ Checks for unbalanced variable tags `{{ }}`
- ✓ Ignores CSS/JS content to avoid false positives

### 3. Model Data Check (`--models`)
- ✓ Validates student data (names, IDs)
- ✓ Validates teacher data (names, contact info)
- ✓ Checks for non-standard ID formats
- ✓ Finds duplicate IDs
- ✓ Identifies active records missing required relationships

### 4. URL Check (`--urls`)
- ✓ Verifies URL configuration loads properly
- ✓ Checks for essential URL patterns (student_list, teacher_list, dashboard)
- ✓ Reports configuration errors

### 5. Static & Media Check (`--static`)
- ✓ Verifies staticfiles directory exists
- ✓ Verifies images directory exists
- ✓ Verifies documents directory exists
- ✓ Counts files in each directory
- ✓ Can auto-create missing directories with `--fix`

### 6. Security Check (`--security`)
- ✓ Checks if DEBUG mode is OFF (should be OFF in production)
- ✓ Validates SECRET_KEY strength
- ✓ Checks ALLOWED_HOSTS configuration
- ✓ Verifies .env file exists and is excluded from git

### 7. Performance Check (`--performance`)
- ✓ Checks database size
- ✓ Identifies large querysets that may need pagination
- ✓ Suggests optimization opportunities

## Understanding the Output

### Status Icons
- ✓ = Check passed, no issues
- ⚠️ = Warning (non-critical issue)
- ❌ = Critical issue requiring attention

### Summary Report
At the end of each scan, you'll see:
- Total critical issues found
- Total warnings
- List of all issues by category
- Overall system health status

### Health Status Messages
- 🎉 **SYSTEM IS HEALTHY!** - No issues or warnings
- ⚠️ **System operational with X warning(s)** - Working but has warnings
- ❌ **X critical issue(s) need attention** - Has issues requiring fixes

## Examples

### Example 1: Quick Daily Check
```bash
python manage.py scan_system --quick
```
Output:
```
======================================================================
  SYSTEM PROBLEM SCANNER
======================================================================

──────────────────────────────────────────────────────────────────────
  DATABASE CHECK
──────────────────────────────────────────────────────────────────────
✓ Database connected (34 tables)
✓ No database issues found

──────────────────────────────────────────────────────────────────────
  TEMPLATE CHECK
──────────────────────────────────────────────────────────────────────
Scanned 47 templates
✓ All templates OK

──────────────────────────────────────────────────────────────────────
  MODEL DATA CHECK
──────────────────────────────────────────────────────────────────────

======================================================================
  SCAN SUMMARY
======================================================================

✓ NO CRITICAL ISSUES FOUND

🎉 SYSTEM IS HEALTHY!
======================================================================
```

### Example 2: Pre-Deployment Full Scan
```bash
python manage.py scan_system --full
```
Runs all 7 checks before deploying to production.

### Example 3: Troubleshooting Specific Area
If users report display issues:
```bash
python manage.py scan_system --templates
```

If reports show missing data:
```bash
python manage.py scan_system --database --models
```

## When to Run Scans

### Daily/Regular Use
```bash
python manage.py scan_system --quick
```

### Before Deployment
```bash
python manage.py scan_system --full
```

### After Major Changes
- After bulk data imports: `--database --models`
- After template updates: `--templates`
- After settings changes: `--security`

### Troubleshooting
Run specific checks based on the problem:
- Display issues → `--templates`
- Missing data → `--database --models`
- Slow performance → `--performance`
- Access issues → `--urls`

## Tips

1. **Run quick scans regularly** - They complete in seconds and catch most issues
2. **Run full scans before deployment** - Comprehensive check before going live
3. **Use specific checks for troubleshooting** - Faster than full scan
4. **Review warnings** - They indicate potential future issues
5. **Be cautious with --fix** - Always review what will be changed first

## Alternative: Standalone Health Check

For a simpler, non-Django check, you can also run:
```bash
python system_health_check.py
```

This standalone script performs basic health checks without requiring Django management commands.

## Support

If the scanner reports an issue you don't understand:
1. Note the exact error message
2. Note which check reported it (database, templates, etc.)
3. Review the specific section above for that check type
4. Check the system logs for more details

The scanner is designed to help you maintain a healthy system. Regular scans can catch small issues before they become big problems!
