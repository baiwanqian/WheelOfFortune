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
    return (meal_data)
