from  django.shortcuts import render,redirect
from app.models import Staff,Staff_leave,Student,Course,Subject

def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()

    context = {
        'subject_count': subject_count,
        'student_count': student_count,
        'staff_count': staff_count,
        'course_count': course_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female
    }
    return render(request,'staff/home.html',context)


def APPLY_LEAVE(request):
    staff=Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id=i.id
        staff_leave_history=Staff_leave.objects.filter(staff_id=staff_id)
        context={
            'staff_leave_history':staff_leave_history
        }
    return render(request,'staff/apply_leave.html', context)


def STAFF_LEAVE_APPLY_SAVE(request):
    if request.method=="POST":
        leave_date=request.POST.get('leave_date')
        leave_message=request.POST.get('leave_message')
        staff=Staff.objects.get(admin=request.user.id)

        leave=Staff_leave(
            staff_id=staff,
            data=leave_date,
            message=leave_message,

        )
        leave.save()
        return redirect('staff_apply_leave')