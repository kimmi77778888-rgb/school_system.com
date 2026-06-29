import json

with open('data_export.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

image_fields = ['photo', 'logo', 'favicon']
count = 0
for item in data:
    fields = item.get('fields', {})
    for field in image_fields:
        if field in fields and fields[field]:
            print(f"Clearing {item['model']}.{field} = {fields[field]}")
            fields[field] = ''
            count += 1

with open('data_export.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Done! Cleared {count} image paths from export.")
