import asyncio

from discord.ext import commands
from mods import firestore


async def flash_flag(uid, command):
    await firestore.update_command_field(uid, command, 'flag', True)
    await firestore.update_user_field(uid, 'flag', True)
    await asyncio.sleep(0.1)
    await firestore.update_command_field(uid, command, 'flag', False)
    await firestore.update_user_field(uid, 'flag', False)


def ctx_dict(ctx=None, dict_=None):
    if not ctx and not dict_:
        return
    elif ctx:  # turning ctx to dict
        return {
            'message': message_dict(message=ctx.message),
            'args': ctx.args,
            'kwargs': ctx.kwargs,
            'prefix': ctx.prefix,
            'command': ctx.command,
            'invoked_with': ctx.invoked_with
        }
    elif dict_:  # turning dict into ctx
        return commands.Context(
            message=dict_['message'],
            args=dict_['args'],
            kwargs=dict_['kwargs'],
            prefix=dict_['prefix'],
            command=dict_['command'],
            invoked_with=dict_['invoked_with']
        )


def message_dict(message=None, dict_=None):
    if not message and not dict_:
        return
    elif message:  # turning message to dict
        return {
            'author': message.author,
            'content': message.content,
            'id': message.id,
        }
