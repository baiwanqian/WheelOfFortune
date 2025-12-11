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
        ingredient_basepath = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
        print("this is ingredient basepath: " + ingredient_basepath)
        response = requests.get(ingredient_basepath)
        data = response.json()

        ingredients = data["meals"]
        rand_ing = randint(0,len(ingredients))
        print(ingredients)
        print(rand_ing)
    except:
        print("oops")

random_ingredient()
