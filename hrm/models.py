from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
import calendar

MONTH_CHOICES = (
    (5, "5"),
    (6, "6"),
)

class Job(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=40)

    class Meta:
        verbose_name = _('İş')
        verbose_name_plural = _('İşlər')
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
    first_name = models.CharField(max_length=100, verbose_name ='Ad')
    mid_name = models.CharField(max_length=100,default="",blank=True, verbose_name ='Ata adı')
    last_name = models.CharField(max_length=100, verbose_name ='Soyad')
    hire_date = models.DateField(_('hire date'))
    birth_date = models.DateField(_('birthday'))
    quit_date = models.DateField(_('quit date'),blank=True, null=True)
    salary = models.IntegerField(_('salary'),default=0)
    fin = models.CharField(max_length=12,default="", blank=True, verbose_name ='Fin')
    passport = models.CharField(max_length=12,default="", blank=True, verbose_name ='Passport nömrəsi')
    bank_account = models.CharField(max_length=16,default="not", blank=True, verbose_name ='Bank nömrəsi')
    phone = models.CharField(max_length=20,default="", blank=True, verbose_name ='Əl telefonu')
    home_phone = models.CharField(max_length=20,default="", blank=True, verbose_name ='Ev telefonu')
    address = models.CharField(max_length=20,default="", blank=True, verbose_name ='Ünvan')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no', verbose_name=_('department'),blank=True,default=0)
    manager = models.ForeignKey('self', null=True, related_name='employee',on_delete=models.CASCADE, blank=True, verbose_name ='Meneceri')
    job = models.ForeignKey(Job, on_delete=models.CASCADE,blank=True,default=0, verbose_name ='İşi')
    bank_account_len = models.PositiveIntegerField(default=0, verbose_name ='Bank nömrəsi')
    social_insurance = models.CharField(max_length=20,default="", blank=True, verbose_name ='Sığorta nömrısi')
    social_insurance_len = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True, verbose_name ='hazırda bu müəssədə işləyirmi')
    give_bank_account = models.BooleanField(default=False, verbose_name = 'bank akkauntu verilibmi')
    give_insurance_account = models.BooleanField(default=False, verbose_name = 'sığorta akkauntu verilibmi')
    day = models.IntegerField( default=5,validators=[MaxValueValidator(6),MinValueValidator(5)],choices=MONTH_CHOICES, verbose_name = 'İş rejimi')

    rest_days = models.IntegerField(
        default=21,
        validators=[
            MaxValueValidator(50),
            MinValueValidator(1)
        ], verbose_name = 'Məzuniyyət günü sayı'
     )

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __repr__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
         self.bank_account_len = len(self.bank_account)
         self.social_insurance_len = len(self.social_insurance)

         return super(Employee, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('İşçi')
        verbose_name_plural = _('İşçilər')


class Month(models.Model):
    month = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ], verbose_name = 'Ay'
     )
    year = models.IntegerField(
        default=2019,
        validators=[
            MaxValueValidator(2050),
            MinValueValidator(2010)
        ], verbose_name = 'İl'
    )
    last_day = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(31),
            MinValueValidator(28)
        ], verbose_name = 'Ayın son günü'
     )

    hours = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(210),
            MinValueValidator(10)
        ], verbose_name = 'Aylıq iş norması'
     )

    weekday = models.PositiveIntegerField(default=0, verbose_name = 'Ayın ilk günü həftənin hansı günüdür')

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

    def post_save(self):
        for e in Employee.objects.filter(active=True):
            MonthEmployee(month=self)


    class Meta:
        verbose_name = _('Ay')
        verbose_name_plural = _('Aylar')


class MonthEmployee(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE,blank=True,default=0, verbose_name = 'Ay')
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE,blank=True,default=0 ,verbose_name = 'İşçi')
    day_1 = models.BooleanField(default=False)
    day_2 = models.BooleanField(default=False)
    day_3 = models.BooleanField(default=False)
    day_4 = models.BooleanField(default=False)
    day_5 = models.BooleanField(default=False)
    day_6 = models.BooleanField(default=False)
    day_7 = models.BooleanField(default=False)
    day_8 = models.BooleanField(default=False)
    day_9 = models.BooleanField(default=False)
    day_10 = models.BooleanField(default=False)
    day_11 = models.BooleanField(default=False)
    day_12 = models.BooleanField(default=False)
    day_13 = models.BooleanField(default=False)
    day_14 = models.BooleanField(default=False)
    day_15 = models.BooleanField(default=False)
    day_16 = models.BooleanField(default=False)
    day_17 = models.BooleanField(default=False)
    day_18 = models.BooleanField(default=False)
    day_19 = models.BooleanField(default=False)
    day_20 = models.BooleanField(default=False)
    day_21 = models.BooleanField(default=False)
    day_22 = models.BooleanField(default=False)
    day_23 = models.BooleanField(default=False)
    day_24 = models.BooleanField(default=False)
    day_25 = models.BooleanField(default=False)
    day_26 = models.BooleanField(default=False)
    day_27 = models.BooleanField(default=False)
    day_28 = models.BooleanField(default=False)
    day_29 = models.BooleanField(default=False)
    day_30 = models.BooleanField(default=False)
    day_31 = models.BooleanField(default=False)

    rest = models.FloatField(null=True, blank=True, default=0 ,verbose_name = 'Bu ay ərzində alınan məzuniyyət')

    salary = models.FloatField(null=True, blank=True, default=None,verbose_name = 'Bu ay işçinin maaşı')

    all_amount = models.FloatField(null=True, blank=True, default=None,verbose_name = 'Bu ay işçinin maaşı(məzuniyyət daxil)')

    hours = models.FloatField(null=True, blank=True, default=None,verbose_name = 'Bu ay işçinin işlədiyi saat')


    def __str__(self):
        return "{} -> {}".format(self.month, self.emp)

    def alldays(self):

        alma = self.day_1+self.day_2+self.day_3+self.day_4+self.day_5+self.day_6+\
               self.day_7+self.day_8+self.day_9+self.day_10+self.day_11+self.day_12+\
               self.day_13+self.day_14+self.day_15+self.day_16+ self.day_17+self.day_18+\
               self.day_19+self.day_20+self.day_21+self.day_22+self.day_23+self.day_24+\
               self.day_25+self.day_26+self.day_27+self.day_28+self.day_29+self.day_30+self.day_31
        return alma
    
    def is_sunday(self,day):
        if 7==datetime.date(self.month.year, self.month.mon, day).isoweekday()):
            return True
        return False
    
    def is_saturday(self,day):
        if 6==datetime.date(self.month.year, self.month.mon, day).isoweekday()):
            return True
        return False
    
      def is_weekday(self,day):
        if 6>datetime.date(self.month.year, self.month.mon, day).isoweekday()):
            return True
        return False  
    
    def save(self, *args, **kwargs):
         self.salary = (self.alldays())*float(self.emp.salary/self.month.hours)
         if self.emp.day==5:
            self.hours = (self.alldays())*8
         elif self.emp.day==6:
            self.hours = (self.alldays())*7
            
         self.all_amount = float(self.salary)+float(self.rest)
         return super(MonthEmployee, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Aylıq')
        verbose_name_plural = _('Aylıqlar')


class Rest(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE, verbose_name=_('month'),blank=True,default=0)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('employee'),blank=True,default=0)
    day = models.IntegerField( default=0,validators=[MaxValueValidator(55),MinValueValidator(1)])
    sum = models.IntegerField( default=0,validators=[MaxValueValidator(55),MinValueValidator(1)])
    year = models.IntegerField( default=0,validators=[MaxValueValidator(2055),MinValueValidator(2001)])
    extra_money = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('Məzuniyyət')
        verbose_name_plural = _('Məzuniyyət')


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


class Holiday(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE, verbose_name=_('month'),blank=True,default=0)
    day_1 = models.BooleanField(default=False)
    day_2 = models.BooleanField(default=False)
    day_3 = models.BooleanField(default=False)
    day_4 = models.BooleanField(default=False)
    day_5 = models.BooleanField(default=False)
    day_6 = models.BooleanField(default=False)
    day_7 = models.BooleanField(default=False)
    day_8 = models.BooleanField(default=False)
    day_9 = models.BooleanField(default=False)
    day_10 = models.BooleanField(default=False)
    day_11 = models.BooleanField(default=False)
    day_12 = models.BooleanField(default=False)
    day_13 = models.BooleanField(default=False)
    day_14 = models.BooleanField(default=False)
    day_15 = models.BooleanField(default=False)
    day_16 = models.BooleanField(default=False)
    day_17 = models.BooleanField(default=False)
    day_18 = models.BooleanField(default=False)
    day_19 = models.BooleanField(default=False)
    day_20 = models.BooleanField(default=False)
    day_21 = models.BooleanField(default=False)
    day_22 = models.BooleanField(default=False)
    day_23 = models.BooleanField(default=False)
    day_24 = models.BooleanField(default=False)
    day_25 = models.BooleanField(default=False)
    day_26 = models.BooleanField(default=False)
    day_27 = models.BooleanField(default=False)
    day_28 = models.BooleanField(default=False)
    day_29 = models.BooleanField(default=False)
    day_30 = models.BooleanField(default=False)
    day_31 = models.BooleanField(default=False)


class InsuranceEmployee(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('employee'),blank=True,default=0)
    first_name = models.CharField(max_length=100, verbose_name ='Ad')
    mid_name = models.CharField(max_length=100,default="",blank=True, verbose_name ='Ata adı')
    last_name = models.CharField(max_length=100, verbose_name ='Soyad')
    hire_date = models.DateField(_('hire date'))
    birth_date = models.DateField(_('birthday'))
    quit_date = models.DateField(_('quit date'),blank=True, null=True)
    salary = models.IntegerField(_('salary'),default=0)
    fin = models.CharField(max_length=12,default="", blank=True, verbose_name ='Fin')
    passport = models.CharField(max_length=12,default="", blank=True, verbose_name ='Passport nömrəsi')
    bank_account = models.CharField(max_length=16,default="not", blank=True, verbose_name ='Bank nömrəsi')
    phone = models.CharField(max_length=20,default="", blank=True, verbose_name ='Əl telefonu')
    home_phone = models.CharField(max_length=20,default="", blank=True, verbose_name ='Ev telefonu')
    address = models.CharField(max_length=20,default="", blank=True, verbose_name ='Ünvan')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no', verbose_name=_('department'),blank=True,default=0)
    manager = models.ForeignKey('self', null=True, related_name='employee',on_delete=models.CASCADE, blank=True, verbose_name ='Meneceri')
    job = models.ForeignKey(Job, on_delete=models.CASCADE,blank=True,default=0, verbose_name ='İşi')
    bank_account_len = models.PositiveIntegerField(default=0, verbose_name ='Bank nömrəsi')
    social_insurance = models.CharField(max_length=20,default="", blank=True, verbose_name ='Sığorta nömrısi')
    social_insurance_len = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True, verbose_name ='hazırda bu müəssədə işləyirmi')
    give_bank_account = models.BooleanField(default=False, verbose_name = 'bank akkauntu verilibmi')

    give_insurance_account = models.BooleanField(default=False, verbose_name = 'sığorta akkauntu verilibmi')
    day = models.IntegerField( default=5,validators=[MaxValueValidator(6),MinValueValidator(5)],choices=MONTH_CHOICES, verbose_name = 'İş rejimi')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = _('Sığorta İşçi')
        verbose_name_plural = _('Sığorta İşçilər')
        
    def save(self, *args, **kwargs):
        self.first_name = self.emp.first_name
        self.mid_name = self.emp.mid_name
        self.last_name = self.emp.last_name
        self.hire_date = self.emp.hire_date
        self.birth_date = self.emp.birth_date
        self.quit_date = self.emp.quit_date
        self.salary = self.emp.salary
        self.fin = self.emp.fin
        self.passport = self.emp.passport
        self.bank_account = self.emp.bank_account
        self.phone = self.emp.phone
        self.home_phone = self.emp.home_phone
        self.address = self.emp.address
        self.job = self.emp.job
        self.social_insurance = self.emp.social_insurance
        self.active = self.emp.active
        return super(InsuranceEmployee, self).save(*args, **kwargs)

class BankCardEmployee(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('employee'),blank=True,default=0)
    first_name = models.CharField(max_length=100, verbose_name ='Ad')
    mid_name = models.CharField(max_length=100,default="",blank=True, verbose_name ='Ata adı')
    last_name = models.CharField(max_length=100, verbose_name ='Soyad')
    hire_date = models.DateField(_('hire date'))
    birth_date = models.DateField(_('birthday'))
    quit_date = models.DateField(_('quit date'),blank=True, null=True)
    salary = models.IntegerField(_('salary'),default=0)
    fin = models.CharField(max_length=12,default="", blank=True, verbose_name ='Fin')
    passport = models.CharField(max_length=12,default="", blank=True, verbose_name ='Passport nömrəsi')
    bank_account = models.CharField(max_length=16,default="not", blank=True, verbose_name ='Bank nömrəsi')
    phone = models.CharField(max_length=20,default="", blank=True, verbose_name ='Əl telefonu')
    home_phone = models.CharField(max_length=20,default="", blank=True, verbose_name ='Ev telefonu')
    address = models.CharField(max_length=20,default="", blank=True, verbose_name ='Ünvan')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_no', verbose_name=_('department'),blank=True,default=0)
    manager = models.ForeignKey('self', null=True, related_name='employee',on_delete=models.CASCADE, blank=True, verbose_name ='Meneceri')
    job = models.ForeignKey(Job, on_delete=models.CASCADE,blank=True,default=0, verbose_name ='İşi')
    bank_account_len = models.PositiveIntegerField(default=0, verbose_name ='Bank nömrəsi')
    social_insurance = models.CharField(max_length=20,default="", blank=True, verbose_name ='Sığorta nömrısi')
    social_insurance_len = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True, verbose_name ='hazırda bu müəssədə işləyirmi')
    give_bank_account = models.BooleanField(default=False, verbose_name = 'bank akkauntu verilibmi')

    give_insurance_account = models.BooleanField(default=False, verbose_name = 'sığorta akkauntu verilibmi')
    
    day = models.IntegerField( default=5,validators=[MaxValueValidator(6),MinValueValidator(5)],choices=MONTH_CHOICES, verbose_name = 'İş rejimi')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = _('Bank İşçi')
        verbose_name_plural = _('Bank İşçilər')

        
    def save(self, *args, **kwargs):
        self.first_name = self.emp.first_name
        self.mid_name = self.emp.mid_name
        self.last_name = self.emp.last_name
        self.hire_date = self.emp.hire_date
        self.birth_date = self.emp.birth_date
        self.quit_date = self.emp.quit_date
        self.salary = self.emp.salary
        self.fin = self.emp.fin
        self.passport = self.emp.passport
        self.bank_account = self.emp.bank_account
        self.phone = self.emp.phone
        self.home_phone = self.emp.home_phone
        self.address = self.emp.address
        self.job = self.emp.job
        self.social_insurance = self.emp.social_insurance
        self.active = self.emp.active
        return super(BankCardEmployee, self).save(*args, **kwargs)
