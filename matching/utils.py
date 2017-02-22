from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from matching.models import Movies
import json

def get_movies(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        movies = Movies.objects.filter(title__icontains=q)[:20]
        results = []
        for movie in movies:
            movies_json = {}
            movies_json['id'] = movie.id
            movies_json['label'] = movie.title
            movies_json['value'] = movie.title
            results.append(movies_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@csrf_exempt
def find_movies(request):
    data = []
    return HttpResponse(data)