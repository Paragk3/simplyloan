# Generated by Django 4.2.5 on 2023-09-24 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApplications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_id', models.CharField(max_length=50)),
                ('loan_type', models.CharField(choices=[('car', 'Car'), ('home', 'Home'), ('education', 'Education'), ('personal', 'Personal')], max_length=20)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('term_period', models.IntegerField()),
                ('disbursment_date', models.DateField()),
                ('next_due_date', models.DateField()),
                ('emi_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('status', models.CharField(default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=45)),
                ('annual_income', models.IntegerField(verbose_name=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.loanapplications')),
            ],
        ),
        migrations.AddField(
            model_name='loanapplications',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users'),
        ),
        migrations.CreateModel(
            name='CreditScore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('credit_score', models.IntegerField(verbose_name=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
    ]