from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
import calendar



class Job(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=40)

    class Meta:
        verbose_name = _('job')
        verbose_name_plural = _('jobs')
        db_table = 'jobs'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=40)

    class Meta:
        verbose_name = _('Departament')
        verbose_name_plural = _('Departamentlər')
        db_table = 'departments'

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    mid_name = models.CharField(max_length=100,default="",blank=True)
    last_name = models.CharField(max_length=100)
    hire_date = models.DateField(_('hire date'))
    birth_date = models.DateField(_('birthday'))
    quit_date = models.DateField(_('quit date'),blank=True, null=True)
    salary = models.IntegerField(_('salary'),default=0)
    fin = models.CharField(max_length=12,default="", blank=True)
    passport = models.CharField(max_length=12,default="", blank=True)
    bank_account = models.CharField(max_length=16,default="not", blank=True)
    phone = models.CharField(max_length=20,default="", blank=True)
    address = models.CharField(max_length=20,default="", blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no', verbose_name=_('department'),blank=True,default=0)
    manager = models.ForeignKey('self', null=True, related_name='employee',on_delete=models.CASCADE, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,  verbose_name=_('job'),blank=True,default=0)
    bank_account_len = models.PositiveIntegerField(default=0)
    social_insurance = models.CharField(max_length=20,default="", blank=True)
    social_insurance_len = models.PositiveIntegerField(default=0)
    quit = models.BooleanField(default=False)
    give_bank_account = models.BooleanField(default=False)
    bank_account_given = models.BooleanField(default=False)
    rest_days = models.IntegerField(
        default=21,
        validators=[
            MaxValueValidator(50),
            MinValueValidator(1)
        ]
     )
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __repr__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
         self.bank_account_len = len(self.bank_account)
         self.social_insurance_len = len(self.social_insurance)

         return super(Employee, self).save(*args, **kwargs)


class Month(models.Model):
    month = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ]
     )
    year = models.IntegerField(
        default=2019,
        validators=[
            MaxValueValidator(2050),
            MinValueValidator(2010)
        ]
    )
    last_day = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(31),
            MinValueValidator(28)
        ]
     )

    hours = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(210),
            MinValueValidator(10)
        ]
     )

    weekday = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} / {} / {}".format(self.month, self.year,self.last_day)

    def last_day_of_month(self,year, mon):
        day, num_days = calendar.monthrange(year, mon)
        return num_days

    def get_weekends(self):
        import datetime
        get_day = datetime.date(self.year, self.month, 1).weekday()

        return get_day

    def save(self, *args, **kwargs):
         self.last_day = self.last_day_of_month(self.year,self.month)
         self.weekday = self.get_weekends()
         return super(Month, self).save(*args, **kwargs)


class MonthEmployee(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE, verbose_name=_('month'),blank=True,default=0)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('employee'),blank=True,default=0)
    day_1 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_2 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_3 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_4 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_5 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_6 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_7 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_8 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_9 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_10 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_11 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_12 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_13 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_14 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_15 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_16 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_17 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_18 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_19 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_20 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_21 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_22 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_23 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_24 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_25 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_26 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_27 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_28 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_29 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_30 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])
    day_31 = models.IntegerField( default=0,validators=[MaxValueValidator(12),MinValueValidator(0)])

    rest = models.FloatField(null=True, blank=True, default=None)

    salary = models.FloatField(null=True, blank=True, default=None)

    all_amount = models.FloatField(null=True, blank=True, default=None)

    hours = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return "{} -> {}".format(self.month, self.emp)

    def alldays(self):

        alma= self.day_1+self.day_2+self.day_3+self.day_4+self.day_5+self.day_6+\
               self.day_7+self.day_8+self.day_9+self.day_10+self.day_11+self.day_12+\
               self.day_13+self.day_14+self.day_15+self.day_16+ self.day_17+self.day_18+\
               self.day_19+self.day_20+self.day_21+self.day_22+self.day_23+self.day_24+\
               self.day_25+self.day_26+self.day_27+self.day_28+self.day_29+self.day_30+self.day_31
        return alma


    def save(self, *args, **kwargs):
         self.salary = float(self.alldays())*float(self.emp.salary/self.month.hours)
         self.hours = float(self.alldays())
         self.all_amount = self.salary+self.rest
         return super(MonthEmployee, self).save(*args, **kwargs)


class Rest(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE, verbose_name=_('month'),blank=True,default=0)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('employee'),blank=True,default=0)
    day = models.IntegerField( default=0,validators=[MaxValueValidator(55),MinValueValidator(1)])
    sum = models.IntegerField( default=0,validators=[MaxValueValidator(55),MinValueValidator(1)])
    year = models.IntegerField( default=0,validators=[MaxValueValidator(2055),MinValueValidator(2001)])
    extra_money = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('məzuniyyət')
        verbose_name_plural = _('məzuniyyət')


    def __str__(self):
        return "{} - {}".format(self.month, self.emp)

    def update_sum(self):
        rest_list = Rest.objects.filter(emp=self.emp).filter(month__year=self.year)

        sum_day = 0
        if Rest.objects.filter(pk=self.pk).exists():
            pass
        else:
            sum_day = self.day

        for relement in rest_list:
            sum_day = sum_day+relement.day
            print(relement.day)
        self.sum = sum_day
        # for relement in rest_list:
        #     sum_day = sum_day+relement.day
        #     print(relement.day)

        return True

    def save(self, *args, **kwargs):
        self.year = self.month.year
        self.update_sum()
        rest_list = Rest.objects.filter(emp=self.emp).filter(month__year=self.year).update()
        return super(Rest, self).save(*args, **kwargs)