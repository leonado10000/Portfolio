from django.shortcuts import render
from .models import Data,Topics
import datetime
import random
# Create your views here.

imageLink = [
    "https://i.pinimg.com/736x/49/23/57/492357d5a3ea0e4f00b3294ab421b4c7.jpg",
    "https://i.pinimg.com/236x/c4/03/b5/c403b51c014e6753e327abd8e38269db.jpg",
    "https://64.media.tumblr.com/19bfb7fffae85f3fcb0a65e8c0851bcb/tumblr_pipeo8KbpW1xxxd2qo10_r1_400.jpg",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/3c8b03b6-013a-43d7-8b1e-e1c18852a527/dfthdd1-1bd38384-a330-4532-b6ba-2d9ecfd82d4a.png/v1/fill/w_250,h_250/oshi_no_ko_1_folder_by_rkasai14_dfthdd1-250t.png",
    "https://pbs.twimg.com/media/FMNfmj8WYAgT2si.jpg",
    "https://c4.wallpaperflare.com/wallpaper/89/543/779/anime-anime-girls-lycoris-recoil-nishikigi-chisato-inoue-takina-hd-wallpaper-preview.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxDUb0LpmHyTRqbsnXuuvmQaqKFydMeh1HvA",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRiFpWwcWR9mhkJhRbNdQQHTRKFMxWnMWcT8w",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHf31DYC_7zxXdVV76-rfAY2Gm8DJX5lH0qQ",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQiwDZaaetgFdlu5b6m_NrmP3HFDa-EO7SSXA", 
]


def blog(request):
    # print(request)
    if request.method == "POST":
        print(request.POST)
        if request.POST['message_id'] != '':
            a = Data.objects.get(id=request.POST['message_id'])
            a.likes += 1
            a.save()
        else:
            a = Data(textfield=request.POST['a'],sender=request.META.get('REMOTE_ADDR'))
            a.topic_obj = Topics.objects.get(id=request.POST['topic_id'])
            b = Topics.objects.get(id=request.POST['topic_id'])
            b.number_of_messages += 1
            b.save()
            a.save()

    data = Data.objects.all().order_by('-likes')
    topics = Topics.objects.all().order_by('-last_updated')
    topic_id = topics[0].id
    return render(request, 'main.html' ,{
        "data":data,
        "topics":topics,
        "topic_id":topic_id
    })