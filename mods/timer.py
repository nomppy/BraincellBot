from mods import firestore, core, util
import asyncio
import warnings
from datetime import datetime, timedelta


class Timer:
    def __init__(self, name):
        self.name = name
        self.pool = {}
        self.run = False

    async def pull_pool(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            self.pool = {**{doc.id: dict(cb=on_timer_trigger(doc.id, self.name), **doc.to_dict())
                            for doc in await firestore.get_pool(self.name)}, **self.pool}

    def add(self, uid: str, conf):
        self.pool[uid] = conf

    def stop(self):
        self.run = False

    async def push_poll(self):
        await self.pull_pool()
        pool = [doc.id for doc in await firestore.get_pool(self.name)]
        [
            await firestore.add_to_pool(self.name, uid, conf)
            for uid, conf in self.pool.items()
            if uid not in pool
        ]

    async def run_timer(self):
        if not self.run:
            self.run = True
            while self.run:
                await self.pull_pool()
                await self.push_poll()
                await asyncio.sleep(30)
                for uid, conf in self.pool.items():
                    command_ = await firestore.get_command(uid, self.name)

                    if datetime.utcnow() >= datetime.strptime(command_['scheduled'], "%Y-%m-%d %H:%M:%S.%f") \
                            and int(command_['timer']) != 0:
                        await conf['cb']
        else:
            return True


async def init_user_newpfp_timer(uid, interval):
    await firestore.update_command_field(uid, 'newpfp', 'scheduled',
                                         str(datetime.utcnow() + timedelta(minutes=int(interval))))


async def on_timer_trigger(uid, command):
    user_ = await firestore.get_user(uid)
    command_ = await firestore.get_command(uid, command)
    await firestore.update_command_field(uid, command, 'scheduled',
                                         str(datetime.utcnow() + timedelta(minutes=int(command_['timer']))))
    if command == 'newpfp':
        if user_['self']:
            await firestore.update_command_field(uid, 'newpfp', 'link', await core.get_cat_link())
            await util.flash_flag(uid, 'newpfp')
        else:
            await core.change_avatar(await firestore.get_user(uid), await core.get_cat_link())
