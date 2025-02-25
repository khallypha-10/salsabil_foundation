from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from .models import Event, Project, Cause, Blog

def search_models(query):
    vector = SearchVector('title')  # Add fields you want to search
    search_query = SearchQuery(query)
    rank = SearchRank(vector, search_query)

    # Search across all models
    results_model1 = Event.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')
    results_model2 = Blog.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')
    results_model3 = Project.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')
    results_model4 = Cause.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')
    # Combine results
    combined_results = list(results_model1) + list(results_model2) + list(results_model3) + list(results_model4)
    combined_results.sort(key=lambda x: x.rank, reverse=True)  # Sort by rank

    return combined_results