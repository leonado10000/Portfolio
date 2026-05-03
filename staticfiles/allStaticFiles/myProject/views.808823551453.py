import datetime
from django.shortcuts import render
from .models import projectTable

# Create your views here.
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

def delete(request):
    obj = projectTable.objects.filter(id=request.POST['project-id'])[0]
    obj.delete()
    data = projectTable.objects.all()
    return render(request, "base.html", {
        "data":data
    })