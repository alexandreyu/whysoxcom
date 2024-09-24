from pydoc import describe
from textwrap import indent

from classes import *


@bot.slash_command(guild_ids=testing_servers, description="Ping")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.command(description="Show map.")
async def show_map(ctx):
    await ctx.respond("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
                      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛")


@bot.command(description="Init")
async def init_test(ctx, nom):
    team_1 = load_team(nom, ctx.author)
    await ctx.respond(ctx.author.name)
    team_1.add_member(0)
    team_1.save()


@bot.command(description="Créer une équipe")
async def creer_equipe(ctx, nom=-1):
    if nom == -1:
        nom = f"Team de {ctx.author.name}"

    with open("teams.json") as f:
        data = json.load(f)

    exists = False
    for i in data:
        if i == ctx.author.name:
            for j in range(len(data[i])):
                print(data[i])
                if data[i][j]["name"] == nom:
                    await ctx.respond("Cette équipe existe déjà !")
                    exists = True
    if not exists:
        team = Team(name=nom, owner=ctx.author)
        await ctx.respond(f"Nom de l'équipe : {team.name}, propriétaire : {team.owner.name}.")


@bot.command(description="Recruter un soldat dans une de vos équipes")
async def recruter_soldat(ctx, equipe=-1):
    with open("teams.json") as f:
        data = json.load(f)
    owns_a_team = False
    team = None
    proceed = True
    for i in data:
        if i == ctx.author.name:
            owns_a_team = True
    if owns_a_team:
        if equipe == -1:
            await ctx.respond("Veuillez choisir une équipe dans laquelle recruter ce soldat.")
            proceed = False
        else:
            team = load_team(equipe, ctx.author)
    else:
        if equipe == -1:
            equipe = "Equipe 1"
        team = Team(name=equipe, owner=ctx.author)
    if proceed:
        unit = Unit(spec_medic)
        unit.save()
        team.add_member(unit.unit_id)
        team.save()
        await ctx.respond(f"Vous avez recruté le soldat numéro {unit.unit_id}, {unit.name} {unit.surname}, {unit.spec} dans l'équipe {team.name}.")


@bot.command(description="Infos d'une équipe")
async def info_equipe(ctx, nom, nom_proprietaire=-1):
    with open("teams.json") as f:
        teams_data = json.load(f)

    if nom_proprietaire == -1:
        nom_proprietaire = ctx.author.name

    units = [None]*max_team_size
    info = ""
    team_empty = True
    for i in teams_data:
        if i == nom_proprietaire:
            for j in range(len(teams_data[i])):
                if teams_data[i][j]["name"] == nom:
                    if len(teams_data[i][j]["members"]) > 0:
                        team_empty = False
                    for k in range(len(teams_data[i][j]["members"])):

                        units[k] = teams_data[i][j]["members"][k]

                    info = f"Cette équipe contient {len(teams_data[i][j]['members'])} soldat(s) :\n"
    if team_empty:
        await ctx.respond("Cette équipe est vide !")
    else:
        for i in range(len(units)):

            if units[i] is not None:
                unit = load_unit(str(units[i]), save_to_json=False)
                nickname = " "
                if unit.nickname != "":
                    nickname += f"'{unit.nickname}' "
                info += f"\n{unit.name}{nickname}{unit.surname}, identifiant '{unit.unit_id}'"
        await ctx.respond(info)


@bot.command(description="Attention ! Cette commande détruira définitivement ce soldat")
async def retraite_soldat(ctx, id_soldat):
    with open("teams.json") as f:
        teams_data = json.load(f)

    with open("units.json") as f:
        units_data = json.load(f)

    unit = load_unit(str(id_soldat), save_to_json=False)

    for i in teams_data:
        if i == ctx.author.name:
            for j in range(len(teams_data[i])):
                for k in range(len(teams_data[i][j]["members"])):
                    if str(teams_data[i][j]["members"][k]) == str(id_soldat):
                        del teams_data[i][j]["members"][k]
    nickname = " "
    if unit.nickname != "":
        nickname += f"'{unit.nickname}' "

    del units_data[str(id_soldat)]
    with open("teams.json", "w") as f:
        json.dump(teams_data, f, indent=4)

    with open("units.json", "w") as f:
        json.dump(units_data, f, indent=4)

    await ctx.respond(f"Le soldat {unit.name}{nickname}{unit.surname} a été mis à la retraite."
                      f" Merci pour votre service.")



@bot.command(description="Changer les armes d'un soldat")
async def equiper_soldat(ctx, id_soldat):
    pass

"""embed = discord.Embed(title="Inscription",
                          description="Démarrage de la partie, les joueurs on",
                          color=0xFF5733)"""
"""sol_1 = Unit(spec_medic)
    print(sol_1.spec)
    await ctx.respond(f"Unit's id is {sol_1.unit_id}, name is {sol_1.name}, surname is {sol_1.surname}, "
                      f"nickname is {sol_1.nickname}, specialization is {sol_1.spec}, status is {sol_1.status}, "
                      f"kill count is {sol_1.kill_count}, mission count is {sol_1.mission_count}.")
    save_unit(sol_1)
    # print(str(spec_medic))"""

"""@bot.command(description="Inspect unit")
async def inspect_unit(ctx, unit_id):
    await ctx.respond(f"Unit number {sol_1.unit_id}'s name is {sol_1.name}, surname is {sol_1.surname}, health is {sol_1.health}, status is {sol_1.status}, team is {sol_1.team}.")"""
