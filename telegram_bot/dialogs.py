from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.api.entities import StartMode
from aiogram import types
from aiogram_dialog.dialog import DialogManager
import aiohttp
import os

API_URL = os.environ.get('API_URL', 'http://web:8000/api')

async def get_tasks_http(user_id: int) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/tasks/my_tasks/?user_id={user_id}") as response:
            if response.status == 200:
                return await response.json()
            return []

async def create_task_http(data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/tasks/", json=data) as response:
            if response.status == 201:
                return await response.json()
            return {}

async def start_handler(event: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuStates.MENU, mode=StartMode.RESET_STACK)

async def my_tasks_handler(event: types.Message, dialog_manager: DialogManager):
    user_id = event.from_user.id
    tasks = await get_tasks_http(user_id)
    if tasks:
        tasks_text = []
        for task in tasks:
            category_name = task.get('category_name', 'Без категории')
            created_at = task.get('created_at', 'Нет даты')
            status = "✓" if task.get('is_completed') else "○"
            tasks_text.append(f"{status} {task['title']} [{category_name}] (Создано: {created_at})")
        text = "📋 Ваши задачи:\n\n" + "\n".join(tasks_text)
    else:
        text = "📋 У вас пока нет задач."
    await event.answer(text)

async def add_task_start_handler(event: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddTaskStates.TITLE, mode=StartMode.RESET_STACK)

async def title_processing(event: types.Message, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['title'] = text
    await dialog_manager.next()

async def description_processing(event: types.Message, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['description'] = text
    await dialog_manager.next()

async def category_processing(event: types.Message, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['category_name'] = text
    await dialog_manager.next()

async def due_date_processing(event: types.Message, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['due_date'] = text
    await dialog_manager.next()

async def confirm_task_handler(event: types.CallbackQuery, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    task_data = {
        'user_id': event.from_user.id,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'due_date': data.get('due_date', None),
        'category': data.get('category_name', None)
    }
    result = await create_task_http(task_data)
    if result:
        await event.message.answer("✅ Задача успешно создана!")
    else:
        await event.message.answer("❌ Ошибка при создании задачи.")
    await dialog_manager.start(MainMenuStates.MENU, mode=StartMode.RESET_STACK)

class MainMenuStates:
    MENU = 0

class AddTaskStates:
    TITLE = 0
    DESCRIPTION = 1
    CATEGORY = 2
    DUE_DATE = 3
    CONFIRM = 4

main_menu_dialog = Dialog(
    Window(
        Const("📝 ToDo List Bot\n\nВыберите действие:"),
        Row(
            Button(Const("📋 Мои задачи"), id="my_tasks", on_click=my_tasks_handler),
            Button(Const("➕ Добавить задачу"), id="add_task", on_click=add_task_start_handler),
        ),
        state=MainMenuStates.MENU,
    ),
)

add_task_dialog = Dialog(
    Window(
        Const("📝 Добавление задачи\n\nВведите название задачи:"),
        TextInput(id="title_input", on_process=title_processing),
        state=AddTaskStates.TITLE,
    ),
    Window(
        Const("📝 Добавление задачи\n\nВведите описание задачи (или нажмите /skip для пропуска):"),
        TextInput(id="description_input", on_process=description_processing),
        state=AddTaskStates.DESCRIPTION,
    ),
    Window(
        Const("📝 Добавление задачи\n\nВведите категорию (или нажмите /skip для пропуска):"),
        TextInput(id="category_input", on_process=category_processing),
        state=AddTaskStates.CATEGORY,
    ),
    Window(
        Const("📝 Добавление задачи\n\nВведите дату выполнения в формате ГГГГ-ММ-ДД ЧЧ:ММ (или нажмите /skip для пропуска):"),
        TextInput(id="due_date_input", on_process=due_date_processing),
        state=AddTaskStates.DUE_DATE,
    ),
    Window(
        Format("Подтвердите создание задачи:\n\n📌 {dialog_data[title]}\n📝 {dialog_data[description]}\n🏷️ {dialog_data[category_name]}\n📅 {dialog_data[due_date]}"),
        Row(
            Button(Const("✅ Создать"), id="confirm", on_click=confirm_task_handler),
            Button(Const("❌ Отмена"), id="cancel"),
        ),
        state=AddTaskStates.CONFIRM,
    ),
)