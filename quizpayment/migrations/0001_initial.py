# Generated by Django 4.0.6 on 2022-09-26 12:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizopen', '0001_initial'),
        ('quizstart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizpaymentResponseAPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_params', models.CharField(blank=True, max_length=2055, null=True)),
                ('creation', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuizpaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('PAID', 'PAID'), ('UNPAID', 'UNPAID')], default='UNPAID', max_length=1055, null=True)),
                ('payment_game_status', models.CharField(blank=True, choices=[('PLAYED', 'PLAYED'), ('UNPLAYED', 'UNPLAYED')], default='UNPLAYED', max_length=1055, null=True)),
                ('payment_type_value', models.CharField(blank=True, default='6', max_length=1055, null=True)),
                ('total_price', models.CharField(blank=True, max_length=1055, null=True)),
                ('order_id', models.CharField(blank=True, max_length=1055, null=True)),
                ('result_code', models.CharField(blank=True, max_length=1055, null=True)),
                ('txn_id', models.CharField(blank=True, max_length=1055, null=True)),
                ('checksum', models.CharField(blank=True, max_length=1055, null=True)),
                ('creation', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('quizopen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizopen.quizopenmodel')),
                ('quizstart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizstart.quizstartmodel')),
            ],
        ),
        migrations.CreateModel(
            name='QuizpaymentItsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('PAID', 'PAID'), ('UNPAID', 'UNPAID')], default='UNPAID', max_length=1055, null=True)),
                ('payment_game_status', models.CharField(blank=True, choices=[('PLAYED', 'PLAYED'), ('UNPLAYED', 'UNPLAYED')], default='UNPLAYED', max_length=1055, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=1055, null=True)),
                ('payment_type_value', models.CharField(blank=True, default='1', max_length=1055, null=True)),
                ('creation', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('quizopen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizopen.quizopenmodel')),
                ('quizstart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizstart.quizstartmodel')),
            ],
        ),
    ]
