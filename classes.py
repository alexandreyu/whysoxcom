from common import *


def load_unit(unit_id):
    with open("units.json") as units_file:
        units_dict = json.load(units_file)
    assert units_dict[str(unit_id)] is not None, "Unit_id not found in units.json"
    unit_json = units_dict[str(unit_id)]
    unit = Unit(unit_json["spec"], unit_id=unit_id, name=unit_json["name"], surname=unit_json["surname"],
                nickname=unit_json["nickname"], status=unit_json["status"], health=unit_json["health"],
                kill_count=unit_json["kill_count"], mission_count=unit_json["mission_count"])

    return unit


def save_unit(unit):
    with open("units.json") as units_file:
        units_dict = json.load(units_file)
    units_dict[str(unit.unit_id)] = dict(name=unit.name, surname=unit.surname, nickname=unit.nickname,
                                         spec=str(unit.spec), status=unit.status, health=unit.health,
                                         kill_count=unit.kill_count, mission_count=unit.mission_count)
    with open("units.json", "w") as f:
        json.dump(units_dict, f, indent=4)


def save_unit_to_id(unit, value):
    with open("units.json") as units_file:
        units_dict = json.load(units_file)
    units_dict[str(value)] = dict(name=unit.name, surname=unit.surname, nickname=unit.nickname, spec=str(unit.spec),
                                  status=unit.status, health=unit.health, kill_count=unit.kill_count,
                                  mission_count=unit.mission_count)

    with open("units.json", "w") as f:
        json.dump(units_dict, f, indent=4)


def attribute_unit_id():
    with open("units.json") as f:
        units_dict = json.load(f)
    search = 0
    for i in units_dict:
        if search != int(i):
            return search
        search += 1
    return search


class Weapon:
    def __init__(self, name, slot, category, min_damage, max_damage, crit_bonus=0):
        self.name = name
        self.slot = slot
        self.category = category
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.crit_bonus = crit_bonus


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
                 nickname="", status="Alive", health=-1, kill_count=0, mission_count=0):
        self.spec = spec
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.unit_id = unit_id
        self.kill_count = kill_count
        self.mission_count = mission_count
        self.status = status
        self.health = health
        self.unit_id = attribute_unit_id()

        if name == "":
            self.name = random.choice(names)

        if surname == "":
            self.surname = random.choice(surnames)

        if health == -1:
            self.health = spec.base_health


    def save(self):
        save_unit(self)

    def shoot_primary(self, target):
        pass

    def move(self, sequence):
        pass


class Team:
    # A REFAIRE TOUT
    # pour permettre des soldats blessés et not on duty
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.members = [None] * max_team_size

    def check_if_complete(self):
        for i in self.members:
            if i is not Unit:
                return False
        return True

    def save(self):
        if self.check_if_complete():
            team_dict = {

                "owner": str(self.owner.username),
                "name": str(self.name),
                "members": {"unit0": int(self.members[0].unit_id),
                            "unit1": int(self.members[1].unit_id),
                            "unit2": int(self.members[2].unit_id),
                            "unit3": int(self.members[3].unit_id)}
            }
            file = open("teams.json", "w")
            file.write(str(team_dict))

    def add_member(self, unit):
        for i in range(len(self.members)):
            if self.members[i] is None:
                self.members[i] = unit
            # save()


# Buttons
class TestButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


# Iterations creation


# Category Init :
# Accuracy Profile : 0 to 3m, 3 to 7m, 7 to 10m, 10 to 15m, 15 to 20m+
cat_rifle = Category([90, 80, 70, 60, 50, 40])
cat_shotgun = Category([100, 90, 80, 60, 40, 20])
cat_sniper = Category([30, 30, 40, 70, 80, 70])
cat_pistol = Category([100, 90, 80, 70, 70, 60])
cat_launcher = Category([100, 100, 100, 100, 90, 90])

# Weapons Init : name, slot, category, min_damage, max_damage, crit_bonus
weapon_assault_rifle = Weapon("Assault Rifle", 0, cat_rifle, 3, 5, 0)
weapon_shotgun = Weapon("Shotgun", 0, cat_shotgun, 3, 7, 20)
weapon_sniper_rifle = Weapon("Sniper Rifle", 0, cat_sniper, 3, 6, 40)
weapon_pistol = Weapon("Pistol", 0, cat_pistol, 1, 3, 0)
weapon_rocket_launcher = Weapon("Rocket Launcher", 0, cat_launcher, 6, 6, 0)

# Spec Init : name, base_health, allowed_weapons
spec_medic = Spec("Medic", 4, [cat_rifle, cat_pistol])
spec_heavy = Spec("Heavy", 5, [cat_rifle, cat_pistol])
