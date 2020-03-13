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


async def reload_load(modext, mods=None, bot=None):
    if mods:  # looking for a module
        if modext in mods:
            mod = await _reload_mod(mods[modext])
            st = f'Reloaded module: **{modext}**'
        else:  # if module is not loaded
            mod = await _load_mod(modext)  # tries to load module
            st = f'Loaded modules: **{modext}**'
            if not mod:
                st = f'Module **{modext}** not found'
                raise ModuleNotFoundError
        st = f'Reloaded module: **{modext}**'
        return mod, st
    if bot:
        if f'exts.{modext}' in bot.extensions:
            st = await _reload_ext(bot, modext)
        else:
            st = await _load_ext(bot, modext)
            if not st:
                raise commands.ExtensionNotFound('')
        return st
    return 'Must provide either mod or bot'


async def _reload_ext(bot, ext):
    bot.reload_extension(f'exts.{ext}')
    return f'Reloaded extension: **{ext}**'


async def _reload_mod(mod):
    mod = importlib.reload(mod)
    return mod


async def _load_ext(bot, ext):
    try:
        bot.load_extension(f'exts.{ext}')
        return f'Loaded extension: {ext}'
    except commands.ExtensionNotFound:
        return None


async def _load_mod(mod):
    try:
        mod = importlib.import_module(f'mods.{mod}')
        return mod
    except ModuleNotFoundError:
        return None
