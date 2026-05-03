from html.parser import HTMLParser
from django.shortcuts import render
import os
import json
import httpx
import random as rn
from django.conf import settings
from Portfolio.views import welcoming_user
from Portfolio.models import Visitor
# Create your views here.

s = [
    "Express Love, Seek Empathy",
    "Everyone\'s Love Stands Empty",
    "Embrace Life\'s Surprising Experiences",
    "End Love, Start Emptiness",
    "Escape Limits, Seek Ecstasy",
    "Escape Lies, Seek Euphoria"
]

@welcoming_user
def func(request):
    i = rn.randint(0,len(s)-1)
    return render(request, "else.html", {
        "heading":s[i],
        "theme": {"text_color": "#ffefd5", "bg_color": "#a76b47", "bg_border": "transparent","border_radius": "5px"}
    })

@welcoming_user
def quests(request):
    return render(request, "quests.html")

@welcoming_user
def WebResume(request):
    return render(request,"WebResume.html")

@welcoming_user
def games_home(request):
    return render(request,"games/games_home.html")

@welcoming_user
def terminal_view(request):
    themes = {}
    with open(os.path.join(settings.BASE_DIR,'core','static','themes.json'), 'r') as f:
        themes = json.load(f)
    

    current_theme = request.GET.get('theme', 'neon')
    if current_theme not in themes:
        current_theme = 'neon'

    context = {
        'themes_json': json.dumps(themes),
        'current_theme': current_theme,
        'theme': themes[current_theme],
    }
    return render(request, 'terminal.html', context)

@welcoming_user
def visitors(request):
    return render(request, "visitors.html", {
        "visitors": Visitor.objects.all()
    })

def scrape_riot_jobs():
    base_url = "https://www.riotgames.com"
    target_url = f"{base_url}/en/work-with-us/jobs#craft=software-engineering-group"

    # Get the HTML content
    response = httpx.get(target_url)
    tree = HTMLParser(response.text)

    jobs = []
    for li in tree.css("li.job-row.job-row--body"):
        link_tag = li.css_first("a.job-row__inner.js-job-url")
        role = li.css_first("div.job-row__col--primary").text(strip=True)
        category = li.css_first("div.job-row__col--secondary").text(strip=True)

        if "software" in category.lower() or "data" in role.lower():
            job_url = base_url + link_tag.attributes.get("href", "")
            jobs.append({"role": role, "link": job_url})

    return jobs
