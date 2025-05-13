import requests

class MealApi:
    
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1/"        

    def get_categories(self):
        api_url = "https://www.themealdb.com/api/json/v1/1/list.php?c=list"
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                meal_categories = data['meals']
                category_names = [category["strCategory"] for category in meal_categories]
                return category_names  
            else:
                return(f'Erro ao acessar a API! Codigo: {response.status_code}')
        except requests.exceptions.Timeout:
            return('Timeout')

    def get_meal_by_category(self,category):
        api_url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                meals = data['meals']
                
                meal_names = [meal['strMeal'] for meal in meals]
                return meal_names
                
        except requests.exceptions.Timeout:
            return('Timeout')

    def get_recipe(self,meal_name):
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
                
                return {
                    'title': meal_title,
                    'ingredients': ingredients_list,
                    'instructions': instructions
                }
                
            else:
                return(f'Erro ao acessar a API, Erro: {response.status_code}')

        except requests.exceptions.Timeout:
            return('Timeout')
            
        except requests.exceptions.TooManyRedirects:
            return('Too many redirects, try again later')