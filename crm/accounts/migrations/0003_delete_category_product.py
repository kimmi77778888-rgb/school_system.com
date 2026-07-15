from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_product'),
    ]

    operations = [
        migrations.DeleteModel(name='Product'),
        migrations.DeleteModel(name='Category'),
    ]
