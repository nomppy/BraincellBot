import discord
from mods import timer

mods = {'_': '_'}  # place holder
ignore = ['_', 'vars_.py']  # ignore on loading phase
info_ = {}
repeat_ready = False
unreg = ['register', 'unregister -d', 'unregister']

newpfp_timer = timer.Timer('newpfp')

colour_success = discord.Colour.from_rgb(45, 214, 90)
colour_error = discord.Colour.from_rgb(161, 35, 44)
colour_warning = discord.Colour.from_rgb(209, 200, 31)

default_footer_text = 'created and maintained by Spes#0845'
