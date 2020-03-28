import re

import discord
from discord.ext import commands
from mods import firestore, info, vars_


@commands.command()
async def whitelist(ctx, command=None, user=None, remove=False):
    embed = discord.Embed(title='Whitelist')
    if command:
        if not user:
            embed.description = 'TODO send whitelist for command here'
            embed.colour = vars_.colour_success
        else:
            match = re.search(r"[0-9]+", user)
            if match:
                uid = match.group(0)
                uid_ = str(ctx.author.id)
                command_ = await firestore.get_command(uid_, command)
                if not command_:
                    embed.description = 'Command does not exist'
                    embed.colour = vars_.colour_error
                else:
                    whitelist_ = command_['whitelist']
                    if not whitelist_:
                        embed.description = 'Command has no whitelist'
                        embed.colour = vars_.colour_warning
                    if remove:
                        if uid not in whitelist_:
                            embed.description = 'User not in whitelist'
                            embed.colour = vars_.colour_error
                        else:
                            whitelist_.remove(uid)
                            await firestore.update_command_field(uid_, command, 'whitelist', whitelist_)
                            return 'User removed from whitelist'
                    elif uid in whitelist_:
                        embed.description = 'User already in whitelist'
                        embed.colour = vars_.colour_error
                    else:
                        whitelist_.append(uid)
                        await firestore.update_command_field(uid_, command, 'whitelist', whitelist)
                        embed.description = 'User added to whitelist'
                        embed.colour = vars_.colour_success
    ctx.send(embed=embed)


def setup(bot):
    info.Info(
        name='whitelist',
        brief='allow another user to use a command',
        usage='`whitelist <command> <user>`',
        category='Access Control',
    ).export(vars_.info_)
    bot.add_command(whitelist)
