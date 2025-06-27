import os
import time
import yfinance as yf
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SYMBOL = os.getenv("SYMBOL", "NVDA")
CALL_TRIGGER = float(os.getenv("CALL_TRIGGER", "156.0"))
PUT_TRIGGER = float(os.getenv("PUT_TRIGGER", "154.5"))

bot = Bot(token=TOKEN)
last_status = None

def check_price():
    global last_status
    price = yf.Ticker(SYMBOL).history(period="1m")["Close"][-1]
    if price >= CALL_TRIGGER and last_status != "CALL":
        bot.send_message(CHAT_ID, f"🚨 {SYMBOL} broke above {CALL_TRIGGER} → CALL signal!")
        last_status = "CALL"
    elif price <= PUT_TRIGGER and last_status != "PUT":
        bot.send_message(CHAT_ID, f"🚨 {SYMBOL} dropped below {PUT_TRIGGER} → PUT signal!")
        last_status = "PUT"

if __name__ == "__main__":
    while True:
        try:
            check_price()
        except Exception as e:
            print("Error:", e)
        time.sleep(60)
