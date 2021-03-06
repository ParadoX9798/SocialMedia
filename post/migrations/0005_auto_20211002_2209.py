# Generated by Django 3.2.7 on 2021-10-02 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0004_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plike', to='post.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user_like',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ulike', to=settings.AUTH_USER_MODEL),
        ),
    ]
