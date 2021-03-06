# Generated by Django 4.0 on 2021-12-14 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='created',
        ),
        migrations.RemoveField(
            model_name='like',
            name='updated',
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(max_length=250, verbose_name='treść'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='data modyfikacji'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='treść'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='data modyfikacji'),
        ),
    ]
