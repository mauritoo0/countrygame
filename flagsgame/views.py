from django.shortcuts import render, redirect
from .utils import country_request, check_flag, get_random_country_by_difficulty
from .models import Score
import pycountry


#View for the index template where the user selects difficulty
def index(request):
    request.session.flush()#Delete session at the time "index" is opened
    scoreboard = Score.objects.all()[:10]
    if request.method == 'POST':# User selects the difficulty level through the form
        if 'player-name' in request.POST:
            request.session['player'] = request.POST.get('player-name', None)
            if 'easy' in request.POST:
                request.session['difficulty'] = 'begginer'
            elif 'intermediate' in request.POST:
                request.session['difficulty'] = 'intermediate'
            elif 'hard' in request.POST:
                request.session['difficulty'] = 'hard' 
            
            
            
        
        request.session.pop('random_country', None)# Clear previous session data and redirect to the game

        return redirect ('game')
    
    return render(request, 'index.html', 
                {'scoreboard': scoreboard})




#Game template where users guess the flags
def game(request):
    # If reset button is pressed, clear session and reload page
    if request.method == 'POST' and 'reset' in request.POST:
        request.session.pop('random_country', None)
        return redirect ('game')
    # If the exit button is pressed, clear the session and go back to the index
    if request.method == 'POST' and 'exit' in request.POST:
        request.session.flush()
        return redirect ('index')
    
    
    flag = None 
    correct_flag = None 
    wrong_flag = None 
    user_country_name = None
    random_country_name = None
    
    
    if 'random_country' not in request.session: # If there's no random country stored in the session yet
        # Retrieve difficulty from session and get a random country accordingly
        difficulty = request.session.get('difficulty')
        random_country = get_random_country_by_difficulty(difficulty)
        request.session['random_country'] = random_country.alpha_2.upper()
    
    random_country_code = request.session['random_country']# Store the random country (alpha) name in a variable
    
    # Get the flag and population of the selected country using the API
    random_flag = country_request(random_country_code, info='flag')
    random_flag_population = country_request(random_country_code, info='population')        
        
    if random_country_code:# If a random country is stored in session, get its name using its alpha code
        random_country_name = pycountry.countries.get(alpha_2=random_country_code).name
    
    #Initializing points and attempts     
    if 'points' not in request.session:
        request.session['points'] = 0

    if 'attempts' not in request.session:
        request.session['attempts'] = 3
    
    game_over = False
    
    # Check user input and evaluate the guess using check_flag()
    if request.method == 'GET':
        user_input = request.GET.get('country')
        if user_input:
            result = check_flag(user_input.strip(), random_country_code, request)

            if result.get('redirect'):
                return redirect('index') # Redirect to index if user runs out of attempts

            correct_flag = result.get('correct_flag')
            wrong_flag = result.get('wrong_flag')
            flag = result.get('flag')
            user_country_name = result.get('user_country_name')
            game_over = result.get('game_over', False)

    return render(request, 'game.html', {
        'random_flag': random_flag,        
        'flag': flag,
        'correct_flag': correct_flag,
        'wrong_flag': wrong_flag,
        'random_country_code': random_country_name,
        'user_country_name': user_country_name,
        'random_flag_population': random_flag_population,
        'points': request.session['points'],
        'attempts': request.session['attempts'],
        'game_over': game_over,
        
})



            









  
  
     
    
    
    
    
    
    
        
