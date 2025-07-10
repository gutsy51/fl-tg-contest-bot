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
PARSE_MODE = 'HTML'
TEXTS = get_config_texts(
    file_path=getenv('CONFIG_PATH'),
    required_keys={
        'handle_start',
        'handle_draft',
        'handle_edit',
        'handle_submit',
        'btn_edit',
        'btn_submit'
    }
)

# Main router for all commands.
router = Router()

# 'Submit' or 'Edit' keyboard.
kb_edit = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text=TEXTS['btn_submit'], callback_data='btn_submit'),
    InlineKeyboardButton(text=TEXTS['btn_edit'], callback_data='btn_edit'),
]])


class Form(StatesGroup):
    """Bot states."""

    waiting_for_draft = State()
    waiting_for_decision = State()


@router.message(Command('start'))
async def handle_start(message: types.Message, state: FSMContext):
    """Start the bot and wait for the initial text."""

    await message.answer(TEXTS['handle_start'], parse_mode=PARSE_MODE)
    await state.set_state(Form.waiting_for_draft)


@router.message(Form.waiting_for_draft)
async def handle_draft(message: types.Message, state: FSMContext):
    """Get draft text, wait for the decision to edit or send."""

    await message.answer(TEXTS['handle_draft'],
                         parse_mode=PARSE_MODE,
                         reply_markup=kb_edit)
    await state.set_state(Form.waiting_for_decision)


@router.callback_query(F.data == 'btn_edit')
async def handle_edit(callback: CallbackQuery, state: FSMContext):
    """Handle the 'btn_edit' button and wait for the new text."""

    await callback.message.answer(TEXTS['handle_edit'], parse_mode=PARSE_MODE)
    await state.set_state(Form.waiting_for_draft)
    await callback.answer()


@router.callback_query(F.data == 'btn_submit')
async def handle_submit(callback: CallbackQuery, state: FSMContext):
    """Handle the 'btn_submit' button and save the text."""

    # save_answer(message)  # Save user & text in the sheet.

    await callback.message.answer(TEXTS['handle_submit'], parse_mode=PARSE_MODE)
    await callback.answer()
