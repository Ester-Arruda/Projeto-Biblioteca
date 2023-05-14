# Generated by Django 4.1.7 on 2023-03-19 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0012_alter_emprestimos_nome_emprestado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimos',
            name='tempo_duracao',
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='data_devolucao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='data_emprestimo',
            field=models.DateField(blank=True, null=True),
        ),
    ]
