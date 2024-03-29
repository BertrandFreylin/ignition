import operator
from collections import defaultdict

from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from matching.models import Movies, GenomeScores, Links, GlobalMovieTag, Ratings, GlobalMovieRank
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
    movie_tag = GlobalMovieTag.objects.get(movie_id=movie_id)

    movie_tag_list = GlobalMovieTag.objects.exclude(movie_id=movie_id).all()

    movie_genres = movie_tag.tag.split('|')

    test_genre = []
    movies_matching = {}
    for genre in movie_genres:
        test_genre.append(genre)
        if movie_tag_list.filter(tag__istartswith='|'.join(test_genre)).exists():
            movies_matching = movie_tag_list.filter(tag__istartswith='|'.join(test_genre)).values('movie')
        else:
            break

    rank_movie_list = GlobalMovieRank.objects.filter(movie_id__in=[k['movie'] for k in movies_matching]).order_by('-rating')[:3]

    final_movie_matching = Movies.objects.filter(id__in=[k.movie_id for k in rank_movie_list])

    links = Links.objects.filter(movie_id__in=[k.id for k in final_movie_matching]).all()
    results = []
    for movie in final_movie_matching:
        movies_object = tmdb.Movies(int(links.get(movie_id=movie.id).tmdb)).info()
        movies_selected_json = {}
        movies_selected_json['backdrop_path'] = 'https://image.tmdb.org/t/p/w500' + movies_object['backdrop_path'] if movies_object['backdrop_path'] else ""
        movies_selected_json['poster'] = 'https://image.tmdb.org/t/p/w500'+movies_object['poster_path'] if movies_object['poster_path'] else ''
        movies_selected_json['title'] = movies_object['title']
        movies_selected_json['id'] = movies_object['id']
        movies_selected_json['runtime'] = movies_object['runtime']
        movies_selected_json['release_date'] = movies_object['release_date'].split('-')[0]
        movies_selected_json['vote_average'] = str([k.rating for k in rank_movie_list if k.movie_id == movie.id][0])
        movies_selected_json['overview'] = movies_object['overview']
        movies_selected_json['tmdb_path'] = 'https://www.themoviedb.org/movie/' + str(movies_object['id'])
        movies_selected_json['imdb_path'] = 'http://www.imdb.com/title/' + str(movies_object['imdb_id']) if movies_object['imdb_id'] else ''
        results.append(movies_selected_json)
    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def reduce_tag():

    total_movie_list = Movies.objects.all()
    tag_list = GenomeScores.objects.all()
    for movie in total_movie_list:
        best_tag_listing = tag_list.filter(movie_id=movie.id).select_related('tag').values_list('relevance','tag__tag')
        best_tag_movie = [k[1].lower() for k in sorted(best_tag_listing, key=lambda x: float(x[0]), reverse=True)[:4]]
        total_movie_tag = '|'.join(best_tag_movie) if best_tag_movie else movie.genres
        GlobalMovieTag(movie_id=movie.id, tag=total_movie_tag).save()


def reduce_ranking():

    total_rating_list = Ratings.objects.all()
    merge_list = defaultdict(list)
    for rate in total_rating_list:
        merge_list[rate.movie_id].append(rate.rating)

    for movie, rates in merge_list.items():
        average = sum(rates)/len(rates)
        GlobalMovieRank(movie_id=movie, rating=average).save()
