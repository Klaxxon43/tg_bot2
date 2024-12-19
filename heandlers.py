from aiogram import F, Router, Dispatcher, Bot, types
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import app.database.requests as rq
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest
from app.keyboards import mainadmin, adminpanel, adminpanel2, mail_and_code

router = Router()
adminid =5129878568
chat_id=-1002449672567
class Register(StatesGroup):
    name = State()
    age = State()
    number = State()
    id = State()
    writeuserid = State()
    sms = State()
    tovar = State()
    price = State()

class Pokupka(StatesGroup):
    tovar = State()
    price = State()
    mail = State()
    code = State()
    id = State()

bot=Bot(token='TOKEN')


@router.message(Command('writeuser'))
async def writeuser(message: Message, state: FSMContext):
    await state.set_state(Register.writeuserid)
    await message.answer("✍️Напишите ID пользователя, которому хотите отправить")
    

@router.message(Register.writeuserid)
async def writeuserid(message: Message, state: FSMContext):
    await state.update_data(writeuserid=message.text)
    await state.set_state(Register.sms)
    await message.answer("ID получен👌\n📨Отправь сообщение, которое хочешь ему передать")

@router.message(Register.sms)  
async def sms(message: Message, state: FSMContext):
    await state.update_data(sms=message.text)
    data = await state.get_data()
    await bot.send_message(chat_id=data['writeuserid'],  text=f'Получено новое сообщение от админа: \n {data['sms']}')
    await message.answer('📬Сообщение отправлено')
    state.clear()

@router.message(F.text=='✏️Написать админу')
async def write_to_admin(message: Message):
    await message.answer("❗️Чтобы написать сообщение админу, напишите /write и текст после него, например: </write привет админ>❗️")

@router.message(Command('write'))
async def a(message: Message, command: CommandObject):
    if command.args!=None:
        await bot.send_message(chat_id=chat_id, text=f'📨Сообщение от пользователя: @{message.from_user.username}:\n{command.args}')
    else:
        await message.answer('❌Ошибка. После /write введите сообщение, которое хотите, чтобы полиучил админ❌')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAICs2dcLdnZe_-bUmKMJ1v0IP33Jt29AAL4RQACnHwZS-JD6jzjSEk6NgQ')
    if message.chat.id==adminid:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин игровых ресурсов, админ!👋', reply_markup=kb.mainadmin)
    else:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин игровых ресурсов!👋', reply_markup=kb.main)
    print(message.chat.id)

@router.message(F.text=='👤Админ панель')
async def adminpanel(message: Message):
    if message.from_user.id==adminid:
        await message.answer('Ваш админ панель: ', reply_markup=await kb.adminpanel())
        await message.answer("", reply_markup=kb.adminpanel2)        
    else:
        await message.answer('Чо ахуел, ты не админ')

@router.callback_query(F.data.startswith('main'))
async def main(callback: CallbackQuery):
    await callback.message.answer("Меню: ", reply_markup= kb.main)
    

@router.callback_query(F.data.startswith('banned'))
async def banned(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.id)
    await callback.message.answer('Введите айди игрока, которого хотите забанить')
   
@router.message(Register.id)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await state.set_state(Register.id)
    data = await state.get_data()
    await message.answer(f"id: {data['id']}")
    await rq.set_banned(data['id'])
    
@router.message(Command('myid'))
async def mtid(message: Message):
    id = message.from_user.id
    print(id)

#ПОЛУЧЕНИЕ АЙДИ СТИКЕРА
#@router.message()
#async def stiker(message: types.Message):
#    await message.answer(message.sticker.file_id)
#    await message.answer(message.from_user.id, message.chat.id)

@router.message(F.text == '📦Каталог')
async def catalog(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAICuGdcLmGC9AbYYIZmYL0aIN50VjwYAAJnQwACT17gS-nRkuwlhtfYNgQ')
    await message.answer('Выберите категорию товара', reply_markup= await kb.categories())

@router.message(Command('spisok'))
async def spisok_bunned_users(message: Message):
    await message.answer(' Список:', reply_markup= kb.banned_userss)

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.message.answer_sticker('CAACAgIAAxkBAAICyGdcLzFxkMWd_VGWiq37sLzR7IeJAALkVQACAn_xSWQ_cl7oQsmRNgQ')
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))
    
# @router.callback_query(F.data.startswith('bunned_users_spisok'))
# async def category(callback: CallbackQuery):
#     await callback.message.answer_sticker('CAACAgIAAxkBAAICyGdcLzFxkMWd_VGWiq37sLzR7IeJAALkVQACAn_xSWQ_cl7oQsmRNgQ')
#     #await callback.message.answer('fksf')

    # await callback.message.answer(' Список:', reply_markup= await kb.banned_userss())


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery, state: FSMContext):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await state.set_state(Pokupka.price)
    await state.update_data(price=item_data.price)
    await state.set_state(Pokupka.tovar)
    await state.update_data(tovar=item_data.name)
    await callback.message.answer_sticker('CAACAgIAAxkBAAIC92dcM7wAAQSu93-kXeP0vDpM0VahPwACIkAAAolaKEoOwXCx8eIH_zYE')
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}руб', reply_markup=kb.buy)

@router.callback_query(F.data.startswith('buy_brawl_pass'))
async def category(callback: CallbackQuery):
    await callback.message.answer('Отлично, я рад, что вы решили у нас что то приобрести! \n Теперь вам нужно оплатить товар. Сделать это просто, просто отправьте деньги на один из реквизитов: \n 1. СберБанк: `2202208082846990` \n 2. СПБ: `+79960460076`\n Данные верные, уточнять их правильность не требуется\nПосле оплаты нажмите на кнопку.', reply_markup=kb.proverka_pokupki)

@router.message(F.text=='Проверка оплаты')
async def proverkaoplatitovara(message: Message, state: FSMContext):
    await message.answer('✅Отлично, теперь, если вы действительно оплатили, то нажмите на /mail и введите данные от аккааунта для выполнения вашего заказа! После этого, он проверит поступление оплаты и начнёт выполнение заказа', reply_markup=kb.main)


@router.message(Command('mail'))
async def mail(message: Message,  state:FSMContext):
    await state.set_state(Pokupka.mail)
    await message.answer('✏️Теперь введи тут свою почту от аккаунта')

@router.message(Command('code'))
async def idpokupatelya(message: Message, state: FSMContext):
    if message.from_user.id==adminid:
        await state.set_state(Pokupka.id)
        await message.answer('✏️Введи айди пользователя, у которого хочешь узнать код')

@router.message(Pokupka.id)
async def code(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await state.set_state(Pokupka.code)
    data = await state.get_data()
    await message.answer(f'✅Пользователю отправлен запрос на получение кода, {data['id']}')
    await bot.send_message(chat_id=data['id'], text='✅Админ приступил к выполнению вашего заказа! \nНа вашу почту должен был прийти код, вернитесь в главное меню, нажмите <написать админу> и напишите код, который вы получили✏️', reply_markup= kb.main)
    

@router.message(Pokupka.mail)
async def mailupdate(message: Message, state: FSMContext):
    await state.update_data(mail=message.text)
    data = await state.get_data()
    await message.answer('✅Почта получена! \n Теперь когда админ начнёт выполнение заказа, он попросит у вас код')
    await bot.send_message(chat_id=chat_id, text=f'💸Новая покупка! \nПользователь: @{message.from_user.username}\nЕго ID: {message.from_user.id}\nТовар: {data['tovar']}\nЦена: {data['price']}. \nПочта: {data['mail']} \nПроверьте получение оплаты и выполните заказ!')



@router.message(F.text=='⚜️Контакты')
async def contacts(message: Message):

    await message.answer("⚜️Ссылка на админа и на его канал:", reply_markup=kb.admin)






#ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ ДОНАТ

@router.message(Command("donate", "donat", "донат")or F.text=='donate')
async def cmd_donate(message: Message, command: CommandObject):
    if command.args is None or not command.args.isdigit() or not 1 <= int(command.args) <= 2500:
        await message.answer('💸Пожалуйста, введите сумму в формате /donate [ЧИСЛО], где [ЧИСЛО] это сумма доната от ⭐️ 1 до ⭐️ 2500.')
        return

    # сумма доната
    amount = int(command.args)
    prices = [LabeledPrice(label="XTR", amount=amount)]

    await message.answer_invoice(
        title=("Донат автору"),
        description=('На сумму х звёзд'),
        prices=prices,

        provider_token="",

        payload=f"{amount}_stars",

        # XTR - это код валюты Telegram Stars
        currency="XTR",
    )


@router.message(Command("refund"))
async def cmd_refund(message: Message, bot: Bot, command: CommandObject):
    t_id = command.args

    # чекаем, указан ли ID транзакции
    if t_id is None:
        await message.answer(" Пожалуйста, укажите идентификатор транзакции в формате /refund [id], где [id] это идентификатор транзакции, который вы получили после доната.")
        return

    # пытаемся сделать рефанд
    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=t_id
        )
        await message.answer("Рефанд произведен успешно. Потраченные звёзды уже вернулись на ваш счёт в Telegram.")

    except TelegramBadRequest as e:
        err_text = ("Транзакция с указанным идентификатором не найдена. Пожалуйста, проверьте введенные данные и повторите ещё раз.")

        if "CHARGE_ALREADY_REFUNDED" in e.message:
            err_text = ("Рефанд по этой транзакции уже был ранее произведен.")

        await message.answer(err_text)
        return


@router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)



@router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)



@router.message(F.successful_payment)
async def on_successfull_payment(message: Message):
    await message.answer(
  
            "<b>🫡 Спасибо!</b>/nВаш донат успешно принят.",
            {"t_id": message.successful_payment.telegram_payment_charge_id}
        ),



