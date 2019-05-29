from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import *
from django import forms
from django.shortcuts import redirect
from django.shortcuts import render

from django.conf.urls import include, url


admin.site.site_header = "ERP Admin"
admin.site.site_title = "ERP Admin Portal"
admin.site.index_title = "Welcome to ERP Researcher Portal"


class CsvOrExcelImportForm(forms.Form):
    csv_file = forms.FileField()


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()


class ExportCsvMixin():
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        response.write(u'\ufeff'.encode('utf8'))
        # writer = csv.writer(response, delimiter=';', dialect='excel')

        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([(getattr(obj, field)) for field in field_names])

        return response

    export_as_csv.short_description = "Export to Csv Selected"



    def export_users_csv(self,request,queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Report.csv"'

        # response = HttpResponse(content_type='application/vnd.ms-excel')
        # response['Content-Disposition'] = 'attachment; filename=Report.xlsx'

        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response)

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        writer.writerow(field_names)

        for obj in queryset:
            row = writer.writerow([(getattr(obj, field)) for field in field_names])

        return response

    export_users_csv.short_description = "Export to Excel Selected"


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ("first_name", "job","department","give_bank_account","give_insurance_account")
    readonly_fields=('bank_account_len', 'social_insurance_len',)
    actions = ["export_as_csv","export_users_csv"]
    list_per_page = 100

    list_filter = ("department","job","give_bank_account","give_insurance_account")


    change_list_template = "hrm/employee_changelist.html"

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
            print(wb.iso_dates)
            print(wb.excel_base_date)
            # getting a particular sheet by name out of many sheets
            worksheet = wb["Sheet1"]
            print(worksheet)


            excel_data = list()
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))

                print(row_data)

                excel_data.append(row_data)

            emp_list_body={}


            emp_list_head=list()

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
                    emp_list_body[str(row_count)]=emp
                row_count+=1
            print("emp_list_head")
            print(emp_list_head)

            print("emp_list_body")
            print(emp_list_body)
            from .models import Job
            row_count = 0

            print(type(emp_list_body))

            for key,value in emp_list_body.items():

                print(key)

                print(type(value))
                row = value
                job_id = Job.objects.get(name=value['job'])
                print(job_id)
                import datetime


                emp = Employee( first_name=row['fullname'],
                    hire_date=datetime.datetime.strptime(row['hire_date'], "%Y-%m-%d %H:%M:%S"),
                    birth_date=datetime.datetime.strptime(row['birth_date'], "%Y-%m-%d %H:%M:%S"),
                )

                try:
                    emp.phone =row['phone']
                except:
                    pass

                try:
                    emp.home_phone = row['home_phone']
                except:
                    pass

                try:
                    emp.fin = row['fin']
                except:
                    pass

                try:
                    emp.passport = row['passport']
                except:
                    pass

                try:
                    emp.address = row['address']
                except:
                    pass

                try:
                    if row['active']==1:
                        emp.active = True
                    elif row['active'] == 'OK':
                        emp.active = True
                    elif row['active']=='1':
                        emp.active = True
                    elif row['active']=='ok':
                        emp.active = True
                    elif row['active'] == 'active':
                        emp.active = True
                    elif row['active']=='aktiv':
                        emp.active = True
                    elif row['active']=='Aktiv':
                        emp.active = True
                    else:
                        emp.active = False
                except:
                    pass


                try:
                    emp.job = Job.objects.filter(name=value['job'])[:1].get()
                except:
                    pass

                try:
                    emp.department=Department.objects.filter(name=value['department'])[:1].get()
                except:
                    pass
                try:
                    emp.quit_date = datetime.datetime.strptime(row['quit_date'], "%Y-%m-%d %H:%M:%S")
                except:
                    pass

                emp.save()

                row_count += 1
            self.message_user(request, "Your csv file has been imported")


            return redirect("..")


        form = ExcelImportForm()
        payload = {"form": form}
        return render(
            request, "admin/excel_form.html", payload
        )



def has_add_permission(self, request):
    return False



admin.site.register(Department)
# admin.site.register(Rest)
admin.site.register(Job)



@admin.register(Rest)
class RestAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ("month", "emp","day","sum")
    readonly_fields = ('sum','year', )

admin.site.register(Common)

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


from django.dispatch import receiver
from django.db.models.signals import post_save

    
@receiver(post_save, sender=MonthEmployee)
def save_baemp(sender, instance, **kwargs):
    if Common.objects.filter(mon=instance).exists():
        b = Common.objects.filter(mon=instance)[:1].get()
        b.mon = instance
        b.first_name = instance.emp.first_name
        b.rest = instance.rest
        b.salary = instance.salary
        b.all_amount = instance.all_amount
        b.hours = instance.hours
        b.ss = instance.ss
        b.un = instance.un
        b.gv = instance.gv
        b.minus = instance.minus
        b.total = instance.total
        b.save()
        print('added')
    else:

        b = Common(mon = instance,first_name = instance.emp.first_name)

        b.mon = instance
        b.first_name = instance.emp.first_name
        b.rest = instance.rest
        b.salary = instance.salary
        b.all_amount = instance.all_amount
        b.hours = instance.hours
        b.ss = instance.ss
        b.un = instance.un
        b.gv = instance.gv
        b.minus = instance.minus
        b.total = instance.total
        b.save()

    print('_-----')
