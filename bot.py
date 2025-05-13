import time
import discord
from discord.ext import commands
import mealapi
from deep_translator import GoogleTranslator

# Instancia a API
api = mealapi.MealApi()

# Configuração do bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """
    Evento chamado quando o bot está pronto.
    """
    print(f'{bot.user} está online e pronto para uso!')

@bot.command()
async def oi(ctx: commands.Context):
    """
    Responde com uma saudação personalizada ao usuário.
    """
    nome = ctx.author.name
    await ctx.reply(f'Olá {nome}, tudo bem?')

@bot.command()
async def categorias(ctx: commands.Context):
    """
    Busca e exibe as categorias disponíveis na API.
    """
    inicio = time.perf_counter()
    await ctx.send('Buscando categorias...')
    
    categorias = api.get_categories()
    if not categorias:
        await ctx.reply('Nenhuma categoria encontrada.')
    else:
        # Traduz as categorias para português
        categorias_traduzidas = [
            GoogleTranslator(source='en', target='pt').translate(categoria)
            for categoria in categorias
        ]
        categorias_formatadas = '\n'.join(f'- {categoria}' for categoria in categorias_traduzidas)
        await ctx.send(f'Categorias encontradas:\n{categorias_formatadas}')
    
    fim = time.perf_counter()
    print(f'Tempo de execução buscar categorias: {fim - inicio:.2f} segundos')

@bot.command()
async def receita_por_categoria(ctx: commands.Context, *, categoria):
    """
    Busca receitas de uma categoria específica e as exibe.
    """
    inicio = time.perf_counter()
    
    # Traduz a entrada para inglês
    categoria_em_ingles = GoogleTranslator(source='auto', target='en').translate(categoria)
    await ctx.send(f'Buscando receitas da categoria "{categoria}"...')
    
    receitas = api.get_meal_by_category(categoria_em_ingles)
    if not receitas:
        await ctx.send('Categoria inválida. Digite !categorias para ver as categorias disponíveis.')
    else:
        # Traduz as receitas para português
        receitas_traduzidas = [
            GoogleTranslator(source='auto', target='pt').translate(receita)
            for receita in receitas
        ]
        receitas_formatadas = '\n'.join(f'- {receita}' for receita in receitas_traduzidas)
        await ctx.send(f'Receitas encontradas:\n{receitas_formatadas}')
    
    fim = time.perf_counter()
    print(f'Tempo de execução: {fim - inicio:.2f} segundos')

@bot.command()
async def receita(ctx: commands.Context, *, nome_receita):
    """
    Busca uma receita específica pelo nome, traduz os detalhes e exibe.
    """
    # Traduz a entrada para inglês
    nome_receita_em_ingles = GoogleTranslator(source='auto', target='en').translate(nome_receita)
    await ctx.send(f'Buscando receita "{nome_receita}"...')
    
    receita = api.get_recipe(nome_receita_em_ingles)
    
    if not receita:
        await ctx.send('Nenhuma receita encontrada.')
    else:
        # Traduz o título da receita
        titulo_traduzido = GoogleTranslator(source='auto', target='pt').translate(receita['title'])
        
        # Traduz os ingredientes
        ingredientes_traduzidos = [
            GoogleTranslator(source='auto', target='pt').translate(ingrediente)
            for ingrediente in receita['ingredients']
        ]
        ingredientes_formatados = '\n'.join(f'- {i}' for i in ingredientes_traduzidos)
        
        # Traduz as instruções
        instrucoes_traduzidas = GoogleTranslator(source='auto', target='pt').translate(receita['instructions'])
        
        # Envia a receita traduzida
        await ctx.send(
            f"🍽️ Receita encontrada: **{titulo_traduzido}**\n\n"
            f"📋 **Ingredientes:**\n{ingredientes_formatados}\n\n"
            f"👨‍🍳 **Modo de preparo:**\n{instrucoes_traduzidas}"
        )

@bot.event
async def on_message(message):
    """
    Evento chamado para processar mensagens recebidas.
    """
    if message.author.bot:
        return

    # Responde automaticamente a mensagens que mencionam "panqueca"
    if any(p in message.content.lower() for p in ['panqueca', 'panquecas']):
        # Simula o comando !receita para evitar duplicação de lógica
        ctx = await bot.get_context(message)
        await receita(ctx, nome_receita='Pancakes')

    # Permite que outros comandos sejam processados
    await bot.process_commands(message)

# Inicia o bot
bot.run('SEU TOKEN AQUI')
