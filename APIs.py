import ccxt
import os
from dotenv import load_dotenv
import logging

load_dotenv()


# Функция получения актуального курса BTC
def get_actual_price():
    try:
        we = ccxt.wavesexchange({'apiKey': os.getenv('PUBLIC_API_KEY'), 'secret': f'{os.getenv("ACCESS_KEY")}'})
        we.load_markets()
        price = we.markets['BTC-WXG/USDT-WXG']['info']['24h_close']
        return price
    except Exception as e:
        logging.error(f"Error retrieving actual price: {e}")
        price = None


# Функция получения ссылки на бота
def get_bot_url() -> str:
    return 'https://t.me/learning_test_bot_bot'


# Функция генерирования API запроса на обмен BTC
def get_payment_url_btc(amount: float) -> str:
    return f"https://wx.network/#send/{os.getenv('AMOUNT_ASSET_ID_WBTC')}?recipient={os.getenv('ADDRESS')}&amount={amount}&referrer={get_bot_url()}&strict"


# Функция генерирования API запроса на обмен USDT
def get_payment_url_usdt(amount: float) -> str:
    return f"https://wx.network/#send/{os.getenv('AMOUNT_ASSET_ID_WBTC2')}?recipient={os.getenv('ADDRESS')}&amount={amount}&referrer={get_bot_url()}&strict"
