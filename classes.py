from common import *


def load_unit(unit_id, save_to_json=True):
    with open("units.json") as units_file:
        units_dict = json.load(units_file)
    assert units_dict[str(unit_id)] is not None, "Unit_id not found in units.json"
    unit_json = units_dict[str(unit_id)]
    unit = Unit(unit_json["spec"], unit_id=unit_id, name=unit_json["name"], surname=unit_json["surname"],
                nickname=unit_json["nickname"], status=unit_json["status"], health=unit_json["health"],
                kill_count=unit_json["kill_count"], mission_count=unit_json["mission_count"],
                inventory=unit_json["inventory"])
    if save_to_json:
        unit.save()
    return unit


def attribute_unit_id():
    with open("units.json") as f:
        units_dict = json.load(f)
    search = 0
    for i in units_dict:
        if search != int(i):
            return search
        search += 1
    return search


def load_team(name, owner):
    with open("teams.json") as teams_file:
        teams_dict = json.load(teams_file)

    team_json = teams_dict[owner.name]
    for i in range(len(team_json)):
        if name == team_json[i]["name"]:
            team = Team(name, owner, members=team_json[i]["members"])
            return team

def search_unit_in_teams(unit_id):
    pass


class Weapon:
    def __init__(self, name, slot, category, min_damage, max_damage, crit_bonus=0):
        self.name = name
        self.slot = slot
        self.category = category
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.crit_bonus = crit_bonus

    def __str__(self):
        return self.name


# Items
class Item:
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = amount
        self.category = category

    def use(self):
        print(f"Error in {self.name} use")

    def consume(self):
        self.amount += -1


class HEGrenade(Item):
    def __init__(self):
        super().__init__("Grenade", 0, 1)


class Medkit(Item):
    def __init__(self):
        super().__init__("Medkit", 1, 1)

    pass


# Weapon Category
class Category:
    def __init__(self, acc_profile):
        self.acc_profile = acc_profile


# Units Classes
class Spec:
    def __init__(self, name, base_health, allowed_weapons):
        self.name = name
        self.base_health = base_health
        self.allowed_weapons = allowed_weapons

    def __str__(self):
        return self.name


# Unit
class Unit:
    def __init__(self, spec, unit_id=-1, name="", surname="",
                 nickname="", status="Alive", health=-1, kill_count=0, mission_count=0, inventory=-1):
        self.spec = spec
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.unit_id = unit_id
        self.status = status
        self.health = health
        self.kill_count = kill_count
        self.mission_count = mission_count
        self.inventory = inventory
        if self.unit_id == -1:
            self.unit_id = attribute_unit_id()
        self.in_combat = False
        self.pos = [-1, -1]
        self.cover = "None"

        if name == "":
            self.name = random.choice(names)

        if surname == "":
            self.surname = random.choice(surnames)

        if health == -1:
            self.health = spec.base_health

        if inventory == -1:
            self.inventory = ["", ""]

    def save(self):
        with open("units.json") as units_file:
            units_dict = json.load(units_file)
        units_dict[str(self.unit_id)] = dict(name=self.name, surname=self.surname, nickname=self.nickname,
                                             spec=str(self.spec), status=self.status, health=self.health,
                                             kill_count=self.kill_count, mission_count=self.mission_count,
                                             inventory=self.inventory)
        with open("units.json", "w") as f:
            json.dump(units_dict, f, indent=4)

    def save_to_id(self, value):
        with open("units.json") as units_file:
            units_dict = json.load(units_file)
        units_dict[str(value)] = dict(name=self.name, surname=self.surname, nickname=self.nickname, spec=str(self.spec),
                                      status=self.status, health=self.health, kill_count=self.kill_count,
                                      mission_count=self.mission_count)

        with open("units.json", "w") as f:
            json.dump(units_dict, f, indent=4)

    def distance_to_target(self, target):
        if self.in_combat:
            distance = math.sqrt((self.pos[0]-target.pos[0])**2 + (self.pos[1]-target.pos[1])**2)
            return distance

    def weapon_accuracy(self, target, weapon):
        distance = self.distance_to_target(target)
        accuracy = 0
        # Accuracy Profile : 0 to 3m, 3 to 7m, 7 to 10m, 10 to 15m, 15 to 20m+

        if distance < 3:
            accuracy += weapon.category.acc_profile[0]
        elif 3 <= distance < 7:
            accuracy += weapon.category.acc_profile[1]
        elif 7 <= distance < 10:
            accuracy += weapon.category.acc_profile[2]
        elif 10 <= distance < 15:
            accuracy += weapon.category.acc_profile[3]
        elif 15 <= distance < 20:
            accuracy += weapon.category.acc_profile[4]
        elif 20 <= distance:
            accuracy += weapon.category.acc_profile[5]

        if target.cover == "Full":
            accuracy += -40
        elif target.cover == "Partial":
            accuracy += -20

        if accuracy < 0:
            return 0
        elif accuracy > 100:
            return 100
        else:
            return accuracy

    def shoot_primary(self, target):
        pass

    def move(self, sequence):
        pass


class Team:
    def __init__(self, name, owner, members=None):
        if members is None:
            members = []
        self.name = name
        self.owner = owner
        self.members = members
        self.save()

    def add_member(self, unit_id):
        if unit_id not in self.members:
            free = True
            with open("teams.json") as f:
                teams_dict = json.load(f)
            for i in teams_dict:
                for j in range(len(teams_dict[i])):
                    if unit_id in teams_dict[i][j]["members"]:
                        free = False
            if free:
                self.members.append(unit_id)

    def remove_member(self, unit_id):
        if unit_id in self.members:
            self.members.remove(unit_id)

    def save(self):
        with open("teams.json") as f:
            teams_dict = json.load(f)

        if self.owner.name not in teams_dict:
            teams_dict[self.owner.name] = [{"name": self.name, "members": self.members}]
        else:
            for k in range(len(teams_dict[self.owner.name])):
                if teams_dict[self.owner.name][k]["name"] == self.name:
                    del teams_dict[self.owner.name][k]
            for i in range(len(teams_dict[self.owner.name])):
                if self.name == teams_dict[self.owner.name][i]["name"]:
                    teams_dict[self.owner.name][i]["members"] = self.members
                else:
                    teams_dict[self.owner.name].append({"name": self.name, "members": self.members})
        with open("teams.json", "w") as f:
            json.dump(teams_dict, f, indent=4)


# Buttons
class TestButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


# Iterations creation

# Category Init :
# Accuracy Profile : 0 to 3m, 3 to 7m, 7 to 10m, 10 to 15m, 15 to 20m+
cat_rifle = Category([90, 80, 70, 60, 50, 40])
cat_shotgun = Category([100, 90, 80, 60, 40, 20])
cat_machinegun = Category([90, 70, 60, 50, 50, 50])
cat_sniper = Category([30, 30, 40, 70, 80, 70])
cat_pistol = Category([100, 90, 80, 70, 70, 60])
cat_launcher = Category([100, 100, 100, 100, 90, 90])

# Weapons Init : name, slot, category, min_damage, max_damage, crit_bonus
weapon_assault_rifle = Weapon("Assault Rifle", 0, cat_rifle, 3, 5, 0)
weapon_shotgun = Weapon("Shotgun", 0, cat_shotgun, 3, 7, 20)
weapon_machinegun = Weapon("LMG", 0, cat_machinegun, 4, 5, 0)
weapon_sniper_rifle = Weapon("Sniper Rifle", 0, cat_sniper, 3, 6, 40)
weapon_pistol = Weapon("Pistol", 1, cat_pistol, 1, 3, 0)
weapon_rocket_launcher = Weapon("Rocket Launcher", 1, cat_launcher, 6, 6, 0)

# Spec Init : name, base_health, allowed_weapons
spec_medic = Spec("Medic", 5, [cat_rifle, cat_pistol])
spec_ranger = Spec("Ranger", 5, [cat_rifle, cat_shotgun, cat_pistol])
spec_heavy = Spec("Heavy", 6, [cat_machinegun, cat_launcher])
spec_sniper = Spec("Sniper", 4, [cat_sniper, cat_pistol])
