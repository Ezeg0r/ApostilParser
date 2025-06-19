import requests
import time
from telegram import Bot
import asyncio
import httpx  # async HTTP client
import os
from dotenv import load_dotenv



# === Настройки ===
API_URL = "https://api.dkko.edu.gov.by/api/order-units/visits/date"
HEADERS = {
    "X-API-TOKEN": "ec6aab37-f042-4f9d-baaf-bf8069124976",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Origin": "https://dkko.edu.gov.by",
    "Referer": "https://dkko.edu.gov.by/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0"
}
PARAMS = {
    "isActive": "false",
    "numberOfDocs": "1",
    "month": "7",
    "year": "2025"
}
EXPECTED = {
    'isActive': False, 
    'dates': ['2025-07-01', '2025-07-02', '2025-07-03', '2025-07-04', '2025-07-05', 
              '2025-07-06', '2025-07-07', '2025-07-08', '2025-07-09', '2025-07-10', 
              '2025-07-11', '2025-07-12', '2025-07-13', '2025-07-14', '2025-07-15', 
              '2025-07-16', '2025-07-17', '2025-07-18', '2025-07-19', '2025-07-20', 
              '2025-07-21', '2025-07-22', '2025-07-23', '2025-07-24', '2025-07-25', 
              '2025-07-26', '2025-07-27', '2025-07-28', '2025-07-29', '2025-07-30', 
              '2025-07-31']
}


load_dotenv()

# === Telegram bot config ===
TELEGRAM_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# === Функция отправки сообщений в Telegram ===
async def notify_telegram(message: str):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print("Ошибка отправки в Telegram:", e)

# === Основной асинхронный цикл ===
async def main_loop():
    global EXPECTED  # чтобы обновлять переменную из внешнего скоупа

    print("Бот запущен. Нажми Ctrl+C чтобы остановить.")

    async with httpx.AsyncClient(timeout=10) as client:
        while True:
            try:
                r = await client.get(API_URL, headers=HEADERS, params=PARAMS)
                data = r.json()

                if data != EXPECTED:
                    await notify_telegram("❗ Обнаружено изменение в данных!\n" + str(data))
                    EXPECTED = data  # Обновим шаблон, чтобы не спамить
                else:
                    print("✅ Всё стабильно.")

            except Exception as ex:
                await notify_telegram(f"⚠️ Ошибка при запросе: {ex}")
                print("⚠️ Ошибка:", ex)

            await asyncio.sleep(10)

# Запуск
if __name__ == "__main__":
    asyncio.run(main_loop())
