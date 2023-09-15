from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from markdown2 import Markdown
from . import util

# markdown converter
markdowner = Markdown()

# form to add new entry
class AddForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


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

    # make a list of substrings that matched the entries
    matches = []

    # if there is no direct match, check for substrings andd add the entries to Match list
    if query not in all_entries:
        for each in all_entries:
            if query in each:
                matches.append(each)
        return render(request, "encyclopedia/search.html", {
            "matches" : matches,
            "query" : query
        })
    else:
        # if query matches an entry, redirect to that page
        return HttpResponseRedirect(reverse("wiki:pages", kwargs={'entry': query}))
    

def add(request):
    if request.method == "POST":

        # create a new django form
        form = AddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # show error if entry already exists
            if title in util.list_entries():
                return HttpResponse("This entry already exists")
            
            # save entry and redirect to the new page
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:pages", kwargs={'entry': title}))
        
    
    return render(request, "encyclopedia/new.html", {
        "form" : AddForm()
    })

