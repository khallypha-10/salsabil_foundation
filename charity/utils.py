from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from .models import Event, Project, Cause, Blog

def search_models(query):
    # Debug: Print the query
    print(f"Search Query: {query}")

    # Define the search vector and query
    vector = SearchVector('title', 'description')  # Add more fields as needed
    search_query = SearchQuery(query)
    rank = SearchRank(vector, search_query)

    # Search across all models
    results_model1 = Event.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')
    results_model2 = Blog.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')
    results_model3 = Project.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')
    results_model4 = Cause.objects.annotate(rank=rank).filter(rank__gte=0.1).order_by('-rank')

    # Debug: Print the number of results from each model
    print(f"Event Results: {results_model1.count()}")
    print(f"Blog Results: {results_model2.count()}")
    print(f"Project Results: {results_model3.count()}")
    print(f"Cause Results: {results_model4.count()}")

    # Combine results
    combined_results = list(results_model1) + list(results_model2) + list(results_model3) + list(results_model4)
    combined_results.sort(key=lambda x: x.rank, reverse=True)  # Sort by rank

    # Debug: Print the combined results
    print(f"Combined Results: {combined_results}")

    # Handle empty results
    if not combined_results:
        print("No results found.")
        return []

    return combined_results