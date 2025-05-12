import time 
import requests


def format_categories(category_list):
    for item in category_list:
        print(f' -{item}')
        

def get_meal_categories():
    api_url = "https://www.themealdb.com/api/json/v1/1/list.php?c=list"
    category_names = []
    
    try:
        response = requests.get(api_url, timeout=10)
        # Verificação se a requisição foi bem sucedida em 10 segundos.
        if response.status_code == 200:
            data = response.json()
            meal_categories = data['meals']
            
            category_names = [category["strCategory"] for category in meal_categories]
            return format_categories(category_names)
        else:
            print(f'Erro ao acessar a API! Codigo: {response.status_code}')
    
    except requests.exceptions.Timeout:
        print('Timeout')

def get_meal_by_category(category):
    api_url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            meals = data['meals']
            
            meal_names = [meal['strMeal'] for meal in meals]
            print(f'\nPratos da categoria {category}:')
            print('\n'.join(meal_names))
            
    except requests.exceptions.Timeout:
        print('Timeout')

def get_meal(meal_name):
    """Função que busca a receita de um prato especifico na API do TheMealDb.

    Args:
        meal_name (str): Nome do prato a ser buscado
    """
    api_url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
    ingredients_list = [] # Lista para armazenar os ingredientes e medidas, para facilitar a leitura
    
    try:
        response = requests.get(api_url, timeout=10)
        # Verificação se a requisição foi bem sucedida em 10 segundos.
        if response.status_code == 200:
            data = response.json()
            
            # Verifica se a resposta da API é válida
            if data['meals'] is None:
                print('Nenhum resultado encontrado. Você digitou o nome correto?')
                return None
            
            # Se a resposta for válida, armazena a primeira receita que encontrar que tenha o nome digitado
            meal_data = data["meals"][0]
            
            # Coleta de dados
            meal_title = meal_data['strMeal']
            
            # Como no mealDb a quantidade de ingredientes é variável, verifica quantos ingredientes aparecem
            for i in range(1, 21):
                ingredient = meal_data[f'strIngredient{i}']
                measure = meal_data[f'strMeasure{i}']
                if ingredient and measure:
                    ingredients_list.append(f'{ingredient} - {measure}')
                    
            instructions = meal_data['strInstructions']
            
            # Saída de dados        
            print(f'\nReceita: {meal_title}')
            
            print('\nIngredients:')
            for ingredient in ingredients_list:
                print(f' - {ingredient}')
            
            print(f'\nInstructions: {instructions}')
            
        else:
            print('Erro ao acessar a API, tente mais tarde!')

    except requests.exceptions.Timeout:
        print('Timeout')
        
    except requests.exceptions.TooManyRedirects:
        print('Too many redirects, try again later')



start_time = time.perf_counter()

get_meal_categories()
get_meal_by_category('Vegetarian')
get_meal('Dal')

end_time = time.perf_counter()

print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")