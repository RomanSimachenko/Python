import logging
import asyncio
from datetime import datetime
import pytz

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import config
import database
import monitoring
import tasks


NEGATIVE_RESPONSES = {
        'no_k_bal': "❌ Ви ще не встановили конкурсний бал",
        'no_universities': "❌ Ви ще не встановили університети",
}

RESULT_VIEWS = {
    "with_list": "Виводити результат моніторингу із списком абітурієнтів, \
які мають бали вищі або рівні Вашому",
    "without_list": "Виводити результат моніторингу без списку абітурієнтів, \
які мають бали вищі або рівні Вашому" ,
}

API_TOKEN = config.API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class User_k_bal_State(StatesGroup):
    k_bal = State()


@dp.message_handler(commands=('set_k_bal',))
async def set_k_bal(message: types.Message):
    await message.answer("🏆 Введіть Ваш конкурсний бал: ")
    await User_k_bal_State.k_bal.set()


@dp.message_handler(state=User_k_bal_State.k_bal)
async def get_k_bal(message: types.Message, state: FSMContext):
    await state.update_data(k_bal=message.text.strip())
    data = await state.get_data()
    await state.finish()

    response = await database.save_k_bal_to_db(message['from'], data['k_bal'], message['chat'])
    await message.answer(response)


@dp.message_handler(commands=('my_k_bal',))
async def my_k_bal(message: types.Message):
    k_bal = await database.get_k_bal(message['from'])
    if k_bal:
        await message.answer(f"Ваш конкурсний бал {k_bal}")
    else:
        await message.answer(NEGATIVE_RESPONSES['no_k_bal'])


class User_universities_State(StatesGroup):
    universities = State()


@dp.message_handler(commands=('set_universities',))
async def set_universities(message: types.Message):
    await message.answer("🖇 Введіть університети: ")
    await User_universities_State.universities.set()


@dp.message_handler(state=User_universities_State)
async def get_universities(message: types.Message, state: FSMContext):
    await state.update_data(universities=message.text.strip())
    data = await state.get_data()
    await state.finish()

    universities = data['universities']
    new_uns = []
    for un in universities.split(','):
        new_uns += [un[:-1]] if un[-1] == '/' else [un]
    uns = ','.join(new_uns)

    response = await database.save_universities_to_db(message['from'], uns, message['chat'])
    await message.answer(response)


@dp.message_handler(commands=('my_universities',))
async def my_universities(message: types.Message):
    universities = await database.get_universities(message['from'])
    if universities:
        response = f"Ваші університети: \n{universities}"
        await message.answer(response, disable_web_page_preview=True)
    else:
        await message.answer(NEGATIVE_RESPONSES['no_universities'])


@dp.message_handler(commands=('run_monitoring',))
async def run_monitoring(message: types.Message):
    k_bal = await database.get_k_bal(message['from'])
    if not k_bal:
        await message.answer(NEGATIVE_RESPONSES['no_k_bal'])
        return

    universities = await database.get_universities(message['from'])
    if not universities:
        await message.answer(NEGATIVE_RESPONSES['no_universities'])
        return

    for university in universities.split(','):
        try:
            un = await monitoring.process_un(university, k_bal)
            await message.answer(f"\
{un.name}({un.url}): \nВсього {un.k_higher} \
абітурієнтів із {un.k_all} мають конкурсний бал вище \
або рівний {k_bal}, серед них: {un.k_kv} із квотою та {un.k_k} на контракт",
                            disable_web_page_preview=True)

            result_view = await database.get_result_view(message['from'])
            if result_view == 'with_list':
                await message.answer("\
№ Призвіще та ініціали | Пріорітет | Конкурсний бал | Квота(+/-) | Бюджет(Б)/Контракт(К)\
")
                result_list = ""
                for index, entrant in enumerate(un.entrants):
                    result_list += f"\
{index + 1}. {entrant.full_name} | {entrant.priority} | {entrant.k_bal} | {entrant.kvota} | {entrant.b_or_k}\n\
"
                    if (index + 1) % 50 == 0:
                        await message.answer(result_list)
                        result_list = ""
                await message.answer(result_list)
        except:
            await message.answer("❌ Упс... Щось пішло не так\
                    \nМожливо, університети введені у неправильному форматі")


@dp.message_handler(commands=('change_result_view',))
async def change_result_view(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Із списком абітурієнтів", callback_data="btn_with_list"))
    keyboard.add(types.InlineKeyboardButton(text="Без списку абітурієнтів", callback_data="btn_without_list"))

    await message.answer("📝 Як виводити результат моніторингу: ", reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith="btn_"))
async def callbacks_btn(call: types.CallbackQuery):
    result_view = '_'.join(call.data.split('_')[1:])

    result_view = await database.change_result_view(call.from_user, result_view)

    await call.message.edit_text('✅ ' + RESULT_VIEWS[result_view])
    await call.answer()


@dp.message_handler(commands=('my_data',))
async def my_data(message: types.Message):
    id = message['from']['id']

    k_bal = await database.get_k_bal(message['from'])
    k_bal = k_bal if k_bal else NEGATIVE_RESPONSES['no_k_bal']

    universities = await database.get_universities(message['from'])
    universities = universities.split(',') if universities else None

    result_view = await database.get_result_view(message['from'])
    result_view = RESULT_VIEWS[result_view]

    auto_monitoring = await database.get_auto_monitoring(message['from'])

    result_card = f"\
🔑 ID: {id}\n\
🏆 Конкурсний бал: {k_bal}\n\
🖇 Університети: \
"
    if universities:
        for index in range(len(universities)):
            result_card += f"\n{index + 1}) {universities[index].strip()},"
        result_card = result_card[:-1]
    else:
        result_card += NEGATIVE_RESPONSES['no_universities']

    result_card += f"\n📝 Вигляд результату моніторингу: \n{result_view}\
\n⏱ Автоматичний моніторинг: " 
    result_card += f"кожен день о {auto_monitoring}" if auto_monitoring else "вимкнуто"

    await message.reply(result_card, disable_web_page_preview=True)


class User_auto_monitoring_State(StatesGroup):
    time = State()


@dp.message_handler(commands=('enable_auto_monitoring',))
async def enable_auto_monitoring(message: types.Message):
    k_bal = await database.get_k_bal(message['from'])
    if not k_bal:
        await message.answer(NEGATIVE_RESPONSES['no_k_bal'])
        return

    universities = await database.get_universities(message['from'])
    if not universities:
        await message.answer(NEGATIVE_RESPONSES['no_universities'])
        return

    await message.answer("⏱ Введіть час для автоматичного моніторингу, \
у форматі години:хвилини")
    await User_auto_monitoring_State.time.set()


@dp.message_handler(state=User_auto_monitoring_State.time)
async def get_auto_monitoring(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text.strip())
    data = await state.get_data()
    await state.finish()

    response = await database.enable_auto_monitoring(message['from'], data['time'])

    await message.answer(response)

@dp.message_handler(commands=('my_auto_monitoring',))
async def my_auto_monitoring(message: types.Message):
    auto_monitoring = await database.get_auto_monitoring(message['from'])

    if auto_monitoring:
        await message.answer(f"Автоматичний моніторинг: кожен день о {auto_monitoring}")
    else:
        await message.answer("Автоматичний моніторинг: вимкнуто")


@dp.message_handler(commands=('disable_auto_monitoring',))
async def disable_auto_monitoring(message: types.Message):
    response = await database.disable_auto_monitoring(message['from'])

    await message.answer(response)


async def scheduled(wait_for):
    TZ = pytz.timezone("Europe/Kiev")
    while True:
        await asyncio.sleep(wait_for)
        time_now = datetime.now(TZ).strftime("%H:%M")
        await tasks.auto_monitoring(bot, time_now.strip())


def run_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(60))
    executor.start_polling(dp, skip_updates=True)
