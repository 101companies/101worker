# Create your views here.
from django.http import HttpResponse

def hello(request):

    return HttpResponse('Hello World', content_type='text/plain')


