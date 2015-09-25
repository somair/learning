from django.shortcuts import render
from django.shortcuts import redirect

from decks import list_decks, load_deck
from deck_parser import parse_md
from django.http import HttpResponse
from django.http import JsonResponse

from models import Result

def index(request):
    return redirect('/quizzes/list/')

#Shows a list of all available decks
def listing(request):
    #Get available decks
    decks = list_decks()
    #Based on the decks, get the last score and date
    r = Result.objects.filter(name__in=decks)
    #Based on the decks, get the next date to be done
    #Zip lists 
    decks = [{'name':name, 'last_result':res} for name,res in zip(decks, r)]
    context = {'decks': decks}
    return render(request, 'quizzes/listing.html', context)

#Starts a new quiz based on a selected deck
def detail(request, deck_name):
    txt = load_deck(deck_name)
    html = parse_md(txt)
    print(len(html))
    context = {'cards' : html, 'deck_name': deck_name}
    return render(request, 'quizzes/quiz.html', context)

#Saves the result of a quiz in the database (Result)
#quiz_name, quiz_score, date
def save(request):
    if request.method == 'POST':
        #Create new Result object and populate it with the data
        name = request.POST['name']
        score = float(request.POST['score'])
        res = Result(name=name, score=score)
        #Save it
        res.save()
        #Schedule next date
        #...
        return HttpResponse('Result saved.')

#Show the results for a given deck
#loads html and then and ajax request actually fetches the data
def results(request, deck_name):
    context = {'deck_name': deck_name}
    return render(request, 'quizzes/quiz_results.html', context)

#Fetch results for a given deck
#returns a json response
def fetch_results(request, deck_name):
    #Query the db for the Results for that deck
    r = Result.objects.filter(name=deck_name)
    #Send datetimes and scores as lists
    dates  = map(lambda x: x.date.strftime("%Y-%m-%d %H:%M:%S") , r)
    scores = map(lambda x: x.score, r)
    print dates
    return JsonResponse({'dates':dates, 'scores':scores})