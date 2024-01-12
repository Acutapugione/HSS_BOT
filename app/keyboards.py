from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


class KeyboardGenerator:

    reply = ReplyKeyboardBuilder
    inline = InlineKeyboardBuilder


class AuthKeyboard(KeyboardGenerator):

    @classmethod
    @property
    def keyboard(cls):
        builder = cls.reply()
        builder.button(text="Поділитись контактом", request_contact=True)
        return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)