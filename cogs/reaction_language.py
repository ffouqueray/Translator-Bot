import discord
from discord import Intents
from discord.ext import commands,tasks
from discord.ext.commands import Bot, CommandNotFound, ChannelNotFound
from discord.utils import get

from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

from datetime import timezone, tzinfo, timedelta
import sqlite3
import random
import asyncio
import os
import googletrans
from googletrans import Translator

db = sqlite3.connect("translator.sqlite") # Ouverture de la base de donnรฉes
cursor = db.cursor()

trad = Translator(service_urls=['translate.googleapis.com'])

class ReactionEventSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        cursor.execute(f"SELECT reaction_activated FROM default_guild_language WHERE guild_id = {payload.guild_id}")
        reaction_allowed = cursor.fetchone()

        if str(reaction_allowed) == "None" or str(reaction_allowed) == "(None,)" or str(reaction_allowed[0]) == "enabled":
            pass
        else:
            return

        botuser = self.client.get_user(815328232537718794)

        reactionflag = ['๐ฆ๐ธ','๐ฆ๐จ','๐ฆ๐ฉ','๐ฆ๐ช','๐ฆ๐ฌ','๐ฆ๐ฎ','๐ฆ๐ฑ','๐ฆ๐ฒ','๐ฆ๐ด','๐ฆ๐ถ','๐ฆ๐ท','๐ฆ๐น','๐ฆ๐บ','๐ฆ๐ผ','๐ฆ๐ฝ','๐ฆ๐ฟ','๐ง๐ธ','๐ง๐ฆ','๐ง๐ง','๐ง๐ฉ','๐ง๐ช','๐ง๐ซ','๐ง๐ฌ','๐ง๐ญ','๐ง๐ฎ','๐ง๐ฏ','๐ง๐ฑ','๐ง๐ฒ','๐ง๐ณ','๐ง๐ด','๐ง๐ถ','๐ง๐ท','๐ง๐น','๐ง๐ป','๐ง๐ผ','๐ง๐พ','๐ง๐ฟ','๐จ๐ฆ','๐จ๐จ','๐จ๐ฉ','๐จ๐ซ','๐จ๐ฌ','๐จ๐ญ','๐จ๐ฎ','๐จ๐ฐ','๐จ๐ฑ','๐จ๐ฒ','๐จ๐ณ','๐จ๐ด','๐จ๐ต','๐จ๐ท','๐จ๐บ','๐จ๐ป','๐จ๐ผ','๐จ๐ฝ','๐จ๐พ','๐จ๐ฟ','๐ฉ๐ช','๐ฉ๐ฌ','๐ฉ๐ฏ','๐ฉ๐ฐ','๐ฉ๐ฒ','๐ฉ๐ด','๐ฉ๐ฟ','๐ช๐ฆ','๐ช๐จ','๐ช๐ช','๐ช๐ฌ','๐ช๐ญ','๐ช๐ท','๐ช๐ธ','๐ช๐น','๐ช๐บ','๐ซ๐ฎ','๐ซ๐ฏ','๐ซ๐ฐ','๐ซ๐ฒ','๐ซ๐ด','๐ซ๐ท','๐ฌ๐ฆ','๐ฌ๐ง','๐ฌ๐ฉ','๐ฌ๐ช','๐ฌ๐ซ','๐ฌ๐ฌ','๐ฌ๐ญ','๐ฌ๐ฎ','๐ฌ๐ฑ','๐ฌ๐ฒ','๐ฌ๐ณ','๐ฌ๐ต','๐ฌ๐ถ','๐ฌ๐ท','๐ฌ๐ธ','๐ฌ๐น','๐ฌ๐บ','๐ฌ๐ผ','๐ฌ๐พ','๐ญ๐ฐ','๐ญ๐ฒ','๐ญ๐ณ','๐ญ๐ท','๐ญ๐น','๐ญ๐บ','๐ฎ๐จ','๐ฎ๐ฉ','๐ฎ๐ช','๐ฎ๐ฑ','๐ฎ๐ฒ','๐ฎ๐ณ','๐ฎ๐ด','๐ฎ๐ถ','๐ฎ๐ท','๐ฎ๐ธ','๐ฎ๐น','๐ฏ๐ช','๐ฏ๐ฒ','๐ฏ๐ด','๐ฏ๐ต','๐ฐ๐ช','๐ฐ๐ฌ','๐ฐ๐ญ','๐ฐ๐ฎ','๐ฐ๐ฒ','๐ฐ๐ณ','๐ฐ๐ต','๐ฐ๐ท','๐ฐ๐ผ','๐ฐ๐พ','๐ฐ๐ฟ','๐ฑ๐ฆ','๐ฑ๐ง','๐ฑ๐จ','๐ฑ๐ฎ','๐ฑ๐ฐ','๐ฑ๐ท','๐ฑ๐ธ','๐ฑ๐น','๐ฑ๐บ','๐ฑ๐ป','๐ฑ๐พ','๐ฒ๐ฆ','๐ฒ๐จ','๐ฒ๐ฉ','๐ฒ๐ช','๐ฒ๐ซ','๐ฒ๐ฌ','๐ฒ๐ญ','๐ฒ๐ฐ','๐ฒ๐ฑ','๐ฒ๐ฒ','๐ฒ๐ณ','๐ฒ๐ด','๐ฒ๐ต','๐ฒ๐ถ','๐ฒ๐ท','๐ฒ๐ธ','๐ฒ๐น','๐ฒ๐บ','๐ฒ๐ป','๐ฒ๐ผ','๐ฒ๐ฝ','๐ฒ๐พ','๐ฒ๐ฟ','๐ณ๐ฆ','๐ณ๐จ','๐ณ๐ช','๐ณ๐ซ','๐ณ๐ฌ','๐ณ๐ฎ','๐ณ๐ฑ','๐ณ๐ด','๐ณ๐ต','๐ณ๐ท','๐ณ๐บ','๐ณ๐ฟ','๐ด๐ฒ','๐ต๐ฆ','๐ต๐ช','๐ต๐ซ','๐ต๐ฌ','๐ต๐ญ','๐ต๐ฐ','๐ต๐ฑ','๐ต๐ฒ','๐ต๐ณ','๐ต๐ท','๐ต๐ธ','๐ต๐น','๐ต๐ผ','๐ต๐พ','๐ถ๐ฆ','๐ท๐ช','๐ท๐ด','๐ท๐ธ','๐ท๐บ','๐ท๐ผ','๐ธ๐ฆ','๐ธ๐ง','๐ธ๐จ','๐ธ๐ฉ','๐ธ๐ช','๐ธ๐ฌ','๐ธ๐ญ','๐ธ๐ฎ','๐ธ๐ฏ','๐ธ๐ฐ','๐ธ๐ฑ','๐ธ๐ฒ','๐ธ๐ณ','๐ธ๐ด','๐ธ๐ท','๐ธ๐ธ','๐ธ๐น','๐ธ๐ป','๐ธ๐ฝ','๐ธ๐พ','๐ธ๐ฟ','๐น๐ฆ','๐น๐จ','๐น๐ฉ','๐น๐ซ','๐น๐ฌ','๐น๐ญ','๐น๐ฏ','๐น๐ฐ','๐น๐ฑ','๐น๐ฒ','๐น๐ณ','๐น๐ด','๐น๐ท','๐น๐น','๐น๐ป','๐น๐ผ','๐น๐ฟ','๐บ๐ฆ','๐บ๐ฌ','๐บ๐ฒ','๐บ๐ณ','๐บ๐ธ','๐บ๐พ','๐บ๐ฟ','๐ป๐ฆ','๐ป๐จ','๐ป๐ช','๐ป๐ฌ','๐ป๐ฎ','๐ป๐ณ','๐ป๐บ','๐ผ๐ซ','๐ผ๐ธ','๐ฝ๐ฐ','๐พ๐ช','๐พ๐น','๐ฟ๐ฆ','๐ฟ๐ฒ','๐ฟ๐ผ']

        destinationflag = ['sm','en','ca','ar','en','en','sq','hy','pt','en','es','de','en','nl','sv','az','en','bs','en','bn','fr','fr','bg','ar','fr','fr','fr','en','ms','es','nl','pt','ne','is','en','be','en','en','en','fr','fr','fr','de','fr','mi','es','fr','zh-cn','es','fr','es','es','pt','nl','zh-cn','el','cs','de','en','fr','da','en','es','ar','es','es','et','ar','ar','en','es','am','en','fi','hi','en','en','da','fr','fr','en','en','ka','fr','en','en','en','en','en','fr','fr','fr','el','en','es','en','pt','en','zh-cn','en','es','hr','ht','hu','es','id','ga','iw','en','hi','en','ku','fa','is','it','en','en','ar','ja','sw','ky','km','en','fr','en','ko','ko','ar','en','kk','lo','ar','en','ge','ta','en','en','lt','lb','lv','ar','ar','fr','ro','en','fr','mg','en','mk','fr','my','mn','zh-cn','en','fr','ar','en','mt','en','en','en','es','ms','pt','en','fr','fr','en','en','es','nl','no','ne','en','en','mi','ar','es','es','fr','en','tl','en','pl','fr','en','es','ar','pt','en','es','ar','fr','ro','sr','ru','en','ar','en','fr','ar','sv','ms','en','sl','nl','sk','en','it','fr','so','nl','en','pt','es','nl','ar','en','en','en','fr','fr','fr','th','tg','en','pt','en','ar','en','tr','en','en','zh-cn','sw','uk','sw','en','en','en','es','uz','it','en','es','en','en','vi','fr','fr','sm','sq','ar','fr','af','en','sn']

        if payload.emoji.name in reactionflag:

            LangueIndex = reactionflag.index(payload.emoji.name)

            source = destinationflag[LangueIndex]

            TranslateMessage = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)

            Traduction = trad.translate(text = TranslateMessage.content, dest=source)

            EmbedImpossibleSendDM = discord.Embed(description = "You must to open your DM's to allow me to send you the translate you asked for",
                                                colour = discord.Colour.red())
            EmbedImpossibleSendDM.set_author(name = payload.member,
                                            icon_url = payload.member.avatar_url)

            cursor.execute(f"SELECT yesno FROM DMUser WHERE user_id = {payload.user_id}")
            DMOnOff = cursor.fetchone()

            if Traduction.src == source:

                EmbedSameLanguage = discord.Embed(title="It's the same language",
                                                description = "I don't know why you want to translate a message to the same language as the original one.",
                                                colour = discord.Colour.red())
                EmbedSameLanguage.set_footer(icon_url = f"https://cdn.discordapp.com/avatars/341257685901246466/a_09dadd494a375adaced572682c8ec96c.png?size=4096",
                                            text = f"JeSuisUnBonWhisky#0001")
                EmbedSameLanguage.set_author(icon_url = botuser.avatar_url,
                                            name = botuser)

                try:
                    await TranslateMessage.remove_reaction(emoji = f"{payload.emoji.name}", member = payload.member)
                except discord.Forbidden:
                    pass
                
                if (str(DMOnOff) == "None") or (str(DMOnOff) == "(None,)") :
                    try:
                        await self.client.get_user(payload.user_id).send(embed = EmbedSameLanguage)
                    except discord.Forbidden:
                        await self.client.get_channel(payload.channel_id).send(embed = EmbedImpossibleSendDM)
                else :
                    await self.client.get_channel(payload.channel_id).send(embed = EmbedSameLanguage)
            
            else:
                
                EmbedTranslated = discord.Embed(title = "The translation you requested",
                                                description = f"**Original Message :**\n{TranslateMessage.content}\n\n**Translated Message :**\n{Traduction.text}",
                                                colour = discord.Colour.purple())
                EmbedTranslated.add_field(name = "**__More infos about the message :__**",
                                        value = f"Message link (to directly go to it) : [Click Here]({TranslateMessage.jump_url})\nMessage Channel : <#{TranslateMessage.channel.id}> / **#{TranslateMessage.channel.name}**\nOriginal Message Author : <@{TranslateMessage.author.id}> / **{TranslateMessage.author}**",
                                        inline = False)
                EmbedTranslated.set_footer(icon_url = f"https://cdn.discordapp.com/avatars/341257685901246466/a_09dadd494a375adaced572682c8ec96c.png?size=4096",
                                        text = f"JeSuisUnBonWhisky#0001")
                EmbedTranslated.set_author(icon_url = botuser.avatar_url,
                                        name = botuser)

                try:
                    await TranslateMessage.remove_reaction(emoji = f"{payload.emoji.name}", member = payload.member)
                except discord.Forbidden:
                    pass
                
                if (str(DMOnOff) == "None") or (str(DMOnOff) == "(None,)") :
                    try:
                        SendRequest = await self.client.fetch_user(payload.user_id)
                        await SendRequest.send(embed = EmbedTranslated)
                    except discord.Forbidden:
                        await self.client.get_channel(payload.channel_id).send(embed = EmbedImpossibleSendDM)
                else :
                    await self.client.get_channel(payload.channel_id).send(embed = EmbedTranslated)


def setup(client):
    client.add_cog(ReactionEventSlash(client))
    print("Reaction Language Event cog ready !")
