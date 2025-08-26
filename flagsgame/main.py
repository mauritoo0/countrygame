import requests


def buscar_pais(usuario):
    try:
        url = (f'https://restcountries.com/v3.1/name/{usuario}')
        response = requests.get(url)
        pais = response.json()
        bandera = pais[0]['flags']['png']
        print(bandera)
    except ValueError:
        print("No se encuentra el país")
    

pais_usuario = input("Ingresa, en inglés, el nombre del país que quieres buscar: ")
buscar_pais(pais_usuario)