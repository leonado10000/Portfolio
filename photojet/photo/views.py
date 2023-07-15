from django.shortcuts import render
from .models import EVENT
# Create your views here.
def add_event(request):
    if request.method == "POST":
        data = request.POST
        date = data['date']
        place = data['place']
        link = data['link']
        desc = data['desc']
        main = data['main']
        n = len(EVENT.objects.all())
        d = EVENT(E_id=n+1,date=date,place=place,photo_link=link,desc=desc,main_topic=main)
        d.save()
        dat = EVENT.objects.all()
        return render(request, 'events.html',{
            "data":dat
        })
    else:
        return render(request, "add_event.html")

def event_page(request):
    dat = EVENT.objects.all()
    return render(request, 'events.html',{
        "data":dat
    })

def page(request, id):
    if request.method=="POST":
        data = request.POST
        print(data)
        choice = data["next"]
        if choice == '1':
            id += 1
            if id == len(EVENT.objects.all())+1 :
                print("works")
                id = 1
        else:
            id -= 1
            print(id)
            if id == 0 or id == '0':
                id = len(EVENT.objects.all())
                
                print("works",id)

    data = EVENT.objects.get(E_id = id)
    return render(request, "page.html" ,{
        "data":data
    })