# search_indexes.py

from haystack import indexes
from .models import Project, Cause, Event, Blog

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    location = indexes.CharField(model_attr='location')
    description = indexes.CharField(model_attr='description')  # Add this line

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class CauseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')  # Add this line

    def get_model(self):
        return Cause

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')  # Add this line
    location = indexes.CharField(model_attr='location')  # Add this line

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='message')  # Add this line

    def get_model(self):
        return Blog

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

# Add similar classes for Event and Blog models