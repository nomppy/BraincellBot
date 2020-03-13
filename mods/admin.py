import importlib


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
