from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os
import ccxt
import logging

we = ccxt.wavesexchange({'apiKey': os.getenv('PUBLIC_API_KEY')})
we.load_markets()
price = we.markets['BTC-WXG/USDT-WXG']['info']['24h_close']
load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

button = types.ReplyKeyboardMarkup(resize_keyboard=True)
button.add('Получить')

buttons_to_exchange = types.InlineKeyboardMarkup(row_width=1)
buttons_to_exchange.add(types.InlineKeyboardButton(text='Обменять BTC на USDT', callback_data='BTC-USDT'),
                        types.InlineKeyboardButton(text='Обменять USDT на BTC', callback_data='USDT-BTC'),
                        types.InlineKeyboardButton(text='Перейти на сайт биржи', url='https://wx.network'))


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Получить'))
    await message.answer_sticker('CAACAgIAAxkBAAIDG2VyLufSqhoIbuCe5zIO2qm5oS0XAAL7BQAClvoSBZdb7eV44WgWMwQ')
    await message.answer(
        f"""Привет {message.from_user.first_name}, это бот, который предоставляет информацию о курсе BTC/USDT и позволяет совершить обмен.
Чтобы получить список команда введите команду /help""", reply_markup=button)


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await message.answer(f"""
    Доступный список комманд:
/help - вывод списка команд данного бота
/get_price - получение курса BTC/USDT
/BTC_to_USDT - обмен BTC на USDT
/USDT_to_BTC - обмен USDT на BTC
""")


@dp.message_handler(text='Получить')
async def keyboard(message: types.Message):
    global price
    await message.answer(f"""Актуальный курс <b>BTC</b> на бирже WX Network:
{price} <b>USDT</b>""", parse_mode='HTML', reply_markup=buttons_to_exchange)


@dp.message_handler(commands=['get_price'])
async def get_price(message: types.Message):
    global price
    await message.answer(f"""Актуальный курс <b>BTC</b> на бирже WX Network:
{price} <b>USDT</b>""", parse_mode='HTML', reply_markup=buttons_to_exchange)


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Воспользуйтесь одной из команд, список команд вы можете увидеть, введя команду /help')


@dp.callback_query_handler()
async def double_exchange(callback_query: types.CallbackQuery):
    if callback_query.data == 'BTC-USDT':
        await bot.send_message(chat_id=callback_query.from_user.id, text="Обмен BTC на USDT пока не реализован")
    elif callback_query.data == 'USDT-BTC':
        await bot.send_message(chat_id=callback_query.from_user.id, text="Обмен USDT на BTC пока не реализован")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
