from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from apps.students.models import Student

from .utils import score_grade


# Create your models here.
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_score = models.IntegerField(default=0)
    exam_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student} {self.session} {self.term} {self.subject}"

    @property
    def calculate_total_aggregates(self):
        
        results = Result.objects.filter(student=self.student, session=self.session, term=self.term, current_class=self.current_class)
        total_aggregates = sum(result.aggregate() for result in results)
        return total_aggregates
    
    def total_score(self):
        weighted_test_score = self.test_score * 0.3
        weighted_exam_score = self.exam_score * 0.7
        return round(weighted_test_score + weighted_exam_score)

    def grade(self):
        return score_grade(self.total_score())

    def aggregate(self):
        total_score = self.total_score()
        if 0 <= total_score <= 34:
            return 9
        elif 35 <= total_score <= 44:
            return 8
        elif 45 <= total_score <= 54:
            return 7
        elif 55 <= total_score <= 59:
            return 6
        elif 60 <= total_score <= 64:
            return 5
        elif 65 <= total_score <= 69:
            return 4
        elif 70 <= total_score <= 74:
            return 3
        elif 75 <= total_score <= 79:
            return 2
        elif 80 <= total_score <= 100:
            return 1
    
    
    @property
    def calculate_division(self):
        total_aggregates = self.calculate_total_aggregates
        if 4 <= total_aggregates <= 12:
            return "Division 1"
        elif 13 <= total_aggregates <= 23:
            return "Division 2"
        elif 24 <= total_aggregates <= 29:
            return "Division 3"
        elif 30 <= total_aggregates <= 34:
            return "Division 4"
        else:
            return "Ungraded (U)"
