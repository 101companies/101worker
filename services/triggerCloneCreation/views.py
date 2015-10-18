from django.http import HttpResponse
import subprocess

def trigger(request):
    output = subprocess.Popen(["whoami"], cwd="../../modules/cloneCreation", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = output.stdout.read() + "\n"
    output = subprocess.Popen(["make", "run"], cwd="../../modules/cloneCreation", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result += output.stdout.read()
    return HttpResponse(result, content_type='text/plain')


