import json
from mealapi import MealApi


class Impress:
    def __init__(self):
        # Inicializa a API e obtém a lista de categorias disponíveis
        self.api = MealApi()
        self.category_list = self.api.get_categories()

    def write_recipe_for_category_txt(self):
        """
        Grava as receitas organizadas por categoria em um arquivo de texto.
        """
        if self.category_list:
            with open('receitas_por_categoria.txt', 'w', encoding='utf-8') as file:
                file.write('Receitas por categoria\n')
                file.write('=====================\n')
                
                # Itera sobre cada categoria e obtém as receitas diretamente da API
                for category in self.category_list:
                    file.write(f'{category}\n')  # Escreve o nome da categoria
                    receitas = self.api.get_meal_by_category(category)  # Chama o método do outro arquivo
                    
                    if receitas:
                        for item in receitas:
                            file.write(f'- {item}\n')  # Escreve cada receita
                    else:
                        file.write('Nenhuma receita nesta categoria\n')  # Caso não haja receitas
                    file.write(f'{"-" * 20}\n')  # Adiciona uma linha separadora

    def write_recipe_for_category_json(self):
        """
        Grava as receitas organizadas por categoria em um arquivo JSON.
        """
        if self.category_list:
            receitas_por_categoria = {}
            
            # Itera sobre cada categoria e obtém as receitas diretamente da API
            for category in self.category_list:
                receitas = self.api.get_meal_by_category(category)  # Chama o método do outro arquivo
                receitas_por_categoria[category] = receitas if receitas else []  # Adiciona receitas ou lista vazia
            
            # Grava o dicionário no arquivo JSON
            with open('./json/receitas_por_categoria.json', 'w', encoding='utf-8') as file:
                json.dump(receitas_por_categoria, file, ensure_ascii=False, indent=4)

    def write_categories_json(self):
        """
        Grava a lista de categorias em um arquivo JSON.
        """
        if self.category_list:
            categories = {"categorias": self.category_list}
            with open('./json/categories.json', 'w', encoding='utf-8') as file:
                json.dump(categories, file, ensure_ascii=False, indent=4)


# Instancia a classe Impress e executa os métodos para gerar os arquivos
imprime = Impress()
imprime.write_categories_json()  # Gera o arquivo JSON com as categorias
imprime.write_recipe_for_category_json()  # Gera o arquivo JSON com as receitas por categoria

