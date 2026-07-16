# Generated migration to change UserProfile.student from OneToOneField to ForeignKey
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_teacher_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='student',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='parent_profiles',
                to='school.student'
            ),
        ),
    ]
