from django.urls import path

from .views import ResultListView,create_result,edit_results,result_summary

urlpatterns = [
    path("create/", create_result, name="create-result"),
    path('', result_summary, name='result_summary'),
    path("edit-results/", edit_results, name="edit-results"),
    path("view/all", ResultListView.as_view(), name="view-results"),
]
