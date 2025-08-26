import requests, random, pycountry
from .models import Score


# Function to request flag or population of a country from the REST Countries API
def country_request(alpha_code, info='flag'):
    response = requests.get(f'https://restcountries.com/v3.1/alpha/{alpha_code}')
    if response.status_code != 200:
        return None  
    
    try:
        data = response.json()
        
    except ValueError:
        return None  

# If data is retrieved successfully, extract the country info depending on the 'info' parameter
    if isinstance(data, list) and data:
        country_data = data[0]

        if info == 'flag':
            return country_data.get('flags', {}).get('png')
        elif info == 'population':
            return country_data.get('population')
    
    return None



# Function to evaluate the user's input against the randomly selected country
def check_flag(user_input, random_country_code, request):
    try:
        user_country = pycountry.countries.lookup(user_input)# Look up the country entered by the user using pycountry

        user_country_name = user_country.name #Saving the name to return to template
        flag = country_request(user_country.alpha_2)
        
        if user_country.alpha_2.upper() == random_country_code.upper():# If the input country matches the randomly selected one

            request.session['points'] += 1
            del request.session['random_country']#deleting session to restart game if user win round
            return {
                'correct_flag': "Great!",
                'wrong_flag': None,
                'flag': flag,
                'user_country_name': user_country_name,
                'redirect': False,
                'game_over': False,
            }
        else:#If they don't match
            request.session['attempts'] -= 1 if request.session['attempts'] > 0 else 0
            if request.session['attempts'] == 0:
                save_score(request)
                return { 'game_over': True }
            
            return {
                'correct_flag': None,
                'wrong_flag': "Fail! Try again!",
                'flag': flag,
                'user_country_name': user_country_name,
                'redirect': False,
                'game_over': False,
            }

    except LookupError:# If the input is not a valid country name

        user_country_name = user_input
        request.session['attempts'] -= 1 if request.session['attempts'] > 0 else 0
        if request.session['attempts'] == 0:
                save_score(request)
                return { 'game_over': True }

        
        return {
            'correct_flag': None,
            'wrong_flag': "Fail! Try again!",
            'flag': None,
            'user_country_name': user_country_name,
            'redirect': False,
            'game_over': False,
        }   




# Function to get a random country based on the difficulty in the session
def get_random_country_by_difficulty(difficulty):
    countries = list(pycountry.countries)
    while True:
        random_country = random.choice(countries)
        population = country_request(random_country.alpha_2.upper(), info="population")
        if population is None:
            continue
        if difficulty == "hard" and population <= 10_000_000:
            return random_country
        elif difficulty == "intermediate" and 10_000_000 < population <= 70_000_000:
            return random_country
        elif difficulty == "begginer" and population > 70_000_000:
            return random_country


#Add score to database once player lost
def save_score(request):
    playername = request.session.get('player', 'Anonymous') 
    total_score = request.session.get('points', 0)
    Score.objects.create(player_name=playername, player_score=total_score)
    


#Reset session
def reset_game_session(request):
    request.session.pop('random_country', None)
    request.session['points'] = 0
    request.session['attempts'] = 3



