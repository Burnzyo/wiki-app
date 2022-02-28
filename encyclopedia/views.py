from random import randint
from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django import forms

markdowner = Markdown()

class NewPageForm(forms.Form):
    title = forms.CharField(required = True, widget = forms.TextInput(attrs={
        "class": "form-control col-sm-2 mb-2",
        "placeholder": "New Title"
    }))
    content = forms.CharField(required = True, widget = forms.Textarea(attrs={
        "class": "form-control mb-4",
        "placeholder": "Write here the content of the new entry"
    }))

class EditPageForm(forms.Form):
    content = forms.CharField(initial="Hola", required = True, widget = forms.Textarea(attrs={
        "class": "form-control mb-4"
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def navigate(request, title):
    if title.lower() in (name.lower() for name in util.list_entries()):
        return render(request, "encyclopedia/navigate.html", {
            "title": getTitle(title),
            "entry": convert(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/notfound.html")

#Mardown to HTML
def convert(markdown):
    return markdowner.convert(markdown)

#Used for getting the exact title for the html file
def getTitle(title):
    for name in util.list_entries():
        if title.lower() == name.lower():
            return name

def search(request):
    query = request.GET.get("q", "")
    if query is None or query == "":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "query": ""
        })
        
    matches = [match for match in util.list_entries() if query.lower() == match.lower()]
    matchesSubstring = [match for match in util.list_entries() if query.lower() in match.lower()]

    if len(matches) == 1:
        return redirect("wiki:navigate", matches[0])
    
    if len(matchesSubstring) == 0:
        return render(request, "encyclopedia/notfound.html")

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matchesSubstring
    })

def randomEntry(request):
    i = randint(0, len(util.list_entries()) - 1)
    entries = util.list_entries()
    return redirect("wiki:navigate", entries[i])

def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title.lower() in (name.lower() for name in util.list_entries()):
                return render(request, "encyclopedia/add.html", {
                   "form": form,
                   "error": "An entry with that title already exists."
                })
            else: 
                util.save_entry(title, content)
                return redirect("wiki:navigate", title)
    
    return render(request, "encyclopedia/add.html", {
        "form": NewPageForm()
    })

def editEntry(request, title):
    initialValue = {
        "content": util.get_entry(title)
    }

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("wiki:navigate", title)

    return render(request, "encyclopedia/edit.html", {
        "form": EditPageForm(initial=initialValue),
        "title": title
    })
