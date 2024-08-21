# Generated by Django 4.2.9 on 2024-01-25 07:35

import article.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_articlepost_user_like_alter_articlepost_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 25, 7, 35, 19, 340478, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentator', models.CharField(max_length=90)),
                ('body', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=article.models.Comment.on_delete, related_name='comments', to='article.articlepost')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
