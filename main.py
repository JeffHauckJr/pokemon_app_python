import requests
import PySimpleGUI as sg

URL = "https://pokeapi.co/api/v2/"


def overview():
    layout = [[sg.Text("Using a keyword, what are you looking for?")],
              [sg.InputText()],
              [sg.Submit()]]
    window = sg.Window("PokeInfo", layout)

    option_selected = False  # flag to track if a valid option has been selected

    while not option_selected:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return None, True  # indicate that the user wants to exit the app

        welcome = values[0].lower()
        response = requests.get(URL).json()

        keys = [key.split()[0] for key in response.keys()]

        for key in keys:
            if key in welcome:
                window.close()
                return key, False  # indicate that a valid option has been selected

        sg.popup(
            "No matching keywords, please select one of the following keywords: " + str(keys))
        category = sg.popup_get_text("Please select a category. ")
        if category is None:  # user clicked Cancel on the popup
            window.close()
            return None, True  # indicate that the user wants to exit the app
        else:
            window.close()
            return category, False  # indicate that a valid option has been selected


def choose_ability():
    layout = [[sg.Text("Choose an Ability:")],
              [sg.InputText()],
              [sg.Submit()]]
    window = sg.Window("Choose Ability", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        ability = values[0].lower()
        response = requests.get(URL + "ability").json()

        # search through the list of abilities
        for result in response["results"]:
            if result["name"] == ability:
                ability_url = result["url"]
                break
        else:
            sg.popup("Invalid ability name.")
            continue

        response = requests.get(ability_url).json()
        name = response["name"]
        effect = ""
        entry_found = False
        for entry in response["effect_entries"]:
            if entry["language"]["name"] == "en":
                effect = entry["effect"]
                entry_found = True
                break
        if not entry_found:
            effect = "No effect in English found for this ability."
        effect_changes = ""
        effect_change_found = False
        for entry in response["effect_changes"]:
            for effect_entry in entry["effect_entries"]:
                if effect_entry["language"]["name"] == "en":
                    effect_changes += effect_entry["effect"] + "\n"
                    effect_change_found = True
                    break
            if effect_change_found:
                break
        if not effect_change_found:
            effect_changes = "No effect change in English found for this ability."
        flavor_text = ""
        flavor_text_found = False
        for entry in response["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                flavor_text = entry["flavor_text"]
                flavor_text_found = True
                break
        if not flavor_text_found:
            flavor_text = "No flavor text in English found for this ability."
        pokemon_list = ""
        for entry in response["pokemon"]:
            if entry:
                pokemon_list += entry["pokemon"]["name"] + "\n"

        window.close()
        layout = [[sg.Text("Name: " + name)],
                  [sg.Text("Effect entry: " + effect)],
                  [sg.Text("Effect changes:\n" + effect_changes)],
                  [sg.Text("Flavor text:\n" + flavor_text)],
                  [sg.Text("Pokemon who can have the ability:")],
                  [sg.Text(pokemon_list)],
                  [sg.Button("OK")]]
        window = sg.Window(name, layout, finalize=True)
        window.TKroot.focus_force()
        event, values = window.read()
        window.close()


def choose_item():
    layout = [[sg.Text("Choose an Item")],
              [sg.InputText()],
              [sg.Submit()]]
    window = sg.Window("Choose Item", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        item = values[0].lower().replace(" ", "-")
        response = requests.get(URL + "item").json()

        for result in response["results"]:
            if result["name"] == item:
                item_url = result["url"]
                break
        else:
            sg.popup("Invalid Item name.")
            continue

        response = requests.get(item_url).json()

        attributes = [result["name"] for result in response["attributes"]]
        attributes_str = ", ".join(attributes)

        category_name = response["category"]["name"]

        for entry in response["effect_entries"]:
            if entry["language"]["name"] == "en":
                effect = entry["effect"]
                short_effect = entry["short_effect"]
                break

        for entry in response["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                flavor_text = entry["text"]
                break

        cost = response["cost"]
        window.close()
        name = response["name"]
        layout = [[sg.Text("Name: " + name.replace(" ", "-").capitalize())],
                  [sg.Text("Cost: " + str(cost))],
                  [sg.Text("Description: \n" + flavor_text)],
                  [sg.Text("Attributes: " + "".join(attributes_str))],
                  [sg.Text("Category: " +
                           category_name.replace(" ", "-").capitalize())],
                  [sg.Text("Effect Entry: \n" + effect)],
                  [sg.Text("Short Effect: \n" + short_effect)],
                  [sg.Button("OK")]]
        window = sg.Window(name, layout, finalize=True)
        window.TKroot.focus_force()
        event, values = window.read()
        window.close()


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
        category, exit_app = overview()
        if exit_app:
            break

        if category == "ability":
            choose_ability()
        elif category == "item":
            choose_item()
        elif category == "pokemon":
            choose_pokemon()
        elif category == "berry":
            choose_berry()

    sg.popup("Goodbye!")


if __name__ == "__main__":
    main()
