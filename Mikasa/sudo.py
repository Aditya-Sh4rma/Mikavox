import asyncio

from pyrogram import filters

import config
from Mikasa import mongo

_sudo_ids: set[int] = set()
_loaded = False
_lock = asyncio.Lock()


async def load_sudoers(force: bool = False) -> set[int]:
    global _loaded

    if _loaded and not force:
        return _sudo_ids

    async with _lock:
        if _loaded and not force:
            return _sudo_ids

        _sudo_ids.clear()
        try:
            _sudo_ids.update(await mongo.get_sudoers())
        except Exception:
            pass
        if config.OWNER_ID:
            _sudo_ids.add(config.OWNER_ID)

        _loaded = True
        return _sudo_ids


def get_sudo_ids() -> set[int]:
    return set(_sudo_ids)


def is_sudo(user_id: int) -> bool:
    return user_id in _sudo_ids


def is_owner(user_id: int) -> bool:
    return bool(config.OWNER_ID) and user_id == config.OWNER_ID


async def add_sudo(user_id: int) -> bool:
    await load_sudoers()
    if user_id in _sudo_ids:
        return False

    await mongo.add_sudo(user_id)
    _sudo_ids.add(user_id)
    return True


async def remove_sudo(user_id: int) -> bool:
    await load_sudoers()
    if user_id not in _sudo_ids:
        return False

    await mongo.del_sudo(user_id)
    _sudo_ids.discard(user_id)
    return True


async def _sudo_filter_func(_, client, update) -> bool:
    await load_sudoers()
    user = getattr(update, "from_user", None)
    return bool(user and user.id in _sudo_ids)


async def _owner_filter_func(_, client, update) -> bool:
    user = getattr(update, "from_user", None)
    return bool(user and is_owner(user.id))


sudo_filter = filters.create(_sudo_filter_func, "SudoFilter")
owner_filter = filters.create(_owner_filter_func, "OwnerFilter")
