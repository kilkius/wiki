from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from markdown2 import Markdown
from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, entry):
    # if entry is not listed in the entries then render a page not found
    all_entries = util.list_entries()
    if entry not in all_entries:
        return render(request, "encyclopedia/not_found.html")
    
    text = markdowner.convert(util.get_entry(entry))
    return render(request, "encyclopedia/entries.html", {
        "data" : text,
        "entry" : entry
    })

def search(request):
    # if query matches an entry, redirect to that page
    query = request.GET.get("q")
    all_entries = util.list_entries()

    if query not in all_entries:
        return HttpResponse("Not found")
    
    text = markdowner.convert(util.get_entry(query))
    
    return render(request, "encyclopedia/entries.html", {
        "data" : text,
        "entry" : query
    })


    # return HttpResponseRedirect(reverse(index))