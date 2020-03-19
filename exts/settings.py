from discord.ext import commands
from mods import firestore
from mods import info
from mods import vars_


@commands.command()
async def settings(ctx, command=None, field=None, value=None):
    uid = str(ctx.author.id)
    command_ = await firestore.get_command(uid, command)
        
    if not command:
        configurable = []
        [configurable.append(key) for key in vars_.info_.keys() if vars_.info_[key].configurable()]
        await ctx.send(f"Here are commands that you can configure.\n {configurable}")
        return
    elif command not in vars_.info_.keys():
        await ctx.send("The command you entered could not be found.")
        return
    elif command and not field:
        await ctx.send(f"The available settings for this command are {vars_.info_[command].get_settings()}")
        return
    elif not command or not field or not value:
        await ctx.send("Incorrect syntax, see `help settings`.")
        return
    elif field not in vars_.info_[command].get_settings():
        await ctx.send(f"The specified setting does not exist. See `settings {command}` for available settings.")
        return
    elif not vars_.info_[command].validate_setting(field, value):
        await ctx.send("That's not a valid option for this setting")
        return

    if vars_.info_[command].get_options(field) is None:
        value = not command_[field]
    await firestore.update_command(uid, command, field, value)


def setup(bot):
    info.Info(
        name='settings',
        brief='configure things for commands',
        usage='settings [command] [option] [value]',
    ).export(vars_.info_)

    bot.add_command(settings)
