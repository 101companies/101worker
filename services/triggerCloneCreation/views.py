from django.http import HttpResponse
import os

def trigger(request):
    exitcode = os.system('cd ../../modules/cloneCreation; make run')
    return HttpResponse(str(exitcode), content_type='text/plain')


