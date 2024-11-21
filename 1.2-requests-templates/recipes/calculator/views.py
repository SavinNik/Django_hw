from django.http import HttpResponse
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
}


def recipe_view(request, recipe_name: dict):

    servings = request.GET.get('servings', 1)

    try:
        servings = int(servings)
        if servings <= 0:
            raise ValueError
    except ValueError:
        return HttpResponse('Параметр servings должен быть положительным целым числом')

    recipe = {ingredient: amount * servings for ingredient, amount in DATA[recipe_name].items()}

    context = {
        'recipe': recipe
    }

    return render(request, 'calculator/index.html', context)

