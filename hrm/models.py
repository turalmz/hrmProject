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


def get_hour(self,day):
    if day==1:
        return self.day_1
    elif day==2:
        return self.day_2
    elif day==3:
        return self.day_3
    elif day==4:
        return self.day_4
    elif day==5:
        return self.day_5
    elif day==6:
        return self.day_6   
    elif day==7:
        return self.day_7
    elif day==8:
        return self.day_8
    elif day==9:
        return self.day_9
    elif day==10:
        return self.day_10
    elif day==11:
        return self.day_11
    elif day==12:
        return self.day_12
    elif day==13:
        return self.day_13
    elif day==14:
        return self.day_14
    elif day==15:
        return self.day_15
    elif day==16:
        return self.day_16
    elif day==17:
        return self.day_17
    elif day==18:
        return self.day_18    
    elif day==19:
        return self.day_19
    elif day==20:
        return self.day_20
    elif day==21:
        return self.day_21
    elif day==22:
        return self.day_22
    elif day==23:
        return self.day_23
    elif day==24:
        return self.day_24 
    elif day==25:
        return self.day_25
    elif day==26:
        return self.day_26  
    elif day==27:
        return self.day_27
    elif day==28:
        return self.day_28
    elif day==29:
        return self.day_29
    elif day==30:
        return self.day_30
    elif day==31:
        return self.day_31
    else:
        return 0
    
    

class Job(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=40)

    class Meta:
        verbose_name = _('İş')
        verbose_name_plural = _('İşlər')
        db_table = 'jobs'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(_('name'), primary_key=True, max_length=40)

    class Meta:
        verbose_name = _('Departament')
        verbose_name_plural = _('Departamentlər')
        db_table = 'departments'

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Ad',primary_key=True)
    hire_date = models.DateField(_('hire date'))
    birth_date = models.DateField(_('birthday'))
    quit_date = models.DateField(_('quit date'),blank=True, null=True)
    salary = models.IntegerField(_('salary'),default=0)

    fin = models.CharField(max_length=7,default="", blank=True, verbose_name ='Fin')
    passport = models.CharField(max_length=12,default="", blank=True, verbose_name ='Passport nömrəsi')
    bank_account = models.CharField(max_length=16,default="not", blank=True, verbose_name ='Bank nömrəsi')
    phone = models.CharField(max_length=20,default="", blank=True, verbose_name ='Əl telefonu')
    home_phone = models.CharField(max_length=20,default="", blank=True, verbose_name ='Ev telefonu')
    address = models.CharField(max_length=200,default="", blank=True, verbose_name ='Ünvan')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name ='Şöbə',blank=True,null=True)
    # manager = models.ForeignKey('self', null=True, related_name='employee',on_delete=models.CASCADE, blank=True, verbose_name ='Meneceri')
    job = models.ForeignKey(Job, on_delete=models.CASCADE,blank=True, null=True,verbose_name ='İşi',)
    bank_account_len = models.PositiveIntegerField(default=0, verbose_name='Bank nömrəsi')
    social_insurance = models.CharField(max_length=20,default="", blank=True, verbose_name='SSN')
    social_insurance_len = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True, verbose_name='hazırda bu müəssədə işləyirmi')
    give_bank_account = models.BooleanField(default=False, verbose_name='bank akkauntu verilibmi')
    give_insurance_account = models.BooleanField(default=False, verbose_name='sığorta akkauntu verilibmi')
    day = models.IntegerField( default=5,validators=[MaxValueValidator(6),MinValueValidator(5)],choices=MONTH_CHOICES, verbose_name = 'İş rejimi')

    rest_days = models.IntegerField(
        default=21,
        validators=[
            MaxValueValidator(50),
            MinValueValidator(1)
        ], verbose_name = 'Məzuniyyət günü sayı'
     )

    def __str__(self):
        return "{}".format(self.first_name)

    def __repr__(self):
        return self.__str__()


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
        return num_days+1

    def get_weekends(self):
        import datetime
        get_day = datetime.date(self.year, self.month, 1).weekday()

        return get_day


    def get_weekday(self):


        return self.weekday


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

    rest = models.FloatField(null=True, blank=True, default=0 ,verbose_name='Məzuniyyətə görə hesablanan məbləğ')

    salary = models.FloatField(null=True, blank=True, default=None,verbose_name='İşçinin maaşı')

    all_amount = models.FloatField(null=True, blank=True, default=None,verbose_name='Bu ay işçinin maaşı(məzuniyyət daxil)')

    hours = models.FloatField(null=True, blank=True, default=None,verbose_name='Bu ay işçinin işlədiyi saat')


    ss = models.FloatField(null=True, blank=True, default=None,verbose_name='SS')

    un = models.FloatField(null=True, blank=True, default=None,verbose_name='işsizlik fon')

    gv = models.FloatField(null=True, blank=True, default=None,verbose_name='g/v')

    minus = models.FloatField(null=True, blank=True, default=None,verbose_name='tutum cəmi')

    total = models.FloatField(null=True, blank=True, default=None,verbose_name='total')

    def get_weekday(self):
        return self.month.weekday

    def __str__(self):
        return "{} -> {}".format(self.month, self.emp)

    def get_day_hours(self):
        sum_day_hours=0.0
        for day in range(1, 31):
            if get_hour(self,day):
                sum_day_hours = sum_day_hours+self.get_day_hour(day)

        return sum_day_hours


    def is_sunday(self,day):
        try:
            if (7==datetime.date(self.month.year, self.month.month, day).isoweekday()):
                return True
        except:
            return False
        return False


    def is_saturday(self,day):
        try:
            if (6==datetime.date(self.month.year, self.month.month, day).isoweekday()):
                return True
        except:
            False

        return False

    def is_weekday(self,day):
        try:
            if (6>datetime.date(self.month.year, self.month.month, day).isoweekday()):
                return True
        except:
            return False
        return False
    
    def get_day_hour(self,day):
        if self.is_saturday(day):
            if self.emp.day==6:
                return 5
            else:
                return 8
        elif self.is_weekday(day):
            if self.emp.day==6:
                return 7
            else:
                return 8
        elif self.is_sunday(day):
            if self.emp.day==6:
                return 7
            else:
                return 8
        else:
            return 0
    
    def get_holidays(self):
        hol = Holiday.objects.first(mon=self.month)
        hours = hol.get_holidays(hol,self.emp)
        return hours

    def get_hol_hours(self, hol):
        sum_day_hours = 0.0
        for day in range(1, 31):
            sum_day_hours = sum_day_hours + self.get_day_hour(day)

        return sum_day_hours

    def save(self, *args, **kwargs):
        self.salary = (self.get_day_hours())*float(self.emp.salary/self.month.hours)
        self.hours = (self.get_day_hours())
        self.all_amount = float(self.salary)+float(self.rest)
        self.ss = self.all_amount-200*3/100+(self.all_amount-200)*10
        self.total = self.all_amount+self.ss
        return super(MonthEmployee, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Əmək haqqı')
        verbose_name_plural = _('Əmək haqqı')


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

    def alldays(self):

        alma = self.day_1+self.day_2+self.day_3+self.day_4+self.day_5+self.day_6+\
               self.day_7+self.day_8+self.day_9+self.day_10+self.day_11+self.day_12+\
               self.day_13+self.day_14+self.day_15+self.day_16+ self.day_17+self.day_18+\
               self.day_19+self.day_20+self.day_21+self.day_22+self.day_23+self.day_24+\
               self.day_25+self.day_26+self.day_27+self.day_28+self.day_29+self.day_30+self.day_31
        return alma

    def get_day_hours(self):
        sum_day_hours = 0.0
        for day in range(1, 31):
            sum_day_hours = sum_day_hours + self.get_day_hour(day)

        return sum_day_hours

    def is_sunday(self, day):
        try:
            if (7 == datetime.date(self.month.year, self.month.month, day).isoweekday()):
                return True
        except:
            return False
        return False

    def is_saturday(self, day):
        try:
            if (6 == datetime.date(self.month.year, self.month.month, day).isoweekday()):
                return True
        except:
            False

        return False

    def is_weekday(self, day):
        try:
            if (6 > datetime.date(self.month.year, self.month.month, day).isoweekday()):
                return True
        except:
            return False
        return False

    def get_day_hour(self, emp,day):
        if self.is_saturday(self, day):
            if emp.day == 6:
                return 5
            else:
                return 8
        elif self.is_weekday(self, day):
            if emp.day == 6:
                return 7
            else:
                return 8
        elif self.is_sunday(self, day):
            if emp.day == 6:
                return 7
            else:
                return 8
        else:
            return 0

    def get_holidays(self,emp):
        hours = self.get_hol_hours(self,emp)

        return hours

    def get_hol_hours(self,emp):
        sum_day_hours = 0.0
        for day in range(1, 31):
            sum_day_hours = sum_day_hours + self.get_day_hour(emp,day)

        return sum_day_hours




class Common(models.Model):
    mon = models.OneToOneField(MonthEmployee,to_field='id', on_delete=models.CASCADE,blank=True,default=0)

    first_name = models.CharField(null=True, blank=True,max_length=100, verbose_name ='Ad')

    rest = models.FloatField(null=True, blank=True, default=0 ,verbose_name='Məzuniyyətə görə hesablanan məbləğ')

    salary = models.FloatField(null=True, blank=True, default=None,verbose_name='İşçinin maaşı')

    all_amount = models.FloatField(null=True, blank=True, default=None,verbose_name='Bu ay işçinin maaşı(məzuniyyət daxil)')

    hours = models.FloatField(null=True, blank=True, default=None,verbose_name='Bu ay işçinin işlədiyi saat')

    ss = models.FloatField(null=True, blank=True, default=None,verbose_name='SS')

    un = models.FloatField(null=True, blank=True, default=None,verbose_name='işsizlik fon')

    gv = models.FloatField(null=True, blank=True, default=None,verbose_name='g/v')

    minus = models.FloatField(null=True, blank=True, default=None,verbose_name='tutum cəmi')

    total = models.FloatField(null=True, blank=True, default=None,verbose_name='total')

    class Meta:
        verbose_name = _('Əmək haqqı hesabat')
        verbose_name_plural = _('Əmək haqqı cəmi hesabat')