# Generated by Django 4.0 on 2021-12-13 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_relationship_status'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], max_length=7)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='like',
            new_name='likes',
        ),
        migrations.DeleteModel(
            name='Liked',
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
    ]
