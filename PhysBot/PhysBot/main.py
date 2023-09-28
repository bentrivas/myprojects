import json
import os
import subprocess
import asyncio
import random

import discord
from discord import app_commands
from discord.errors import HTTPException
from discord.ext import commands
from keep_alive import keep_alive

#USED TO KEEP BOT ALIVE 24/7
keep_alive()

file_path = "students.txt"

# DICTIONARY THAT CONTAINS ALL STUDENT INFORMATION
student_data = {}

with open(file_path, "r") as file:
  for line in file:

    fields = line.strip().split(",")

    student_data[fields[0]] = f"{fields[1]} {fields[2]}"

for key, value in student_data.items():
  print(f"Student ID: {key}, Full Name: {value}")

intents = discord.Intents.all()
intents.typing = False
client = discord.Client(intents=intents)

# SETS BOT COMMAND PREFIX TO "!"
bot = commands.Bot(command_prefix='!', intents=intents)


#INITIALIZER
@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)


#START CHECKS IF COMMAND IS IN APPROVAL LOG CHANNEL


def in_approval_log():

  async def predicate(ctx):
    allowed_channel_id = os.environ['APPROVAL_LOG_ID']
    print(
        f"allowed channel id: {allowed_channel_id}, current id: {ctx.channel.id}."
    )
    if str(ctx.channel.id) != str(allowed_channel_id):
      await ctx.message.delete()
    return str(ctx.channel.id) == (allowed_channel_id)

  return commands.check(predicate)


#END CHECKS IF COMMAND IS IN APPROVAL LOG CHANNEL

#START CHECKS IF PERSON IS BEN


def is_ben():

  def predicate(ben):
    allowed_user_id = os.environ['BEN_USER_ID']
    return str(ben.author.id) == str(allowed_user_id)

  return commands.check(predicate)


#END CHECKS IF PERSON IS BEN

#START VERIFIER


@bot.command()
@in_approval_log()
async def verify(stu, student_id):
  student = stu.author
  upper_student_id = student_id.upper()
  key_exists = upper_student_id in student_data
  await stu.message.delete()
  if key_exists:
    role = discord.utils.get(stu.guild.roles, name="Student")
    if role:
      nickname = student_data.get(upper_student_id)
      await student.add_roles(role)
      await student.edit(nick=nickname)
      print(f"Student {nickname} with ID {upper_student_id} has been verified")
    else:
      print(f"ID: {upper_student_id} failed")
      await stu.channel.send(
          f"{student.mention} your verification failed, please try again or send your name and student ID in this chat and we will manually verify you shortly"
      )

  else:
    print(f"ID: {upper_student_id} failed")
    await stu.channel.send(
        f"{student.mention} your verification failed, please try again or send your name and student ID in this chat and we will manually verify you shortly"
    )


#END VERIFIER

#START CHANNEL CLEARER


@bot.command()
@is_ben()
async def clear(toclear):
  channel = toclear.channel
  async for message in channel.history(limit=None):
    await message.delete()


#END CHANNEL CLEARER


#START GRADE GENERATOR
@bot.tree.command(name="grade")
async def grade(interaction: discord.Interaction):
  await interaction.response.send_message(
      f"{interaction.user.mention}'s grade is a {random.randrange(100)} i think"
  )


#END GRADE GENERATOR


#START GREEK LETTER GENERATOR
@bot.tree.command(name="greek")
async def greek(interaction: discord.Interaction):
  await interaction.response.send_message(
      f"i summon greek... \n {os.environ['UPPERCASE_GREEK']} \n {os.environ['LOWERCASE_GREEK']}"
  )


#END GREEK LETTER GENERATOR


#START EQUATION SHEET SENDER
@bot.tree.command(name="eqsheet")
async def eqsheet(interaction: discord.Interaction):
  await interaction.response.send_message(
      f"here you go.  {os.environ['EQSHEET']}")


#END EQUATION SHEET SENDER

#START RESTART BOT
while True:
  try:
    bot.run(os.environ['BOT_KEY'])
  except HTTPException:
    subprocess.run(['kill', '1'])
