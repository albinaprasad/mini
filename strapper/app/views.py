from django.shortcuts import render
from .models import User, Jobs, JobPreference, JobOpted
from django.shortcuts import redirect,HttpResponse
import hashlib
from .scrapper2 import main
import asyncio
import json
from django.core.serializers import serialize

def set_cookie(res,data):
    for key,value in data.items():
        res.set_cookie(key=key,value=value,max_age=12*3600)
    pass

def launch(req):
    return render(req,"index.html")

def select_job(req):
    print(req.COOKIES)
    if req.method == "POST":
        jsonJobs = json.loads(req.body.decode('utf-8'))
        user = User.objects.filter(email=req.COOKIES['email']).first()
        try:
            for job in jsonJobs:
                print(job)
                job = JobPreference.objects.filter(title=job['text']).first()
                print(job)
                jobOpted = JobOpted(user_id=user,jobid=job)
                jobOpted.save()
            user = User.objects.filter(email=req.COOKIES['email']).first()
            return HttpResponse(json.dumps({'result':"/"+user.hash}))
        except Exception as e:
            print("Probably unique Constraint exception...")
            return HttpResponse(json.dumps({'result':"/"+user.hash}))
    job_type = JobPreference.objects.all()
    return render(req,"select.html",{
        'jobs':job_type
    })

def signup(req):
    print("signup")
    if req.method == "POST":
        error=None
        success=None
        user = User.objects.filter(email=req.POST.get('email')).first()
        if user is not None:
            error="Email already taken"
        else:
            print("user is None")
            user=User(name=req.POST['username'],password=req.POST['password'],email=req.POST['email'])
            user.save()
            success = "Account created successfully"
            res = redirect("/select_job/")
            set_cookie(res,req.POST)
            return res
        res = render(req,'elixir/assets/login/signup.html',{
            'error' : error,
            'success' : success
        })
        res.set_cookie(key='user',value="user1")
        return res
    elif req.method == "GET":
        return render(req,'elixir/assets/login/signup.html')

def login(req):
    print("login")
    if req.method == "POST":
        email = req.POST.get('email')
        password = req.POST.get('password')
        user = User.objects.filter(email=email,password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()
        if user is None:
            return render(req,'elixir/assets/login/signup.html',{ 'error':'No user found','success': None})
        else:
            res = redirect("/"+user.hash) 
            set_cookie(res,req.POST)
            return res
    else:
        print("else working...")
        res = render(req,'elixir/assets/login/login.html')
        return res
    pass
from django.db.models import Q

def dynamic(req,slug):
    print(slug)
    search = req.GET.get('search')
    print(search)
    if search is not None:
        jobs = Jobs.objects.filter(Q(title__icontains=search) | Q(description__icontains=search)).all()
        serialized_queryset = serialize('json', jobs)
        return render(req, 'account.html', {
        'jobs': jobs,
        'job_json':serialized_queryset
        })

    user = User.objects.filter(hash=slug).first()
    job_preference_ids = JobOpted.objects.filter(user_id=user).values_list('jobid', flat=True)
    jobs = Jobs.objects.filter(job_type__in=job_preference_ids)
    serialized_queryset = serialize('json', jobs)
    return render(req, 'account.html', {
        'jobs': jobs,
        'job_json':serialized_queryset
    })

def account(req):
    print("callled account")
    return render(req,'usersetting.html')

def change(req):
    return render(req,'account.html')