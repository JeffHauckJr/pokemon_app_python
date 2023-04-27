import requests

URL = "https://pokeapi.co/api/v2/"

def overview():
    welcome = input("Welcome to the world of pokemon. Using a keyword, what are you looking for? ").lower()
    print(welcome)
    response = requests.get(URL).json()

    keys = [key.split()[0] for key in response.keys()]

    for key in keys:
        if key in welcome:
            return key
    else:
        print("No matching keywords, please select one of the following keywords: " + str(keys))
        category = input("Please select a category. ")
        return category

def choose_ability():
    ability = input("Choose an Ability: ").lower()
    response = requests.get(URL + "ability").json()

    #search through the list of abilities 
    for result in response["results"]:
        print(result)
        if result["name"] == ability:
            ability_url = result["url"]
            break
    else:
        print("Invalid ability name.")
        choose_ability()
        return
    
    response = requests.get(ability_url).json()
    print(response)
def choose_berry():
    berry = input("Choose a Berry: ").lower()
    response = requests.get(URL + "berry").json()

    # Search through the list of berries for the one the user chose
    for result in response["results"]:
        print(result)
        if result["name"] == berry:
            berry_url = result["url"]
            break
    else:
        print("Invalid berry name.")
        choose_berry()
        return

    response = requests.get(berry_url).json()
    print(response)

def choose_pokemon():
    #url is pokemon based abd not number based. Can take pokemon from input
    pokemon = input("Choose a pokemon: ").lower()
    new_pokemon_url = URL + "pokemon/" + pokemon
    response = requests.get(new_pokemon_url).json()
    print(response)

def choose_item():
    item = input("Choose an Item: ").lower().replace(" ", "-")
    response = requests.get(URL + "item").json()

    for result in response["results"]:
        if result["name"] == item:
            item_url = result["url"]
            break
    else:
        print("Invalid Item name.")
        choose_item()
        
    response = requests.get(item_url).json()
    print(response)

def main():
    category = overview()
    if category == "pokemon":
        choose_pokemon()
    elif category == "ability":
        choose_ability()
    elif category == "berry":
        choose_berry()
    elif category == "item":
        choose_item()
    else:
        print("Unknown category")

if __name__ == "__main__":
    main()