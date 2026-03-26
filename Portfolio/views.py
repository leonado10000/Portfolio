from django.shortcuts import render
from .models import Visitor
from utils.bronzelogger import bronzelogger

# Create your views here.
# ======================================
#               Data
# ======================================
projects_s = [
    [
        "https://static.vecteezy.com/system/resources/thumbnails/027/376/701/small/monitor-lo-fi-retro-animation-video.jpg",
        "Operating System, api, Algorithms, data Scrutures"
    ],
    [
        "https://img.freepik.com/premium-photo/heartshaped-electronic-device-with-complex-circuitry-fusion-human-emotions-machine-learning-concept-generative-ai-illustration_124717-2739.jpg",
        "Machine Learning"
    ],
    [
        "https://images-platform.99static.com//60ymdkeAKMHeEuZlulWzS5niuzk=/0x0:1055x1055/fit-in/500x500/99designs-contests-attachments/74/74540/attachment_74540382",
        "Web Dev"
    ],
    [
        "https://i.stack.imgur.com/Ph3Ou.jpg",
        "Python Software Project"
    ]
]
stacks = [
    ["rgb(132, 104, 104)","Pandas| Numpy| streamlit"],
    ["rgb(92, 116, 86)","Red Hat| Ubantu"],
    ["rgb(123, 127, 95)","Django| Html-Css| JS"],
    ["rgb(107, 97, 130)","Docker| WSL"],

]
certificates = [
    ["https://certificates.simplicdn.net/share/4397060_1688564792.pdf","Data Science with Python","simply learn"],
    ["https://www.kaggle.com/learn/certification/leonado10000/pandas","Pandas","Kaggle"],
    ["https://www.kaggle.com/learn/certification/leonado10000/intro-to-machine-learning","intro-to-machine-learning","Kaggle"],
    ["https://onlinecourses.nptel.ac.in/noc23_cs104/preview","Applied Accelerated Artificial Intelligence","NPTEL"]
]


from functools import wraps

def welcoming_user(view_func):
    @wraps(view_func)
    def wrapper(req, *args, **kwargs):
        ip = req.META.get('REMOTE_ADDR')

        visitor, created = Visitor.objects.get_or_create(ipaddress=ip)
        visitor.useragent = req.META.get('HTTP_USER_AGENT', 'Unknown')
        visitor.acceptedlanguage = req.META.get('HTTP_ACCEPT_LANGUAGE', 'Unknown')
        visitor.acceptedencoding = req.META.get('HTTP_ACCEPT_ENCODING', 'Unknown')
        visitor.save()

        print("=====================")
        print(f"Hello, from: {view_func.__name__}")
        print(f"Hello, to  : {visitor.ipaddress} (created={created})")
        print("=====================")

        return view_func(req, *args, **kwargs)
    return wrapper


@welcoming_user
@bronzelogger
def index(request):
    n = 0
    if n :
        return render(request, 'dist/index.html',{
            "certificates":certificates,
            "projects":projects_s,
            "stacks":stacks
        })
    return render(request, 'v3/index.html')

@welcoming_user
@bronzelogger
def projects(request):
    return render(request, 'v1/projects.html'  , {
        "theme": {"text_color": "white", "bg_color": "#1e1e1e", "bg_border": "transparent","border_radius": "10px"}
    })

@welcoming_user
@bronzelogger
def v2(request):
	return render(request, 'v2/base.html')

@welcoming_user
@bronzelogger
def v1(request):
	return render(request, 'v1/index.html')
