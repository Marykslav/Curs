from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import requests
import logging

import app.keyboargs as kb
import app.database.requests as rq

# Налаштування логування
logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привіт Шинігамі, тут ми радимо найкращі аніме! Натисни /help, щоб дізнатись більше що наш бот вміє', reply_markup=kb.main)


@router.message(Command('help'))
async def get_help(message: Message, state: FSMContext):
    await message.answer('''Ми збираємо та пропонуємо найкращі твори японської культури. 
Наша мета - створити для вас затишне місце, 
де ви зможете відкрити для себе нові світи, відчути емоції із кожним переглядом та знайти нових улюбленців серед героїв та сюжетів.

У нас ви знайдете широкий вибір аніме, манґи та новинок, а також дружнє співтовариство однодумців, готових поділитися своїми враженнями та рекомендаціями.

Будьте в курсі останніх трендів, знаходьте нові аніме для перегляду та отримуйте задоволення від спілкування з нами!

\n/start - розпочне роботу бота. \n/help - довідка можливостей боту.\n/get_photo - знайде аніме яке ти не зміг знайти або хочеш подивитись, але не знаєш назви.\nСамі аніме та манги ти можеш обрати на панелі знизу для зручності щоб не вводити команди. Там ти зможеш знайти як аніме за твоїми улюбленими жанрами так і подивитись нові для себе жанри. Також там представлені новинки за 2023 та 2024 рік які виходять або уже вийшли та звісно ж анонси. Ну і нарешті ми дібрались до манги. Серед Вас є багато хто полюбляє мангу? Впевнений що так, тому всі найкращі манги ти також зможеш знайти там.\нЗ повагою, команда нашого аніме бота)''', reply_markup=kb.main)


@router.message(Command('get_anime'))
async def get_anime(message: Message):
    query = message.get_args()
    if not query:
        await message.answer("Будь ласка, введіть назву аніме після команди /get_anime.")
        logging.info("Користувач не ввів назву аніме.")
        return

    logging.info(f"Пошук аніме: {query}")

    url = f'https://kitsu.io/api/edge/anime?filter[text]={query}'
    try:
        response = requests.get(url)
        logging.info(f"API Запит URL: {url}")
        logging.info(f"HTTP статус-код: {response.status_code}")

        if response.status_code != 200:
            await message.answer("Виникла помилка при отриманні даних з API. Спробуйте пізніше.")
            logging.error(f"HTTP статус-код: {response.status_code}")
            return

        response_json = response.json()
        logging.info(f"API Відповідь JSON: {response_json}")

        if not response_json['data']:
            await message.answer("Аніме не знайдено. Спробуйте іншу назву.")
            logging.info("Аніме не знайдено.")
            return

        for data in response_json['data']:
            anime = data['attributes']
            title = anime.get('canonicalTitle', 'Немає назви')
            rating = anime.get('popularityRank', 'Немає рейтингу')
            poster = anime.get('posterImage', {}).get('large', '')

            if poster:
                await message.answer_photo(poster, caption=f"{title}\nRating: {rating}")
                logging.info(
                    f"Відправлено фото аніме: {title} з рейтингом: {rating}")
            else:
                await message.answer(f"{title}\nRating: {rating}\n(Постер відсутній)")
                logging.info(
                    f"Аніме: {title} з рейтингом: {rating} без постера")

    except Exception as e:
        logging.error(f"Помилка: {e}")
        await message.answer("Виникла помилка при отриманні даних. Спробуйте пізніше.")


@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgQAAxkBAAICt2ZjXMrTnipGIosUnAoRDly_uo0XAAINxjEb-R0ZU2AE4WWG5bPEAQADAgADeAADNQQ',
                               caption='Це - Бліч, улюблене аніме автора бота.')


@router.message(F.text == 'Як справи?')
async def how_are_you(message: Message):
    await message.answer('Чудово, шукаю цікаві новинки саме для тебе, а як в тебе?')


@router.message(F.text == 'Добре')
async def how_are_you(message: Message):
    await message.answer('Тоді швидше іди переглядати нашу підбірку, обирай все що сподобалось')


@router.message(F.text == 'Жанри')
async def catalog(message: Message):
    await message.answer('Виберіть жанр аніме який бажаєте', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Ви вибрали жанри')
    await callback.message.answer('Виберіть аніме за цим жанром',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Ви вибрали аніме яке бажаєте')
    await callback.message.answer(f'Назва: {item_data.name}\nОпис: {item_data.description}\нРейтинг: {item_data.price}')


@router.message(F.text == 'Новинки')
async def novelty(message: Message):
    await message.answer('Оберіть новинку яка сподобалась', reply_markup=await kb.novelties())


@router.callback_query(F.data.startswith('novelty_'))
async def novelty(callback: CallbackQuery):
    await callback.answer('Ви вибрали новинки')
    await callback.message.answer('Оберіть рік релізу',
                                  reply_markup=await kb.items1(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item1_'))
async def novelty(callback: CallbackQuery):
    item1_data = await rq.get_item1(callback.data.split('_')[1])
    await callback.answer('Ви вибрали аніме яке бажаєте')
    await callback.message.answer(f'Назва: {item1_data.name}\нОпис: {item1_data.description}\нРейтинг: {item1_data.price}')


@router.message(F.text == 'Манга')
async def manga(message: Message):
    await message.answer('Оберіть жанр манги який бажаєте', reply_markup=await kb.mangs())


@router.callback_query(F.data.startswith('mangs_'))
async def mangs(callback: CallbackQuery):
    await callback.answer('Ви вибрали жанри')
    await callback.message.answer('Виберіть аніме за цим жанром',
                                  reply_markup=await kb.items2(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item2_'))
async def mangs(callback: CallbackQuery):
    item2_data = await rq.get_item2(callback.data.split('_')[1])
    await callback.answer('Ви вибрали аніме яке бажаєте')
    await callback.message.answer(f'Назва: {item2_data.nammma}\нОпис: {item2_data.descripniot}\нРейтинг: {item2_data.respect}')
