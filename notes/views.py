from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Note
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .serializers import NoteSerializer


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


@api_view(['GET', 'POST'])
def api_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        new_note_data = request.data
        note.title = new_note_data['title']
        note.content = new_note_data['content']
        note.tag = new_note_data['tag']
        note.save()

    serialized_note = NoteSerializer(note)

    return Response(serialized_note.data)


@api_view(['GET', 'POST'])
def api_notes(request):
    if request.method == 'POST':
        new_note_data = request.data
        new_note = Note(title=new_note_data['title'],
                        content=new_note_data['content'], tag=new_note_data['tag'])
        new_note.save()

    all_notes = Note.objects.all()
    serialized_notes = NoteSerializer(all_notes, many=True)

    return Response(serialized_notes.data)
