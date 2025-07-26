from django.urls import path
from . import apis

urlpatterns = [
    path("me/", apis.MeApi.as_view(), name="me"),
    path("students/", apis.ApplicantListView.as_view(), name="applicant-list"),
    path(
        "students/bulk-upload/", apis.FileUploadView.as_view(), name="applicant-upload"
    ),
    path("analytics/kpis/", apis.KPIView.as_view(), name="kpis"),
    path("analytics/charts/", apis.ChartDataView.as_view(), name="charts"),
    path(
        "students/filter-options/",
        apis.FilterOptionsView.as_view(),
        name="filter-options",
    ),
]
