import discord
from discord.ext import commands
from discord.utils import get
from discord import member
import os
import key
import bot_commands
import gsheet
from discord_slash import SlashCommand, SlashContext
# coding: utf-8

intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents, help_command=None)
slash = SlashCommand(client)
