from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello(request):
  return render(request, "hello.html", {"name": "you"});


def page(request):
   text = """<h1>this is another page! hi</h1>"""
   return HttpResponse(text)