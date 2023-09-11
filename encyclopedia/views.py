from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from markdown2 import Markdown
from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def pages(request, entry):
    # if entry is not listed in the entries then render a page not found
    all_entries = util.list_entries()
    if entry not in all_entries:
        return render(request, "encyclopedia/not_found.html")
    
    # convert md to html and save into a variable
    text = markdowner.convert(util.get_entry(entry))

    # render html page using the converted html and entry as a title
    return render(request, "encyclopedia/pages.html", {
        "data" : text,
        "entry" : entry
    })


def search(request):
    # get the query entered and the available pages
    query = request.POST.get("q")
    all_entries = util.list_entries()

    # if query matches an entry, redirect to that page
    if query not in all_entries:
        return render(request, "encyclopedia/not_found.html")
    else:
        return HttpResponseRedirect(reverse("wiki:pages", kwargs={'entry': query}))