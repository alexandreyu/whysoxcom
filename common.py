import os
import json
from datetime import datetime
import random
import mysql.connector
import discord
from dotenv import load_dotenv


load_dotenv()

db = mysql.connector.connect(host="localhost",
                             )
bot = discord.Bot(intents=discord.Intents.all())

testing_servers = [1243269063631962172]

# Variables
names = ["John", "James"]
surnames = ["Dexter", "Smith"]
game_status = 0
team_one = []
team_two = []
weapons = []
units = []
