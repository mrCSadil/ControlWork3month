from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from db import main_db
from config import Staff, bot


class client_fsm(StatesGroup):
    product_id = State()
    size = State()
    quantity = State()
    number = State()
    submit = State()

async def start_client_fsm (message: types.Message):
    await message.answer('Enter product article: ',
                         reply_markup=buttons.cancel_markup)
    await  client_fsm.product_id.set()

async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await client_fsm.next()
    await message.answer('Enter size: ')

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await client_fsm.next()
    await message.answer('Enter your quantity: ')

async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await client_fsm.next()
    await message.answer('Enter your personal number: ')

async def load_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="yes"), KeyboardButton(text="no"))

    await message.answer_photo(photo=data['photo'],
                               caption=f'Артикул - {data["product_id"]}\n'
                                       f'Размер - {data["size"]}\n'
                                       f'Количество - {data["quantity"]}\n'
                                       f'Personal number - {data["number"]}\n')
    await message.answer(f"Все верно?", reply_markup=keyboard)
    await client_fsm.next()

async def load_submit(message: types.Message, state: FSMContext):
    if message.text == 'yes':
        async with state.proxy() as data:
            await main_db.sql_insert_client(
                product_id=data['product_id'],
                size=data['size'],
                quantity=data['quantity'],
                number=data['number']
            )
            clients = main_db.sql_get_all_clients()

            if message.from_user.id in Staff :
                for client in clients:
                    caption = (f'Артикул - {client["product_id"]}\n'
                                f'quantity - {client["quantity"]}\n'
                                f'size - {client["size"]}\n'
                                f'number - {client["number"]}\n'
                                )

                await bot.send_message(caption=caption)

    elif message.text.lower().strip() == 'no':
        await message.answer('It was cancelled.', reply_markup=buttons.start_markup)
        await state.finish()

    else:
        await message.answer('enter yes or no')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()
        await message.answer('Have been cancelled!', reply_markup=buttons.start_markup)


def register_fsm_client_handlers(dp: Dispatcher):
    dp.register_message_handler(start_client_fsm, commands=["buy"])
    dp.register_message_handler(load_product_id, state=client_fsm.product_id)
    dp.register_message_handler(load_size, state=client_fsm.size)
    dp.register_message_handler(load_quantity, state=client_fsm.quantity)
    dp.register_message_handler(load_number, state=client_fsm.number)
    dp.register_message_handler(load_submit, state=client_fsm.submit)