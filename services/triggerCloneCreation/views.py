from django.http import HttpResponse
import os

def trigger(request):
    os.system('cd ../../modules/cloneCreation; make run')
    return HttpResponse('Done.', content_type='text/plain')


