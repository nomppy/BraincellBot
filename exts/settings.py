from discord.ext import commands
from mods import firestore
from mods import info


@commands.command()
async def settings(ctx, command=None, field=None, value=None):
    uid = str(ctx.author.id)
    command_ = await firestore.get_command(uid, command)

    if not command:
        # TODO send list of available settings here
        return
    elif not command_:
        await ctx.send("The command you entered could not be found.")
        return
    elif command and not field:
        # TODO send list of available settings for the specified command here
        return
    elif not command or not field or not value:
        await ctx.send("Incorrect syntax, see `help settings`.")
        return
    elif field not in info.get_settings(command)['fields'].keys():
        await ctx.send(f"The specified setting does not exist. See `settings {command}` for available settings.")

    await firestore.update_command(uid, command, field, value)


def setup(bot):
    info.Help(
        name='settings',
        description='configure user-specific settings such as prefix, counter, whitelist',
        usage='`settings [command] [option] [value]`'
    ).export()
    bot.add_command(settings)
