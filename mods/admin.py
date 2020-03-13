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
        await _reload_mod(mod)
    for ext in queue_exts:
        await _reload_ext(bot, ext)
    return 'Reloaded all extension/modules.'


async def load(modext, bot=None):
    if not bot:
        return await _load_mod(modext)
    return _load_ext(modext, bot)


async def _reload_ext(bot, ext):
    try:
        bot.reload_extension(ext)
    except commands.ExtensionNotLoaded:
        bot.load_extension(ext)


async def _reload_mod(mod):
    try:
        importlib.reload(f'mods.{mod}')
    except ImportError as e:
        return f'Import error {e}'


async def _load_ext(bot, ext):
    try:
        bot.load_extension(f'exts.{ext}')
        return f'Loaded extension: {ext}'
    except commands.ExtensionAlreadyLoaded:
        return f'Extension **{ext}** already loaded.'
    except commands.ExtensionNotFound:
        return 'Extension **{ext}** not found'


async def _load_mod(mod):
    try:
        _ = importlib.import_module(f'mods.{mod}')
        return _, f'Loaded module: {mod}'
    except ModuleNotFoundError:
        _ = None
        return _, f'Module **{mod}** not found'
