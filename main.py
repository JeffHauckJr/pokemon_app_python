import requests

URL = "https://pokeapi.co/api/v2/"


def overview():
    welcome = input(
        "Welcome to the world of pokemon. Using a keyword, what are you looking for? ").lower()
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
    ability = input("Choose an Ability: ").lower().replace(" ", "-")
    response = requests.get(URL + "ability").json()

    # search through the list of abilities
    for result in response["results"]:
        if result["name"] == ability:
            ability_url = result["url"]
            break
    else:
        print("Invalid ability name.")
        choose_ability()
        return

    response = requests.get(ability_url).json()
    print("Name:", response["name"])
    for entry in response["effect_entries"]:
        if entry["language"]["name"] == "en":
            print("Entry entry: " + entry["effect"])
            break
        else:
            print("No effect in English found for this ability.")

    for entry in response["effect_changes"]:
        for effect_entry in entry["effect_entries"]:
            if effect_entry["language"]["name"] == "en":
                print(effect_entry["effect"])
                break
        else:
            print("No effect change in English found for this ability.")
    
    for entry in response["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            print(entry["flavor_text"])
            break
    print("Pokemon who can have the ability ")
    for entry in response["pokemon"]:
        if entry:
            print(entry["pokemon"]["name"])


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
    print(response.effect_changes.json())


def choose_pokemon():
    # url is pokemon based abd not number based. Can take pokemon from input
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


def choose_move():
    move = input("Choose a move: ").lower().replace(" ", "-")
    response = requests.get(URL + "move").json()

    for result in response["results"]:
        if result["name"] == move:
            move_url = result["url"]
            break
    else:
        print("Invalid move name.")
        choose_move()

    response = requests.get(move_url).json()
    print(response)


def main():
    while True:
        if input != "exit":
            category = overview()
            if category == "pokemon":
                choose_pokemon()
            elif category == "ability":
                choose_ability()
            elif category == "berry":
                choose_berry()
            elif category == "item":
                choose_item()
            elif category == "move":
                choose_move()
            else:
                print("Unknown category")
        else:
            break


if __name__ == "__main__":
    main()
