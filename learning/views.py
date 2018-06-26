from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404


def index(request):
    '''learning index'''
    return render(request, '../templates/learning/index.html')


@login_required
def topics(request):
    '''show the topics'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, '../templates/learning/topics.html', context)


@login_required()
def topic(request, topic_id):
    """show the items in topic"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, '../templates/learning/topic.html', context)


@login_required()
def new_topic(request):
    """add new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning:topics'))

    context = {'form': form}
    return render(request, '../templates/learning/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    """add new item for topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():

            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, '../templates/learning/new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    "编辑既有条目"
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning/edit_entry.html', context)

