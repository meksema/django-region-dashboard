from django.core.files.storage import default_storage
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Applicant, UserProfile
from .serializers import ApplicantSerializer, UserSerializer
from .tasks import process_uploaded_file
from django.db.models import Q

from django.db.models.functions import Trim, Lower


class MeApi(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):

        return self.request.user


def apply_filters(queryset, query_params):

    date_from = query_params.get("date_from")
    if date_from:
        queryset = queryset.filter(application_submitted_at__date__gte=date_from)
    date_to = query_params.get("date_to")
    if date_to:
        queryset = queryset.filter(application_submitted_at__date__lte=date_to)

    status = query_params.get("status")
    if status and status != "":
        queryset = queryset.filter(application_status__iexact=status)
    course = query_params.get("courseName")
    if course and course != "":
        queryset = queryset.filter(nd_title__iexact=course)
    gender = query_params.get("gender")
    if gender and gender != "":
        queryset = queryset.filter(gender__iexact=gender)

    region = query_params.get("region")
    if region and region != "":
        queryset = queryset.filter(region__iexact=region)

    return queryset


class ApplicantListView(generics.ListAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Applicant.objects.all()

        if not user.is_staff:
            try:
                user_region = user.userprofile.region
                queryset = queryset.filter(region=user_region)
            except UserProfile.DoesNotExist:
                queryset = Applicant.objects.none()
        queryset = apply_filters(queryset, self.request.query_params)

        search_query = self.request.query_params.get("search", None)
        if search_query:

            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(application_id__icontains=search_query)
            )

        return queryset.order_by("-application_submitted_at")


class FileUploadView(APIView):
    """
    An API endpoint for bulk-uploading applicant data from a CSV or Excel file.
    This endpoint is restricted to admin users only.
    """

    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {"success": False, "message": "No file was provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_path = default_storage.save(f"temp/{uploaded_file.name}", uploaded_file)
        full_path = default_storage.path(file_path)

        process_uploaded_file.delay(full_path)

        return Response(
            {
                "success": True,
                "message": "Upload received! Data is being processed in the background.",
            },
            status=status.HTTP_202_ACCEPTED,
        )


class ChartDataView(APIView):
    """
    Provides aggregated data for frontend charts, respecting user region.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Applicant.objects.all()

        if not user.is_staff:
            try:
                user_region = user.userprofile.region
                queryset = queryset.filter(region=user_region)
            except UserProfile.DoesNotExist:
                queryset = Applicant.objects.none()
        queryset = apply_filters(queryset, self.request.query_params)
        gender_data = (
            queryset.annotate(clean_gender=Trim(Lower("gender")))
            .values("clean_gender")
            .annotate(count=Count("id"))
        )

        status_data = (
            queryset.annotate(clean_status=Trim(Lower("application_status")))
            .values("clean_status")
            .annotate(count=Count("id"))
        )

        course_data = (
            queryset.annotate(clean_course=Trim(Lower("nd_title")))
            .values("clean_course")
            .annotate(count=Count("id"))
        )

        response_data = {
            "gender": [
                {"name": g["clean_gender"] or "Unknown", "value": g["count"]}
                for g in gender_data
            ],
            "status": [
                {"name": s["clean_status"] or "Unknown", "value": s["count"]}
                for s in status_data
            ],
            "course": [
                {"name": c["clean_course"] or "Unknown", "value": c["count"]}
                for c in course_data
            ],
        }
        return Response(response_data)


class KPIView(APIView):
    """
    Provides Key Performance Indicators (KPIs) for the dashboard,
    using specific enrollment statuses for calculations.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Applicant.objects.all()

        if not user.is_staff:
            try:
                user_region = user.userprofile.region
                queryset = queryset.filter(region=user_region)
            except UserProfile.DoesNotExist:
                queryset = queryset.none()

        filtered_queryset = apply_filters(queryset, request.query_params)

        total_applicants = filtered_queryset.count()

        active_students = filtered_queryset.filter(
            application_status__iexact="enrolled"
        ).count()

        completed_courses = filtered_queryset.filter(
            application_status__iexact="closed"
        ).count()

        successful_applications = active_students + completed_courses

        enrollment_rate = 0
        if total_applicants > 0:
            enrollment_rate = round((successful_applications / total_applicants) * 100)

        kpis = {
            "totalStudents": total_applicants,
            "activeStudents": active_students,
            "completedCourses": completed_courses,
            "completionRate": enrollment_rate,
            "courseCategories": {},
        }
        return Response(kpis)


class FilterOptionsView(APIView):
    """
    Provides distinct values for filter dropdowns.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        statuses = list(
            Applicant.objects.annotate(clean_name=Trim("application_status"))
            .values_list("clean_name", flat=True)
            .distinct()
            .exclude(clean_name__isnull=True)
            .exclude(clean_name__exact="")
        )
        courses = list(
            Applicant.objects.annotate(clean_name=Trim("nd_title"))
            .values_list("clean_name", flat=True)
            .distinct()
            .exclude(clean_name__isnull=True)
            .exclude(clean_name__exact="")
        )

        genders = list(
            Applicant.objects.annotate(clean_name=Trim("gender"))
            .values_list("clean_name", flat=True)
            .distinct()
            .exclude(clean_name__isnull=True)
            .exclude(clean_name__exact="")
        )

        regions = list(
            Applicant.objects.annotate(clean_name=Trim("region"))
            .values_list("clean_name", flat=True)
            .distinct()
            .exclude(clean_name__isnull=True)
            .exclude(clean_name__exact="")
        )

        options = {
            "statuses": sorted(statuses),
            "regions": sorted(regions),
            "courses": sorted(courses),
            "genders": sorted(genders),
            "completionStatuses": sorted(statuses),
        }
        return Response(options)
