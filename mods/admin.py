import importlib

from discord.ext import commands


async def reload_all(bot, mods):
    queue_mods = []
    queue_exts = []
    for mod in mods:
        queue_mods.append(mods[mod])
    for ext in bot.extensions:
        queue_exts.append(ext)
    for mod in queue_mods:
        importlib.reload(mod)
    for ext in queue_exts:
        bot.reload_extension(ext)
    return 'Reloaded all extension/modules.'


async def _reload_ext(bot, ext):
    try:
        bot.reload_extension(ext)
    except commands.ExtensionNotLoaded:
        bot.load_extension(ext)


async def _reload_mod(mod):
    try:
        importlib.reload(f'mods.{mod}')
    except ModuleNotFoundError:
        return 'Module not found.'
    except ImportError as e:
        return f'Import error {e}'
