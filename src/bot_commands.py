from os import getenv

from aiogram import Router, types, F
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           CallbackQuery)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from dotenv import load_dotenv

from src.sheets import *
from src.config import get_config_texts


load_dotenv('config/.env')

# Load message texts from config file.
TEXTS = get_config_texts(
    file_path=getenv('CONFIG_PATH'),
    required_keys={
        'greeting',
        'success_initial',
        'enter_new_text',
        'success_update',
        'btn_change',
    }
)

# Main router for all commands.
router = Router()

# Update button keyboard.
keyboard_update = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text=TEXTS['btn_change'], callback_data='edit_answer')
]])


class Form(StatesGroup):
    """Bot states."""

    waiting_for_initial_text = State()
    waiting_for_edit_text = State()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    """Start the bot and wait for the initial text."""

    await message.answer(TEXTS['greeting'])
    await state.set_state(Form.waiting_for_initial_text)


@router.message(Form.waiting_for_initial_text)
async def handle_initial_text(message: types.Message, state: FSMContext):
    """Get initial text, save it and send edit-button."""

    # save_answer(message)  # Save user & text to the sheet.

    await message.answer(TEXTS['success_initial'], reply_markup=keyboard_update)
    await state.set_state(Form.waiting_for_edit_text)


@router.callback_query(F.data == "edit_answer")
async def handle_edit_button(callback: CallbackQuery, state: FSMContext):
    """Handle the "edit_answer" button and wait for the new text."""

    await callback.message.answer(TEXTS['enter_new_text'])
    await state.set_state(Form.waiting_for_edit_text)
    await callback.answer()


@router.message(Form.waiting_for_edit_text)
async def handle_edited_text(message: types.Message, state: FSMContext):
    """Update the text and send a confirmation message."""

    # save_answer(message, update=True)  # Update user & text in the sheet.

    await message.answer(TEXTS['success_update'], reply_markup=keyboard_update)
    await state.set_state(Form.waiting_for_edit_text)
