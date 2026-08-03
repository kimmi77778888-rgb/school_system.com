# System Scanner - Quick Reference Card

## 🚀 Quick Commands

### Most Common
```bash
# Quick daily check (recommended)
python manage.py scan_system --quick

# Full comprehensive scan
python manage.py scan_system --full

# Or simply
python manage.py scan_system
```

### Specific Checks
```bash
--database     # Check DB integrity
--templates    # Check HTML templates
--models       # Check data quality
--urls         # Check URL config
--static       # Check files
--security     # Check security
--performance  # Check performance
```

### Auto-Fix Mode
```bash
python manage.py scan_system --quick --fix
```
⚠️ Use with caution!

---

## 📊 Understanding Output

| Icon | Meaning |
|------|---------|
| ✓    | All good |
| ⚠️    | Warning (non-critical) |
| ❌    | Critical issue |

### Status Messages
- 🎉 **SYSTEM IS HEALTHY** = Perfect!
- ⚠️ **X warning(s)** = Working, but attention needed
- ❌ **X critical issue(s)** = Fix required

---

## 🔍 What Gets Checked

### Database (--database)
- Connectivity
- Orphaned records
- Missing relationships
- Data integrity

### Templates (--templates)
- Encoding issues
- Syntax errors
- Tag balance

### Models (--models)
- Missing names
- Invalid IDs
- Duplicates
- Contact info

### URLs (--urls)
- Config loaded
- Essential patterns
- Errors

### Static Files (--static)
- Directory exists
- File counts

### Security (--security)
- DEBUG mode
- SECRET_KEY
- ALLOWED_HOSTS
- .env file

### Performance (--performance)
- Database size
- Query optimization
- Pagination needs

---

## 💡 When to Use

| Scenario | Command |
|----------|---------|
| Daily check | `--quick` |
| Before deploy | `--full` |
| Display issues | `--templates` |
| Data problems | `--database --models` |
| Slow system | `--performance` |
| After updates | `--full` |

---

## 📋 Current System Health

**Last Scan**: All checks passed ✓

**Warnings**: 3 minor (non-critical)
1. One student with old ID format
2. One teacher missing contact info  
3. ALLOWED_HOSTS needs production config

**Critical Issues**: None ✓

---

## 📖 Full Documentation

See `SYSTEM_SCANNER_GUIDE.md` for complete details.

---

## 🎯 Pro Tips

1. ✓ Run `--quick` daily (takes seconds)
2. ✓ Run `--full` before deployment
3. ✓ Use specific checks to troubleshoot
4. ⚠️ Review warnings regularly
5. ⚠️ Be careful with `--fix` mode

---

**Questions?** Check the full guide: `SYSTEM_SCANNER_GUIDE.md`
