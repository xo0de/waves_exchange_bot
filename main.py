from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from aiogram.types.web_app_info import WebAppInfo
from APIs import get_actual_price, get_payment_url_BTC, get_payment_url_USDT
import logging
import os

# Объявление перменных и экземпляров классов
load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)
global_amount = None



# Кнопки
button = types.ReplyKeyboardMarkup(resize_keyboard=True)
button.add('Получить')

buttons_to_exchange = types.InlineKeyboardMarkup(row_width=1)
buttons_to_exchange.add(types.InlineKeyboardButton(text='Обменять криптовалюту', callback_data='data'),
                        types.InlineKeyboardButton(text='Перейти на сайт биржи', url='https://wx.network/'))


# Обработчик команды старт
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Получить'))
    await message.answer_sticker('CAACAgIAAxkBAAIDG2VyLufSqhoIbuCe5zIO2qm5oS0XAAL7BQAClvoSBZdb7eV44WgWMwQ')
    await message.answer(
        f"""Привет {message.from_user.first_name}, это бот, который предоставляет информацию о курсе BTC/USDT и позволяет совершить обмен.
Чтобы получить список команда введите команду /help""", reply_markup=button)


# Обработчик команды htlp
@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await message.answer(f"""
    Доступный список комманд:
/help - вывод списка команд данного бота
/get_price - получение курса BTC/USDT
/exchange - произвести обмен
""")


# Обработчик команды /get_price
@dp.message_handler(commands=['get_price'])
async def get_price(message: types.Message):
    await message.answer(f"""Актуальный курс <b>BTC</b> на бирже WX Network:
<b>{get_actual_price()} USDT</b>""", parse_mode='HTML', reply_markup=buttons_to_exchange)


# Обработчик команды /exchange
@dp.message_handler(commands=['exchange'])
async def get_price(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите сумму которую Вы хотите обменять:")


# Обработчик кнопки "Получить"
@dp.message_handler(text='Получить')
async def keyboard(message: types.Message):
    await message.answer(f"""Актуальный курс <b>BTC</b> на бирже WX Network:
<b>{get_actual_price()} USDT</b>""", parse_mode='HTML', reply_markup=buttons_to_exchange)

# Обработчик суммы к обмену
@dp.message_handler(lambda message: message.text.isdigit())
async def handle_number(message: types.Message):
    global global_amount
    if int(message.text) >= 0:
        global_amount = float(message.text)
    else:
        await message.reply(
            f"Введите положительное число:")
    buttons_ready_to_exchange = types.InlineKeyboardMarkup(row_width=1)
    buttons_ready_to_exchange.add(types.InlineKeyboardButton(text=f'Обменять {global_amount} BTC на USDT', web_app=WebAppInfo(url=f'{get_payment_url_BTC(global_amount)}')),
                                        types.InlineKeyboardButton(text=f'Обменять {global_amount} USDT на BTC', web_app=WebAppInfo(url=f'{get_payment_url_USDT(global_amount)}')))
    await message.reply(f"Сумма к обмену: {global_amount}", reply_markup=buttons_ready_to_exchange)

# Обработчик любого текста
@dp.message_handler(lambda message: message.text.isalpha(), content_types=['text'])
async def handle_non_number(message: types.Message):
    await message.reply("""В случае, если Вы хотите произвести обмен, пожалуйста, введите корректное число. 
Иначе воспользуйтесь одной из команд, список команд вы можете увидеть, введя команду /help""")

# Обработчик callback данных от кнопки "Обменять"
@dp.callback_query_handler()
async def double_exchange(callback_query: types.CallbackQuery):
    if callback_query.data == 'data':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Введите сумму которую Вы хотите обменять:")

# Запуск программы
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
