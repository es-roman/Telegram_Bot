from aiogram import Router

from . import search, start


def get_routers() -> list[Router]:
    return [start.router, search.router]
