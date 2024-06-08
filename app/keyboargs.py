from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item, get_novelties, get_novelty_item1, get_mangs, get_manga_item2

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Жанри')],
                                     [KeyboardButton(text='Новинки')],
                                     [KeyboardButton(text='Манга'),
                                      KeyboardButton(text='Про нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Виберіть пункт меню...')


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                     callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(
        text='На головну', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(
            text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(
        text='На головну', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def novelties():
    all_novelties = await get_novelties()
    keyboard = InlineKeyboardBuilder()
    for novelty in all_novelties:
        keyboard.add(InlineKeyboardButton(text=novelty.name,
                     callback_data=f"novelty_{novelty.id}"))
    keyboard.add(InlineKeyboardButton(
        text='На головну', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def items1(novelty_id):
    all_items1 = await get_novelty_item1(novelty_id)
    keyboard = InlineKeyboardBuilder()
    for item1 in all_items1:
        keyboard.add(InlineKeyboardButton(
            text=item1.name, callback_data=f"item1_{item1.id}"))
    keyboard.add(InlineKeyboardButton(
        text='На головну', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def mangs():
    all_mangs = await get_mangs()
    keyboard = InlineKeyboardBuilder()
    for manga in all_mangs:
        keyboard.add(InlineKeyboardButton(text=manga.name,
                     callback_data=f"manga_{manga.id}"))
    keyboard.add(InlineKeyboardButton(
        text='На головну', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def items2(manga_id):
    all_items2 = await get_manga_item2(manga_id)
    keyboard = InlineKeyboardBuilder()
    for item2 in all_items2:
        keyboard.add(InlineKeyboardButton(
            text=item2.name, callback_data=f"item2_{item2.id}"))
    keyboard.add(InlineKeyboardButton(
        text='На головну', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
