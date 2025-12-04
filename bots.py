import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

# Конфигурация бота
TOKEN = "8306643748:AAGiesFvOXu_B7j__CPtflvtiY8oqb4XW2U"
ADMIN_ID = 1837848100

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Определение состояний бота
class Form(StatesGroup):
    """Класс состояний для обработки заявки на справку"""
    fio = State()
    klass = State()
    type_spravki = State()
    comment = State()


@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start
    Выводит приветственное сообщение и очищает состояние
    """
    await message.answer(
        "Здравствуйте! Это бот школы №7.\n"
        "Нажмите /spravka чтобы заказать справку."
    )
    await state.clear()


@dp.message(Command("spravka"))
async def spravka_command(message: types.Message, state: FSMContext):
    """
    Обработчик команды /spravka
    Начинает процесс оформления заявки на справку
    """
    await message.answer("Введите ФИО ученика:")
    await state.set_state(Form.fio)


@dp.message(Form.fio)
async def process_fio(message: types.Message, state: FSMContext):
    """
    Обработчик ввода ФИО
    Сохраняет ФИО и запрашивает класс
    """
    await state.update_data(fio=message.text)
    await message.answer("Введите класс (например: 6Б):")
    await state.set_state(Form.klass)


@dp.message(Form.klass)
async def process_klass(message: types.Message, state: FSMContext):
    """
    Обработчик ввода класса
    Сохраняет класс и запрашивает тип справки
    """
    await state.update_data(klass=message.text)
    await message.answer("Введите тип справки:")
    await state.set_state(Form.type_spravki)


@dp.message(Form.type_spravki)
async def process_type_spravki(message: types.Message, state: FSMContext):
    """
    Обработчик ввода типа справки
    Сохраняет тип справки и запрашивает комментарий
    """
    await state.update_data(type_spravki=message.text)
    await message.answer("Добавьте комментарий (или напишите: нет):")
    await state.set_state(Form.comment)


@dp.message(Form.comment)
async def process_comment(message: types.Message, state: FSMContext):
    """
    Обработчик ввода комментария
    Формирует и отправляет заявку администратору
    """
    # Сохраняем комментарий
    await state.update_data(comment=message.text)
    
    # Получаем все данные из состояния
    data = await state.get_data()
    
    # Формируем текст заявки
    text = (
        "📄 *Новая заявка на справку*\n\n"
        f"👤 ФИО: *{data['fio']}*\n"
        f"🏫 Класс: *{data['klass']}*\n"
        f"📘 Тип справки: *{data['type_spravki']}*\n"
        f"💬 Комментарий: {data['comment']}"
    )
    
    # Отправляем заявку администратору
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="Markdown"
    )
    
    # Подтверждаем пользователю
    await message.answer(
        "✅ Заявка отправлена! Ожидайте ответа.",
        parse_mode="Markdown"
    )
    
    # Очищаем состояние
    await state.clear()


async def main():
    """
    Основная функция запуска бота
    """
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    """
    Точка входа в приложение
    """
    asyncio.run(main())
