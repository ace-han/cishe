from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from cishe.account.models import UserModel


# leave it class to front end
# class ContractSource(Enum):
#     KF = 'kf'
#     SAF = 'saf'
#     SITE_VISIT = 'site_visit'


class Customer(models.Model):
    name = models.CharField(max_length=32)
    phone_num = PhoneNumberField()
    phone_num2 = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    parent_phone_num = PhoneNumberField(blank=True)
    parent_type = models.CharField(max_length=8, blank=True)
    university = models.CharField(max_length=32)
    department = models.CharField(max_length=32, blank=True)
    major = models.CharField(max_length=32, blank=True)

    class Meta:
        unique_together = [("phone_num",)]


class Contract(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contract_num = models.CharField(max_length=16, blank=True)
    contract_type = models.CharField(max_length=8)
    source = models.CharField(max_length=8, blank=True)
    signing_date = models.DateTimeField()
    signing_branch = models.CharField(max_length=4, blank=True)
    sale_agent = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    probation_until = models.DateTimeField()
    total_amount = models.PositiveIntegerField()
    referrer = models.CharField(max_length=32, blank=True)
    supplementary_agreement = models.TextField(blank=True)

    class Meta:
        unique_together = [("contract_num",)]


class ServiceInfo(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, unique=True)
    enrollment_semester = models.CharField(max_length=4)
    retention_statement = models.CharField(max_length=32, blank=True)
    target_country_code = models.CharField(max_length=32)  # concat with comma s
    target_subject = models.CharField(max_length=4)
    target_degree = models.CharField(max_length=4)
    target_major = models.CharField(max_length=32)  # concat with comma s
    team = models.CharField(max_length=4)
    workload = models.FloatField()
    status = models.CharField(max_length=32, blank=True)
    start_date = models.DateTimeField()
    remark = models.TextField(blank=True)  # including workload remark


class TakeOver(models.Model):
    counselor = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    transfer_date = models.DateTimeField()
    remark = models.TextField(blank=True)

    class Meta:
        unique_together = (
            (
                "counselor",
                "contract",
            ),
        )
