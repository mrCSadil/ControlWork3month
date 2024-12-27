from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from config import Staff
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from db import main_db





async def uses_products(message: types.Message):
    if message.from_user.id not in Staff :
        await message.answer('У тебя нет прав!')
    return True

    class products_fsm(StatesGroup):
        name = State()
        category = State()
        size = State()
        price = State()
        product_id = State()
        photo = State()
        submit = State()

    async def start_products_fsm (message: types.Message):
        await message.answer('Enter product name: ', reply_markup=buttons.cancel_markup)
        await  products_fsm.name.set()

    async def load_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text

        await products_fsm.next()
        await message.answer('Enter category name: ')

    async def load_category(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['category'] = message.text

        await products_fsm.next()
        await message.answer('Enter size: ')

    async def load_size(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['size'] = message.text

        await products_fsm.next()
        await message.answer('Enter price: ')

    async def load_price(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['price'] = message.text

        await products_fsm.next()
        await message.answer('Enter article: ')

    async def load_product_id(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['product_id'] = message.text

        await products_fsm.next()
        await message.answer('Enter photo: ')

    async def load_photo(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['photo'] = message.photo[-1].file_id

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton(text="yes"), KeyboardButton(text="no"))
            await message.answer_photo(photo=data['photo'],
                                           caption=f'Название - {data["name"]}\n'
                                                   f'Размер - {data["size"]}\n'
                                                   f'Категория - {data["category"]}\n'
                                                   f'Артикул - {data["product_id"]}\n'
                                                   f'photo - {data["photo"]}'
                                                   f'Цена - {data["price"]}\n')
            await message.answer(f"Все верно?", reply_markup=keyboard)
            await products_fsm.next()


    async def load_submit(message: types.Message, state: FSMContext):
        if message.text == 'yes':
            async with state.proxy() as data:
                await main_db.sql_insert_products(
                        name=data['name'],
                        category=data['category'],
                        size=data['size'],
                        price=data['price'],
                        product_id=data['product_id'],
                        photo=data['photo']
                    )

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


    def register_fsm_products_handlers(dp: Dispatcher):

        dp.register_message_handler(start_products_fsm, commands=['catalog'])
        dp.register_message_handler(load_name, state=products_fsm.name)
        dp.register_message_handler(load_size, state=products_fsm.size)
        dp.register_message_handler(load_category, state=products_fsm.category)
        dp.register_message_handler(load_price, state=products_fsm.price)
        dp.register_message_handler(load_photo, state=products_fsm.photo, content_types=['photo'])
        dp.register_message_handler(load_product_id, state=products_fsm.product_id)
        dp.register_message_handler(load_submit, state=products_fsm.submit)

def register_fsm_products_handlers(dp: Dispatcher):
    dp.uses_products(uses_products, command= ['catalog'])
