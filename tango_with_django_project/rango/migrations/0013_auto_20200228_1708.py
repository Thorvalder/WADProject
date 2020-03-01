# Generated by Django 2.2.3 on 2020-02-28 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0012_picture_saves'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='STYLE',
            new_name='STYLE_1',
        ),
        migrations.AddField(
            model_name='artist',
            name='STYLE_2',
            field=models.CharField(blank=True, choices=[(1, 'Nature'), (2, 'Cartoon'), (3, 'Abstract'), (4, 'Geometric'), (5, 'Realism'), (6, 'Tribal'), (7, 'Sleave'), (8, 'Writing'), (9, 'Non-english Writing'), (10, 'Other')], max_length=20),
        ),
        migrations.AddField(
            model_name='artist',
            name='STYLE_3',
            field=models.CharField(blank=True, choices=[(1, 'Nature'), (2, 'Cartoon'), (3, 'Abstract'), (4, 'Geometric'), (5, 'Realism'), (6, 'Tribal'), (7, 'Sleave'), (8, 'Writing'), (9, 'Non-english Writing'), (10, 'Other')], max_length=20),
        ),
    ]
