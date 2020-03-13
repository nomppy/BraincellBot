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


async def reload_load(modext, bot=None):
    st = ''
    if not bot:  # looking for a module
        mod = await _reload_mod(modext)
        if not mod:  # if module is not loaded
            mod = await _load_mod(modext)  # tries to load module
            st = f'Loaded modules: **{modext}**'
            if not mod:
                st = f'Module **{modext}** not found'
                raise ModuleNotFoundError
        st = f'Reloaded modules: **{modext}**'
        return mod, st
    else:
        st = await _reload_ext(bot, modext)
        if not st:
            st = await _load_ext(bot, modext)
            if not st:
                raise commands.ExtensionNotFound
        return st


async def _reload_ext(bot, ext):
    try:
        bot.reload_extension(ext)
        return f'Reloaded extension: **{ext}**'
    except commands.ExtensionNotLoaded:
        return None


async def _reload_mod(mod):
    try:
        mod = importlib.reload(f'mods.{mod}')
        return mod
    except ModuleNotFoundError:
        return None


async def _load_ext(bot, ext):
    try:
        bot.load_extension(f'exts.{ext}')
        return f'Loaded extension: {ext}'
    except commands.ExtensionNotFound:
        return None


async def _load_mod(mod):
    try:
        _ = importlib.import_module(f'mods.{mod}')
        return _
    except ModuleNotFoundError:
        return None
