from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import *
from django import forms
from django.shortcuts import redirect
from django.shortcuts import render


admin.site.site_header = "ERP Admin"
admin.site.site_title = "ERP Admin Portal"
admin.site.index_title = "Welcome to ERP Researcher Portal"


class CsvOrExcelImportForm(forms.Form):
    csv_file = forms.FileField()


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()


class ExportCsvMixin():
    def export_as_csv(self, request, queryset):
        # help(self)
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class IsCardFilter(admin.SimpleListFilter):
    title = 'has card'
    parameter_name = 'is_card'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(bank_account_len=16)
        elif value == 'No':
            return queryset.exclude(bank_account_len=16)
        return queryset


class IsInsuranceFilter(admin.SimpleListFilter):
    title = 'has insurance'
    parameter_name = 'is_insurance'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(social_insurance_len=20)
        elif value == 'No':
            return queryset.exclude(social_insurance_len=20)
        return queryset

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ("first_name","last_name", "job","department")
    readonly_fields=('bank_account_len', 'social_insurance_len',)
    actions = ["export_as_csv"]
    list_per_page = 100

    list_filter = ("department","job",IsInsuranceFilter,IsCardFilter)

    def is_card(self, obj):
        return obj.bank_account_len == 16

    is_card.boolean = True

    def is_insurance(self, obj):
        return obj.social_insurance == 20

    is_insurance.boolean = True


def has_add_permission(self, request):
    return False



admin.site.register(Department)
# admin.site.register(Rest)
admin.site.register(Job)


@admin.register(BankCardEmployee)
class BankCardEmployeeAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ("first_name","last_name", "job","department")
    actions = ["export_as_csv"]
    list_per_page = 100

    list_filter = ("department","job",IsInsuranceFilter,IsCardFilter)

    def is_card(self, obj):
        return obj.bank_account_len == 16

    is_card.boolean = True

    def is_insurance(self, obj):
        return obj.social_insurance == 20

    is_insurance.boolean = True


@admin.register(InsuranceEmployee)
class InsuranceEmployeeAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ("first_name","last_name", "job","department")
    actions = ["export_as_csv"]
    list_per_page = 100

    list_filter = ("department","job",IsInsuranceFilter,IsCardFilter)

    def is_card(self, obj):
        return obj.bank_account_len == 16

    is_card.boolean = True

    def is_insurance(self, obj):
        return obj.social_insurance == 20

    is_insurance.boolean = True


@admin.register(Rest)
class RestAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ("month", "emp","day","sum")
    readonly_fields = ('sum','year', )


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ("month", "year","last_day","weekday")
    actions = ["export_as_csv"]
    list_per_page = 100
    readonly_fields = ('last_day','weekday')


@admin.register(MonthEmployee)
class MonthEmployeeAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ("month","get_weekday","job","emp","day_1","day_2","day_3","day_4","day_5","day_6","day_7","day_8","day_9",
                    "day_10","day_11","day_12","day_13","day_14","day_15","day_16","day_17","day_18","day_19",
                    "day_20","day_21","day_22","day_23","day_24","day_25","day_26","day_27","day_28","day_29",
                    "day_30", "day_31",)

    list_editable = ("day_1","day_2","day_3","day_4","day_5","day_6","day_7","day_8","day_9",
                    "day_10","day_11","day_12","day_13","day_14","day_15","day_16","day_17","day_18","day_19",
                    "day_20","day_21","day_22","day_23","day_24","day_25","day_26","day_27","day_28","day_29",
                    "day_30", "day_31",)

    change_list_template = "hrm/employee_changelist.html"

    list_filter = ("month","emp__job")
    actions = ["export_as_csv"]

    readonly_fields=('hours','salary' )

    list_per_page = 100

    def job(self, obj):
        return obj.emp.job


    class Media:
        js = ('js/script.js',)
        css = {
             'all': ('css/script.css',)
        }

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path

        my_urls = [
            path('import-csv/', self.import_csv),
            path('import-excel/', self.import_excel),

        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)


            self.message_user(request, "Your csv file has been imported")


            return redirect("..")
        form = CsvOrExcelImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

    def import_excel(self, request):
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            reader = csv.reader(excel_file)

            import openpyxl
            # you may put validations here to check extension or file size

            wb = openpyxl.load_workbook(excel_file)

            # getting a particular sheet by name out of many sheets
            worksheet = wb["Sheet1"]
            print(worksheet)

            excel_data = list()
            # iterating over the rows and
            # getting value from each cell in row
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))

                print(row_data)

                excel_data.append(row_data)

            emp_list_body={}


            emp_list_head=list()
            # emp_list_body=list()

            row_count = 0
            for row in excel_data:
                i = 0

                if row_count == 0:
                    for cell in row:
                        emp_list_head.append(cell)
                        i+=1
                else:
                    emp={}
                    for cell in row:
                        emp[emp_list_head[i]]=cell
                        i += 1
                    emp_list_body[row_count]=emp
                row_count+=1
            print("emp_list_head")
            print(emp_list_head)

            print("emp_list_body")
            print(emp_list_body)

            self.message_user(request, "Your csv file has been imported")


            return redirect("..")


        form = ExcelImportForm()
        payload = {"form": form}
        return render(
            request, "admin/excel_form.html", payload
        )



from django.dispatch import receiver
from django.db.models.signals import post_save


    
@receiver(post_save, sender=Employee)
def save_emp1(sender, instance, **kwargs):
    if instance.give_bank_account  == True:
        if BankCardEmployee.objects.filter(emp=instance).exists():
            pass
        else:
            b = BankCardEmployee(emp=instance)
            b.save()
            print('__added')
 

@receiver(post_save, sender=Employee)
def save_emp2(sender, instance, **kwargs):
    if instance.insurance == True:
        if InsuranceEmployee.objects.filter(emp=instance).exists():
            pass
        else:
            b = InsuranceEmployee(emp=instance)
            b.save()
            print('_added')
        
    print('_-----')


@receiver(post_save, sender=InsuranceEmployee)
def save_inemp(sender, instance, **kwargs):
    if Employee.objects.filter(pk=instance.emp.pk).exists():
        b = Employee.objects.first(pk=instance.emp.pk)
        b.give_insurance_account = instance.give_insurance_account
        b.save()
        print('_added')

    print('_-----')


@receiver(post_save, sender=BankCardEmployee)
def save_baemp(sender, instance, **kwargs):
    if Employee.objects.filter(pk=instance.emp.pk).exists():
        b = Employee.objects.first(pk=instance.emp.pk)
        b.give_bank_account = instance.give_bank_account
        b.save()
        print('_added')

    print('_-----')