import asyncio
from .. import router
from .. keyboards import AuthKeyboard
from .. models import User
from aiogram import F
from aiogram.filters import Command
from aiogram.types import (
    Message,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold


class Auth(StatesGroup):
    contact: dict = State()
    wait: bool = State()
    user: User = State()


@router.message(Command("auth"))
@router.message(F.text.casefold() == "auth")
async def auth_command(message: Message, state: FSMContext) -> None:
    print(message.contact)

    await state.set_state(Auth.contact)
    await message.answer(
        f"Вітаю {hbold(message.from_user.full_name)}. Для проходження авторизації надайте свій контакт.",
        reply_markup=AuthKeyboard.keyboard,
    )


@router.message(Auth.contact,
                F.content_type == "contact",
                F.from_user.id != F.contact.user_id,)
async def wrong_contact(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"Шановний {hbold(message.from_user.full_name)}, ми отримали контакт, що Ви надіслали. Але для безпеки потрібно надати власний контакт. Спробуйте ще раз.",
        reply_markup=AuthKeyboard.keyboard,
    )
    await state.set_state(Auth.contact)


@router.message(Auth.contact,
                F.content_type == "contact",
                F.from_user.id == F.contact.user_id,)
async def contact(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"Дякую {hbold(message.from_user.full_name)}, за надані контактні дані! Зачекайте на повідомлення про успішну авторизацію"
    )
    await state.update_data(contact=message.contact.model_dump(exclude=("vcard", "first_name", "last_name")))
    await state.set_state(Auth.wait)

    # TODO: Send request to api for authorization this number
    await send_auth_request(message=message, state=state)


async def send_auth_request(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    await asyncio.sleep(10)
    contact = data.get("contact")
    user = User(id=contact.get("user_id"), phone=contact.get("phone_number"), )
    #TODO: send post request with user in body to API
     
    await state.clear()
    await message.answer(
        f"Дякую {hbold(message.from_user.full_name)}, за терпіння. Вітаємо, авторизація пройшла успішно!"
    )


@router.message(Auth.wait)
async def wait(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"Шановний {hbold(message.from_user.full_name)}, Зачекайте на повідомлення про успішну авторизацію.",
    )
