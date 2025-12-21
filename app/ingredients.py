# Christine Chen, Naomi Kurian, Ethan Cheung, Owen Zeng
# WheelOfFortune
# SoftDev
# P01 – ArRESTed Development
# 2025-12-02


# get ingredient -> get meal -> get stuff using ID
# https://www.themealdb.com/api/json/v1/1/filter.php?i=chicken_breast
# https://www.themealdb.com/api/json/v1/1/lookup.php?i=52850

import requests
import random
import json


def random_ingredient():
    print(
        "<------------------------------RANDOM INGREDIENT------------------------------>"
    )
    try:
        # get rand ingredient
        ingredient_basepath = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
        print("this is ingredient basepath: " + ingredient_basepath)
        ingredient_response = requests.get(ingredient_basepath)
        ing_data = ingredient_response.json()
        ingredients = ing_data["meals"]
        print(len(ingredients))
        rand_num_ing = random.randint(0, len(ingredients))
        print(rand_num_ing)
        rand_ing = ingredients[rand_num_ing]
        str_ingredient = rand_ing["strIngredient"]
        print(str_ingredient)

        # get meals with rand int
        filtered_ing = str_ingredient.replace(" ", "_")
        filtered_ing = filtered_ing.lower()

        print("huh")
        return filtered_ing
    except:
        return "unwaxed_lemon"


def random_meal(filtered_ing):
    print("<------------------------------RANDOM MEAL------------------------------>")
    f_ing = filtered_ing
    try:
        meal_basepath = f"http://www.themealdb.com/api/json/v1/1/filter.php?i={f_ing}"
        print(meal_basepath)
        meal_response = requests.get(meal_basepath)
        meal_data = meal_response.json()
        meals = meal_data["meals"]
        try:
            print(len(meals))
            print(random.randint(0, len(meals)))
            rand_num_meal = random.randint(0, len(meals))
            rand_meal = meals[rand_num_meal]
        except:
            try:
                rand_meal = meals[0]
            except:
                rand_meal = {"idMeal": 0}
        rand_meal_id = rand_meal["idMeal"]
        return rand_meal_id
    except:
        return 0


def meal_ingredients(rand_meal_id):
    print(
        "<------------------------------MEAL INGREDIENTS------------------------------>"
    )
    id = rand_meal_id
    meal_basepath = f"http://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
    print(meal_basepath)
    meal_response = requests.get(meal_basepath)
    meal_data = meal_response.json()
    meals = meal_data["meals"]

    ingredients = []

    for k in meals[0]:
        if "strIngredient" in k:
            ingredients.append(meals[0][k])
    print(ingredients)

    sanitized_ingredients = filter(None, ingredients)
    sanitized_ingredients = list(sanitized_ingredients)
    end = sanitized_ingredients
    return end


def meal_img(rand_meal_id):
    print("<------------------------------MEAL IMAGE------------------------------>")
    id = rand_meal_id
    print("id " + str(id))
    meal_basepath = f"http://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
    print(meal_basepath)
    meal_response = requests.get(meal_basepath)
    print(meal_response)
    meal_data = meal_response.json()
    # print(meal_data)
    meals = meal_data["meals"][0]
    print(meals)
    image = meals["strMealThumb"]
    print(image)

    return image


