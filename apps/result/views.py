from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from apps.students.models import Student
from apps.result.models import AcademicSession,AcademicTerm,Student,StudentClass   

from .forms import CreateResults, EditResults
from .models import Result


@login_required
def create_result(request):
    students = Student.objects.all()
    if request.method == "POST":

        # After visiting the second page
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
                subjects = form.cleaned_data["subjects"]
                session = form.cleaned_data["session"]
                term = form.cleaned_data["term"]
                student_ids = request.POST["students"]
                results = []
                for student_id in student_ids.split(","):
                    stu = Student.objects.get(pk=student_id)
                    if stu.current_class:
                        for subject in subjects:
                            check = Result.objects.filter(
                                session=session,
                                term=term,
                                current_class=stu.current_class,
                                subject=subject,
                                student=stu,
                            ).first()
                            if not check:
                                results.append(
                                    Result(
                                        session=session,
                                        term=term,
                                        current_class=stu.current_class,
                                        subject=subject,
                                        student=stu,
                                    )
                                )

                Result.objects.bulk_create(results)

                # Calculate aggregates and division for each student
                for student_id in student_ids.split(","):
                    stu = Student.objects.get(pk=student_id)
                    total_aggregates = Result.calculate_total_aggregates(stu, session, term, stu.current_class)
                    division = Result.calculate_division(stu, session, term, stu.current_class)
                    # Store total_aggregates and division in session or pass to next page
                    request.session[f'student_{stu.id}_total_aggregates'] = total_aggregates
                    request.session[f'student_{stu.id}_division'] = division

                return redirect("edit_results")

        # After choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResults(
                initial={
                    "session": request.current_session,
                    "term": request.current_term,
                }
            )
            studentlist = ",".join(id_list)
            return render(
                request,
                "result/create_result_page2.html",
                {"students": studentlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didn't select any student.")
    return render(request, "result/create_result.html", {"students": students})

@login_required
def result_summary(request):
    student_id = request.GET.get('student_id')
    session_id = request.GET.get('session_id')
    term_id = request.GET.get('term_id')
    class_id = request.GET.get('class_id')

    student = Student.objects.get(id=student_id)
    session = AcademicSession.objects.get(id=session_id)
    term = AcademicTerm.objects.get(id=term_id)
    current_class = StudentClass.objects.get(id=class_id)

    results = Result.objects.filter(student=student, session=session, term=term, current_class=current_class)
    
    total_aggregates = request.session.get(f'student_{student.id}_total_aggregates')
    division = request.session.get(f'student_{student.id}_division')

    context = {
        'results': results,
        'total_aggregates': total_aggregates,
        'division': division,
    }

    return render(request, 'result/result_summary.html', context)













@login_required
def edit_results(request):
    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
    else:
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        form = EditResults(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})


class ResultListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        bulk = {}

        for result in results:
            test_total = 0
            exam_total = 0
            subjects = []
            for subject in results:
                if subject.student == result.student:
                    subjects.append(subject)
                    test_total += subject.test_score
                    exam_total += subject.exam_score

            bulk[result.student.id] = {
                "student": result.student,
                "subjects": subjects,
                "test_total": test_total,
                "exam_total": exam_total,
                "total_total": test_total + exam_total,
            }

        context = {"results": bulk}
        return render(request, "result/all_results.html", context)
