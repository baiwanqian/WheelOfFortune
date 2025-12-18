#Christine Chen, Naomi Kurian, Ethan Cheung, Owen Zeng
#WheelOfFortune
#SoftDev
#P01 – ArRESTed Development
#2025-12-02


# get ingredient -> get meal -> get stuff using ID
# https://www.themealdb.com/api/json/v1/1/filter.php?i=chicken_breast
# https://www.themealdb.com/api/json/v1/1/lookup.php?i=52850

import requests
import random
import json

def random_ingredient():

    try:
        # get rand ingredient
        ingredient_basepath = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
        print("this is ingredient basepath: " + ingredient_basepath)
        ingredient_response = requests.get(ingredient_basepath)
        ing_data = ingredient_response.json()
        ingredients = ing_data["meals"]
        print(len(ingredients))
        rand_num_ing = random.randint(0,len(ingredients))
        print(rand_num_ing)
        rand_ing = ingredients[rand_num_ing]
        str_ingredient = rand_ing["strIngredient"]
        print(str_ingredient)

        # get meals with rand int
        filtered_ing = str_ingredient.replace(" ", "_")
        filtered_ing = filtered_ing.lower()


        print("huh")
        return (filtered_ing)
    except:
        print("oops")


def random_meal(filtered_ing):
    f_ing = filtered_ing
    meal_basepath = f"http://www.themealdb.com/api/json/v1/1/filter.php?i={f_ing}"
    print(meal_basepath)
    meal_response = requests.get(meal_basepath)
    meal_data = meal_response.json()
    meals = meal_data["meals"]
    try:
        print(len(meals))
        print(random.randint(0,len(meals)))
        rand_num_meal = random.randint(0,len(meals))
        rand_meal = meals[rand_num_meal]
    except:
        try:
            rand_meal = meals[0]
        except:
            rand_meal = {"idMeal": 0}
    rand_meal_id = rand_meal["idMeal"]
    return (rand_meal_id)

def meal_ingredients(rand_meal_id):
    id = rand_meal_id
    meal_basepath = f"http://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
    print(meal_basepath)
    meal_response = requests.get(meal_basepath)
    meal_data = meal_response.json()
    meals = meal_data["meals"]

    ingredients = {}
    i = 0
    while i < len(meals):
        if "strIngredient" in meals[i]:
            ingredient.append(meals[i]["strIngredient" + i])
        i = i+1

    end = ingredients
    return end

'''
def random_meal():
    meal_basepath = "www.themealdb.com/api/json/v1/1/random.php"
    meal_response = requests.get(meal_basepath)
    meal_data = meal_response.json()
    meal_data = meal_data["meals"][0]

    ingredients = {}
    i = 10
    while meal_data[i] <= 20:
        if ()
            ingredients.append(meal_data["strIngredient" + i])
'''
