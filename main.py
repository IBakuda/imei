import asyncio
import logging
from aiogram import Bot, Dispatcher

import config

import httpx
from aiogram.filters import CommandStart
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


async def check_imei(imei: str):
    headers = {
        'Authorization': f'Bearer {config.API_TOKEN}',
        'Content-Type': 'application/json',
    }

    data = {
        'deviceId': imei,
        'serviceId': config.SERVICE_ID,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(config.URL_CHECK, json=data, headers=headers)
        print(response.json())
        return response.json()


@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if user_id not in config.WHITE_LIST:
        await message.answer("Доступ запрещен. Вы не в списке разрешенных пользователей.")
        return
    await message.answer("Добро пожаловать! Вы имеете доступ к боту.")


@dp.message()
async def handle_imei(message: Message):
    if message.from_user.id not in config.WHITE_LIST:
        return await message.answer("Доступ запрещен. Вы не в списке разрешенных пользователей.")

    imei = message.text.strip()

    if not imei.isdigit() or len(imei) not in {14, 15}:
        return await message.answer("Неверный IMEI")

    response = await check_imei(imei)

    if response.get("status") == "successful":
        properties = response.get('properties', {})

        device_name = properties.get('deviceName', 'Нет данных')
        imei = properties.get('imei', 'Нет данных')
        meid = properties.get('meid', 'Нет данных')
        imei2 = properties.get('imei2', 'Нет данных')
        serial = properties.get('serial', 'Нет данных')
        model_desc = properties.get('modelDesc', 'Нет данных')
        purchase_country = properties.get('purchaseCountry', 'Нет данных')
        sim_lock = "Да" if properties.get('simLock') else "Нет"
        fmi_on = "Да" if properties.get('fmiOn') else "Нет"
        lost_mode = "Да" if properties.get('lostMode') else "Нет"
        image_url = properties.get('image', '')
        warrantyStatus = properties.get('warrantyStatus', 'Нет данных')

        # Формируем красивое сообщение
        result_text = f"""
        Модель устройства: {device_name}
IMEI: {imei}
MEID: {meid}
IMEI2: {imei2}
Серия: {serial}
Описание модели: {model_desc}
Гарантия: {warrantyStatus}
Страна покупки: {purchase_country}
SIM Lock: {sim_lock}
Find My iPhone: {fmi_on}
Режим потерянного устройства: {lost_mode}
{image_url}
        """
    else:
        result_text = f"Не удалось проверить IMEI. Причина: {response.get('error', 'Неизвестная ошибка')}"

    await message.answer(result_text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
