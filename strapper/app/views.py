from django.shortcuts import render


# Create your views here.
def launch(req):
    return render(req,"index.html")

def selectjob(req):
    return render(req,"base.html")

def account(req):
    return render(req,'account.html')