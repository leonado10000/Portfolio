import datetime
from django.shortcuts import render
from .models import projectTable
from Portfolio.views import welcoming_user 

# Create your views here.
@welcoming_user
def base(request):
    if request.method == "POST":
        print("something",request.POST,type(request.POST['start-date']))
        obj = projectTable(
                projectTopic = request.POST['Project-Topic'],
                projectName = request.POST['Project-Title'],
                projectDescription = request.POST['Project-description']
        )
        
        if request.POST['start-date'] != "":
            obj.startDate = request.POST['start-date']
        if request.POST['end-date'] != "":
            obj.endDate = request.POST['end-date']
        
        obj.save()

    data = projectTable.objects.all()
    return render(request, "base.html", {
        "data":data
    })

@welcoming_user
def delete(request):
    obj = projectTable.objects.filter(id=request.POST['project-id'])[0]
    obj.delete()
    data = projectTable.objects.all()
    return render(request, "base.html", {
        "data":data
    })