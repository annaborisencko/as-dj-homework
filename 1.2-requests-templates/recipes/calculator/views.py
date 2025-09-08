from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
def calculator_view(request, dish: str=None):
    recipe = {}
    if request.GET.get('servings'):
        servings = int(request.GET.get('servings'))
    else:
        servings = 1

    if dish in DATA.keys():
        for key, value in DATA[dish].items():
            recipe[key] = value * servings
            msg = f"Рецепт блюда {dish}: "
    else:
        msg = f"Вы указали неизвестное блюдо. Укажите одно из значений: {list(DATA.keys())}"
    context = {
        'recipe' : recipe,
        'msg' : msg
    }
    return render(request, 'calculator/index.html', context)