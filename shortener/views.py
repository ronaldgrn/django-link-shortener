from django.shortcuts import redirect
from django.http import HttpResponse
from shortener import shortern


# Create your views here.
def index(request):
    data = shortern.convert(request.user, "http://google.com/")
    return HttpResponse(data)


def expand(request, link):
    link = shortern.revert(link)
    if link:
        # return HttpResponse(shortern.revert(link))
        return redirect(str(link.full_url))  # TODO: permanent=True
    else:
        HttpResponse("Something bad happened")
