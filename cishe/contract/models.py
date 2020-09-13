from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


UserModel = get_user_model()

# leave it class to front end
# class ContractSource(Enum):
#     KF = 'kf'
#     SAF = 'saf'
#     SITE_VISIT = 'site_visit'


class Contract(models.Model):
    contract_num = models.CharField(max_length=16)
    contract_type = models.CharField(max_length=8)
    source = models.CharField(max_length=8, blank=True)
    signing_date = models.DateField()
    signing_branch = models.CharField(max_length=4)
    sale_agent = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    free_date_until = models.DateField()
    total_amount = models.PositiveIntegerField()
    total_amount_remark = models.CharField(max_length=256, blank=True)
    referrer = models.CharField(max_length=32, blank=True)
    supplementary_agreement = models.TextField(blank=True)


class Customer(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=8)
    phone_num = PhoneNumberField()
    phone_num2 = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    parent_phone_num = PhoneNumberField(blank=True)
    parent_type = models.CharField(max_length=4, blank=True)
    university = models.CharField(max_length=32)
    department = models.CharField(max_length=32, blank=True)
    major = models.CharField(max_length=32, blank=True)


class ServiceInfo(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, unique=True)
    enrollment_semester = models.CharField(max_length=4)
    retention_statement = models.CharField(max_length=32)
    target_country_code = models.CharField(max_length=32)  # concat with comma s
    target_subject = models.CharField(max_length=4)
    target_degree = models.CharField(max_length=4)
    target_major = models.CharField(max_length=32)
    team = models.CharField(max_length=4)
    workload = models.FloatField()
    status = models.CharField(max_length=32)
    start_date = models.DateField()
    remark = models.TextField()  # including workload remark


class TakeOver(models.Model):
    staff = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    transfer_date = models.DateField()
    remark = models.TextField()

    class Meta:
        unique_together = (
            (
                "staff",
                "contract",
            ),
        )
