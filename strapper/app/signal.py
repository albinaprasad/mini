from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobPreference, Jobs
from .scrapper2 import main
import asyncio

@receiver(post_save, sender = JobPreference)
def post_save_handler(sender, instance, created, **kwargs):
    if created:
        jobs = asyncio.run(main(instance.title,"India"))
        for job in jobs:
            print(job['title'])
            j = Jobs(title=job['title'],location=job['location'],company=job['company'],link=job['link'],description=job['description'],job_type=instance)
            j.save()
        print("new entry...")