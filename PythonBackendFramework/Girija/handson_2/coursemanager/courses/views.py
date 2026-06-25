from django.http import HttpResponse


def home(request):
    return HttpResponse("Course Management System")