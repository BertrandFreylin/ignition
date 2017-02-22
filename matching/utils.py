import operator

from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from matching.models import Movies, GenomeScores, Links
import json
import tmdbsimple as tmdb
tmdb.API_KEY = '78d4f3bf87e46dd40677da443ef8ed15'

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
    data = request.POST
    movie_id = data['the_post[id]']
    movie = Movies.objects.get(id=movie_id)
    movie_genres = movie.genres.split('|')
    condition = reduce(operator.and_, [Q(genres__icontains=s) for s in movie_genres])
    first_level = Movies.objects.filter(condition).exclude(id=movie_id).all()
    tag_associated_movies = GenomeScores.objects.filter(movie_id=movie_id).select_related('tag')
    links = Links.objects.filter(movie_id__in=[k.id for k in first_level[:10]]).all()
    results = []
    for movie in first_level[:10]:
        movies_object = tmdb.Movies(int(links.get(movie_id=movie.id).tmdb)).info()
        movies_selected_json = {}
        movies_selected_json['poster'] = 'https://image.tmdb.org/t/p/w500'+movies_object['poster_path']
        movies_selected_json['title'] = movies_object['title']
        results.append(movies_selected_json)
    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
