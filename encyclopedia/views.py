from django.shortcuts import render
from markdown2 import Markdown
from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, entry):
    text = markdowner.convert(util.get_entry(entry))
    return render(request, "encyclopedia/entries.html", {
        "data" : text,
        "entry" : entry
    })