import json


f = open('input/wiping_on_sapp.json',)

data = json.load(f)
raiders = {}
boss_encounters = {}
# {"class": str,"encounter1_buffs":[int],"encounter2_buffs": [int] .... }


pull = True

for snaps in data['snap']:
    if " on " in snaps['r']:
        for records in snaps['p']:
            boss_name = snaps["r"].split(" ")[-1]

            if boss_name not in boss_encounters:
                boss_encounters[boss_name] = 0

            if records["n"] in raiders:
                raider = raiders[records["n"]]
            else:
                raider = {}
                if records["n"] == "Dryadalis" or records["n"] == "Kittypaws":
                    raider["class"] = "Warrior"
                elif records["n"] == "Stepje":
                    raider["class"] = "Warlock"
                elif records["n"] == "Cooftvå":
                    raider["class"] = "Boomkin"
                else:
                    raider["class"] = records["c"]

            boss_name_encounter = boss_name + str(boss_encounters[boss_name])
            
            if pull:
                buffs = records["b"]
            else:
                buffs = raider[boss_name_encounter] + records["b"]

            raider[boss_name_encounter] = list(set(buffs))

            raiders[records["n"]] = raider

        if not pull:
            boss_encounters[boss_name] += 1
        pull = not pull

f.close()


buff = {
    "Greater Arcane Elixir": 17539,
    "Mageblood Potion": 24363,
    "Elixir of Greater Firepower": 26276,
    "Nightfin Soup": 18194,
    "Runn Tum Tuber Surprise": 22730,
    "Elixir of Shadow Power": 11474,
    "Elixir of the Mongoose": 17538,
    "Elixir of Giants": 11405,
    "Elixir of Superior Defense": 11348,
    "Juju Power": 16323,
    "Juju Chill": 16325,
    "Juju Might": 16329,
    "Smoked Desert Dumplings": 24799,
    "Grilled Squid": 18192,
    "Spirit of Zanza": 24382,
    "Swiftness of Zanza": 24383,
    "Winterfall Firewater": 17038,
    "Scorpok": 10669,
    "ROIDS": 10667,
    "Dirge": 25661,
    "Flask of Dislled Wisdom": 17627,
    "Flask of the Titans": 17626,
    "Flask of Supreme Power": 17628,
}

requirements = {
    "Mage": [[buff["Mageblood Potion"]], [buff["Greater Arcane Elixir"]], [buff["Elixir of Greater Firepower"]],  [buff["Nightfin Soup"], buff["Runn Tum Tuber Surprise"]]],
    "Warlock": [[buff["Greater Arcane Elixir"]], [buff["Elixir of Shadow Power"]],  [buff["Nightfin Soup"], buff["Runn Tum Tuber Surprise"]]],
    "Boomkin": [[buff["Mageblood Potion"]], [buff["Greater Arcane Elixir"]],  [buff["Nightfin Soup"], buff["Runn Tum Tuber Surprise"]]],
    "Priest": [[buff["Mageblood Potion"]], [buff["Nightfin Soup"], buff["Runn Tum Tuber Surprise"]]],
    "Paladin": [[buff["Mageblood Potion"]], [buff["Nightfin Soup"], buff["Runn Tum Tuber Surprise"]]],
    "Druid": [[buff["Mageblood Potion"]], [buff["Nightfin Soup"], buff["Runn Tum Tuber Surprise"]]],
    "Hunter": [[buff["Elixir of the Mongoose"]], [buff["Juju Might"]], [buff["Grilled Squid"], buff["Nightfin Soup"]]],
    "Warrior": [[buff["Elixir of the Mongoose"]], [buff["Elixir of Giants"], buff["Juju Power"]], [buff["Elixir of Superior Defense"], buff["Winterfall Firewater"], buff["Juju Might"]], [buff["Dirge"], buff["Smoked Desert Dumplings"]]],
    "Rogue": [[buff["Elixir of the Mongoose"]], [buff["Elixir of Giants"], buff["Juju Power"]], [buff["Winterfall Firewater"], buff["Juju Might"]], [buff["Grilled Squid"], buff["Smoked Desert Dumplings"]]]
}

results = {}
for raider, encounters in raiders.items():
    raider_class = encounters["class"]
    rec_food = requirements[raider_class][-1]
    zanza_buff = False
    flasked = False
    chilled = False

    raider_result = {
        "missing food": 0,
        "missed buffs": 0,
        "total required buffs": 0,
        "number of encounters": 0,
        "zanza": 0,
        "flasked": 0,
        "chilled": 0
    }

    for encounter, buffs in encounters.items():
        required_buffs = requirements[raider_class][:-1]
        number_of_buffs = len(required_buffs)
        found_buffs = 0
        food_buff = 1
        if encounter == "class":
            continue
        for buff in buffs:
            if buff in rec_food:
                food_buff = 0
            for required_buff in required_buffs:
                if buff in required_buff:
                    found_buffs += 1
            if buff in [24382, 24383]:
                zanza_buff = True
            if buff in [17626, 17627, 17628]:
                flasked = True
            if buff in [16325]:
                chilled = True

        raider_result["missing food"] += food_buff
        raider_result["missed buffs"] += (number_of_buffs - found_buffs)
        raider_result["total required buffs"] += number_of_buffs
        raider_result["number of encounters"] += 1
        raider_result["zanza"] = 1 if zanza_buff else raider_result["zanza"]
        raider_result["flasked"] = 1 if flasked else raider_result["flasked"]
        raider_result["chilled"] = 1 if chilled else raider_result["chilled"]

    results[raider] = raider_result

print(results)

for raider, result in results.items():
    deduction = 0
    noe = result["number of encounters"]

    if result["zanza"] == 0:
        deduction -= 0.5

    if result["chilled"] == 0:
        deduction -= 0.5

    missing_food_percent = result["missing food"]/noe
    if missing_food_percent > 0.3 + 0.2*result["flasked"]:
        deduction -= 0.1 * noe * missing_food_percent

    missing_buff_percent = result["missed buffs"] / \
        result["total required buffs"]
    if missing_buff_percent > 0.2 + 0.1*result["flasked"]:
        deduction -= 0.3 * noe * missing_buff_percent


    deduction = round(deduction, 2)
    print(raider, deduction)