import requests
import PySimpleGUI as sg

URL = "https://pokeapi.co/api/v2/"


def overview():
    layout = [[sg.Text("Using a keyword, what are you looking for?")],
              [sg.InputText()],
              [sg.Submit()]]
    window = sg.Window("PokeInfo", icon='./images/icon.ico').Layout(layout)

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
            
        list = ["Ability", "Berry", "Item", "Moves", "Pokemon"]

        sg.popup(
            "No matching keywords, please select one of the following keywords: " + ", ".join(list), icon="./images/icon.ico")
        category = sg.popup_get_text("Please select a category. ", icon="./images/icon.ico")
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
    window = sg.Window(
        "Choose Ability", icon='./images/icon.ico').Layout(layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        ability = values[0].lower()
        ability_url = None
        next_url = URL + "ability"
        while next_url is not None:
            response = requests.get(next_url).json()
            for result in response["results"]:
                if result["name"] == ability:
                    ability_url = result["url"]
                    break
            else:
                next_url = response["next"]
                continue
            break
        else:
            sg.popup("Invalid ability name.", icon="./images/icon.ico")
            continue

        # search through the list of abilities
        for result in response["results"]:
            if result["name"] == ability:
                ability_url = result["url"]
                break
        else:
            sg.popup("Invalid ability name.", icon="./images/icon.ico")
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
                pokemon_list += entry["pokemon"]["name"].capitalize() + "\n"

        window.close()
        layout = [[sg.Text("Name: " + name)],
                  [sg.Text("Effect entry: ")],
                  [sg.Multiline(effect, size=(80, 10),
                                disabled=True, autoscroll=True)],
                  [sg.Text("Effect changes:\n" + effect_changes)],
                  [sg.Text("Flavor text:\n" + flavor_text)],
                  [sg.Text("Pokemon who can have the ability:")],
                  [sg.Multiline(pokemon_list, key='-POKELIST-',
                                size=(50, 20), enable_events=True, disabled=True)],
                  [sg.Button("OK")]]
        window = sg.Window(name, layout, icon="./images/icon.ico", finalize=True)
        window.TKroot.focus_force()
        while True:
            event, values = window.read()
            if event == "OK" or event == sg.WINDOW_CLOSED:
                break

        window.close()


def choose_item():
    layout = [[sg.Text("Choose an Item")],
              [sg.InputText()],
              [sg.Submit()]]
    window = sg.Window("Choose Item", icon='./images/icon.ico').Layout(layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        item = values[0].lower().replace(" ", "-")
        item_url = None
        next_url = URL + "item"
        while next_url is not None:
            response = requests.get(next_url).json()
            for result in response["results"]:
                if result["name"] == item:
                    item_url = result["url"]
                    break
            else:
                next_url = response["next"]
                continue
            break
        else:
            sg.popup("Invalid Item name.", icon="./images/icon.ico")
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
        image = response["sprites"]["default"]
        name = response["name"]  # move this line up

        window.close()

        layout = [[sg.Text("Name: " + name.replace(" ", "-").capitalize())],
                  # use requests.get().content here
                  [sg.Image(requests.get(image).content)],
                  [sg.Text("Cost: " + str(cost))],
                  [sg.Text("Description: " + flavor_text.replace("\n", " "))],
                  [sg.Text("Attributes: " + "".join(attributes_str))],
                  [sg.Text("Category: " +
                           category_name.replace(" ", "-").capitalize())],
                  [sg.Text("Effect Entry: \n" + effect)],
                  [sg.Text("Short Effect: \n" + short_effect)],
                  [sg.Button("OK")]]
        window = sg.Window(name, layout, finalize=True,
                           icon='./images/icon.ico')
        window.finalize()
        window.maximize()
        window.TKroot.focus_force()
        event, values = window.read()
        window.close()


def choose_berry():
    layout = [[sg.Text("Choose a Berry")],
              [sg.InputText()],
              [sg.Submit()]]
    window = sg.Window("Choose Berry", icon='./images/icon.ico').Layout(layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        berry = values[0].lower().replace(" ", "-")
        next_url = URL + "berry"
        berry_url = None
        # Search through the list of berries for the one the user chose
        while next_url is not None:
            response = requests.get(next_url).json()
            for result in response["results"]:
                if result["name"] == berry:
                    berry_url = result["url"]
                    break
            else:
                next_url = response["next"]
                continue
            break
        else:
            sg.popup("Invalid berry name.", icon="./images/icon.ico")
            continue

        response = requests.get(berry_url).json()

        name = response["name"].capitalize()
        firmness = response["firmness"]["name"].capitalize()
        growth_time = str(response["growth_time"])
        max_harvest = str(response["max_harvest"])
        natural_gift_power = str(response["natural_gift_power"])
        natural_gift_type = response["natural_gift_type"]["name"].capitalize()
        flavor_with_potency = []
        for result in response["flavors"]:
            if result["potency"] > 0:
                flavor = result["flavor"]["name"].capitalize()
                potency = result["potency"]
                flavor_with_potency.append(f"{flavor} (potency: {potency})")

        window.close()

        layout = [[sg.Text("Name: " + name)],
                  [sg.Text("Firmness: " + firmness)],
                  [sg.Text("Flavor: " + ",".join(flavor_with_potency))],
                  [sg.Text("Growth time: " + growth_time)],
                  [sg.Text("Max Harvest: " + max_harvest)],
                  [sg.Text("Natural Gift Type: " + natural_gift_type)],
                  [sg.Text("Natural Gift Power: " + natural_gift_power)],
                  ]
        window = sg.Window(
            name, layout, icon='./images/icon.ico', finalize=True)


def choose_pokemon():
    layout = [[sg.Text("Choose a Pokemon")],
              [sg.InputText()],
              [sg.Submit()]]
    window = sg.Window(
        "Choose Pokemon", icon='./images/icon.ico').Layout(layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        pokemon = values[0].lower().replace(" ", "-")

    # url is pokemon based abd not number based. Can take pokemon from input
    # name(done)
    # abilities(ability name url) take url and grab description from url
    # exp exp
    # held items [done]
    # moves []
    # sprite [done]
    # number [done]
    # type [done]
    # stats [done]
        # name
        new_pokemon_url = URL + "pokemon/" + pokemon + "/"
        response = requests.get(new_pokemon_url)
        if response.status_code == 404:
            sg.popup("Invalid Pokemon name. Please try again.", icon="./images/icon.ico")
            break
        response = requests.get(new_pokemon_url).json()
        # sprite
        img = response["sprites"]["front_default"]
        # number
        number = str(response["id"])
        # held items
        held_items = []
        for i in response["held_items"]:
            held_items.append(i["item"]["name"])
        if len(held_items) == 0:
            held_item_str = None
        else: 
            held_item_str = ", ".join(held_items)
        # type
        terp = []
        for result in response["types"]:
            terp.append(result["type"]["name"])
        # stats
        base_stats = []
        for stats in response["stats"]:
            stat = str(stats["base_stat"])
            if isinstance(stats["stat"], dict):
                stat_name = stats["stat"].get("name")
                if stat_name is not None:
                    base_stats.append(f"{stat_name}: {stat}\n")
        # moves
 
        # moves
        moves = {}
        for i in response["moves"]:
            move_name = i["move"]["name"]
            move_data = []
            for j in i["version_group_details"]:
                lvl_available = j["level_learned_at"]
                method = j["move_learn_method"]["name"]
                game_version = j["version_group"]["name"]
                move_data.append((lvl_available, method, game_version))
            moves[move_name] = move_data

        # format moves for display
        moves_text = ""
        for move, data in moves.items():
            moves_text += f"{move.capitalize()}:\n"
            for level, method, game_version in data:
                moves_text += f"    Level: {level}\n    Method: {method}\n    Version: {game_version}\n"
            moves_text += "\n"

        exp = response["base_experience"]
        name = response["name"].capitalize()

        species_url = response["species"]["url"]
        species_result = requests.get(species_url).json()

        #details 
        for i in species_result["flavor_text_entries"]:
            if i["language"]["name"] == "en":
                details = i["flavor_text"]
        #egg details
        egg_group = []        
        for i in species_result["egg_groups"]:
            egg_group.append(i["name"])
            print(len(i))
        egg_group_str = ", ".join(egg_group).title()

        #evolution chain
        evolution_chain_url = species_result["evolution_chain"]["url"]
        evolution_response = requests.get(evolution_chain_url).json()

        # get evolution chain
        evolution_chain = evolution_response["chain"]


        # add evolutions layout to main layout

        layout = [
            [sg.Text(name + " " + "\nPokeNum: " + number)],
            [sg.Image(requests.get(img).content)],
            [sg.Text("Types: " + ", ".join(terp).title())],
            [sg.Text("Details: " + details)],
            [sg.Text("Egg Group: " + egg_group_str)],
            [sg.Text("Base Experience: " + str(exp))],
            [sg.Text("Base Stats: \n" + "\n".join(base_stats).title())],
            [sg.Text("Held Items: " + (held_item_str or "None"))],
            [sg.Multiline("Moves: \n\n" + moves_text, size=(40, 20))]
        ]
        window = sg.Window(name, layout, icon='./images/icon.ico', finalize=True)
    window.close()

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

    sg.popup("Goodbye!",icon='./images/icon.ico' )


if __name__ == "__main__":
    main()
