import discord
from discord.ext import commands
from lxml import html

import datetime, requests, re

from src.helpers.global_vars import WIKI_BASE_URL
from src.helpers.weapons import weapons, hyphenatedWeps

def construct_wep_info_embed(weapon: str, sourceUrl: str, description: str, imageUrl: str, color: discord.Color, stats) -> discord.Embed:
    """
    Helper function to construct weapon embeds. This method
    should not be directly called outside of this file.
    """

    embed = discord.Embed(title=weapon, url=sourceUrl, timestamp=datetime.datetime.now(), color=color)
    embed.add_field(name="Description", value=description)
    embed.set_thumbnail(url=imageUrl)

    return embed

async def weapon_info_command(ctx: commands.Context, weapon: str):
    if weapon not in weapons:
        raise commands.BadArgument("Invalid option")
    
    # weapon ids are case sensitive, so capitalize the first letter of each word in the wep
    delim = "_"
    if weapon in hyphenatedWeps:
        delim = "-"
    
    wepId = delim.join(word.capitalize() for word in weapon.split('_')) 

    res = requests.get(f"{WIKI_BASE_URL}/{wepId}")
    tree: html.HtmlElement = html.fromstring(res.content)

    wepHeader: html.HtmlElement = tree.xpath(f"//span[@id='{wepId}']")[0].getparent()
    wepInfoTable: html.HtmlElement = wepHeader.getnext()

    wepDesc = wepInfoTable.xpath(".//td[@class='weapondesc']")[0].text

    wepBoxElement: html.HtmlElement = wepInfoTable.xpath(".//div[@class='weapon-box']")[0]

    style = wepBoxElement.attrib.get("style", "")
    matched = re.search(r'background-color:\s*(#[0-9A-Fa-f]{6})', style)
    bgColorHex = matched.group(1) if matched else None

    imgElement: html.HtmlElement = wepBoxElement.xpath(".//img")[0]
    imgUrl = imgElement.attrib.get("data-src", None)
    if not imgUrl:
        imgUrl = imgElement.attrib.get("src", "")
    
    #create embed
    embed = construct_wep_info_embed(wepId.replace("_", " "), res.url, wepDesc, imgUrl, discord.Color.from_str(bgColorHex), None)

    await ctx.send(embed=embed)