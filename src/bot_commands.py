from os import getenv
from datetime import datetime

from aiogram import Router, types, F
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           CallbackQuery)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from dotenv import load_dotenv

from src.sheets import SheetAccount
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
        'btn_submit',
        'btn_emoji1',
        'btn_emoji2',
    },
)

# Inits.
router = Router()
sheet_account = SheetAccount()

# Keyboards
kb_edit = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text=TEXTS['btn_submit'], callback_data='btn_submit'),
    InlineKeyboardButton(text=TEXTS['btn_edit'], callback_data='btn_edit'),
]])
kb_stickers = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=TEXTS['btn_emoji1'], url=TEXTS['url_emoji1'])],
    [InlineKeyboardButton(text=TEXTS['btn_emoji2'], url=TEXTS['url_emoji2'])],
])


class Form(StatesGroup):
    """Bot states."""

    waiting_for_draft = State()
    waiting_for_decision = State()
    done = State()


@router.callback_query(Form.done)
@router.message(Form.done)
async def handle_done(event: types.Message | CallbackQuery):
    """Handle any action after the algorithm is completed."""

    if isinstance(event, CallbackQuery):
        await event.message.answer(TEXTS['handle_done'], parse_mode=PARSE_MODE)
        await event.answer()
    else:
        await event.answer(TEXTS['handle_done'], parse_mode=PARSE_MODE)



@router.message(Command('start'))
async def handle_start(message: types.Message, state: FSMContext):
    """Start the bot and wait for the initial text."""

    await message.answer(TEXTS['handle_start'], parse_mode=PARSE_MODE)
    await state.set_state(Form.waiting_for_draft)


@router.message(Form.waiting_for_draft)
async def handle_draft(message: types.Message, state: FSMContext):
    """Get draft text, wait for the decision to edit or send."""

    await state.update_data(text=message.text)
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

    # Save answer in the sheet.
    data = await state.get_data()
    sheet_account.save_answer(
        time=datetime.now(),
        user_id=callback.from_user.id,
        user_name=callback.from_user.username or '-',
        text=data.get('text')
    )

    await callback.message.answer(TEXTS['handle_submit'], parse_mode=PARSE_MODE,
                                  reply_markup=kb_stickers)
    await state.set_state(Form.done)
    await callback.answer()
