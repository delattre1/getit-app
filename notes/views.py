from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Note


def deleteNote(id_):
    note = Note.objects.get(id=id_)
    note.delete()


def updateNote(id_, title, content, tag):
    note_item = (Note.objects.get(id=id_))
    note_item.title, note_item.content = title, content
    note_item.tag = tag
    note_item.save()


def createNote(title, content, tag):
    note_item = Note(title=title, content=content, tag=tag)
    note_item.save()


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = request.POST.get('tag')
        id_ = request.POST.get('id-hidden')
        deleteId = request.POST.get('deleteNote')

        if deleteId != None:
            deleteNote(deleteId)

        elif id_ != 'None':
            updateNote(id_, title, content, tag)

        else:
            createNote(title, content, tag)

        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html',
                      {'notes': all_notes})


def tagsList(request):
    tags = Note.objects.values('tag').distinct()
    print(f'tags: {tags}')

    list_tags = [i['tag'] for i in tags]
    return render(request, 'notes/tagsList.html', {'all_tags': list_tags})


def tag(request, tag_):
    notes_with_tag = Note.objects.filter(tag=tag_)
    print(tag_)
    print(notes_with_tag)
    return render(request, 'notes/tag.html', {'notes': notes_with_tag})
