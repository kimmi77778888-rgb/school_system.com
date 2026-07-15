"""Fix all templates: add {% load school_tags %} after {% extends %} if missing."""
import os
import glob

template_dir = os.path.join(os.path.dirname(__file__), 'school', 'templates')
files = glob.glob(os.path.join(template_dir, '**', '*.html'), recursive=True)

fixed = 0
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "extends 'school/base.html'" in content and 'load school_tags' not in content:
        content = content.replace(
            "{% extends 'school/base.html' %}",
            "{% extends 'school/base.html' %}\n{% load school_tags %}"
        )
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {os.path.relpath(fpath, template_dir)}")
        fixed += 1

print(f"\nDone. Fixed {fixed} templates.")
