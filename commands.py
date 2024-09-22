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
async def init_test(ctx):
    team_1 = load_team(f"(Team de {ctx.author.name})", ctx.author)
    await ctx.respond(ctx.author.name)
    team_1.add_member(0)
    team_1.save()


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
