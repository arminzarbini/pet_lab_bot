import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardRemove
from DML import *
from DQL import *
from config import *
from text import *
import re


bot = telebot.TeleBot(BOT_TOKEN)
hideboard = ReplyKeyboardRemove()
user_steps = dict() # {cid, step,...}
test = dict() # {test_group_id : ... , parameter : ..., type : ... , price : ... , unit : ..., minimum_range : ... , maximum_range : ... , analyze_date : ..., description : ...}
member_user_cid = list() #[cid, ...]


def get_member_user():
    member_user = show_member_user_cid()
    for user in member_user:
        member_user_cid.append(user['cid'])


def get_user_step(cid):
    return user_steps.setdefault(cid, 0)

def send_home():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons['home'])
        return markup


def is_valid(phone):
	Pattern = re.compile("^(0|0098|\+98)?9\d{9}$") #start - group(0 or 0098 or +98) - 9 - exactly 9 digits - end
	return Pattern.match(phone)


get_member_user()

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    call_id = call.id
    data = call.data
    if cid in admins:
        if data.startswith('test_group'):
            test_group_id = int(data.split('_')[-1])
            test.setdefault('test_group_id', test_group_id)
            bot.answer_callback_query(call_id, '✅')
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            markup = send_home()
            bot.send_message(cid, text_admin['template_test'], reply_markup=markup)
            bot.send_message(cid, text_admin['template_input_test'])
            user_steps[cid] = 2
    else:
        if data.startswith('first_name'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['first_name_edit'])
            user_steps[cid] = 10
        elif data.startswith('last_name'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['last_name_edit'])
            user_steps[cid] = 11
        elif data.startswith('username'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['username_edit'])
            user_steps[cid] = 12
        elif data.startswith('national_code'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['national_code_edit'])
            user_steps[cid] = 13
        elif data.startswith('phone'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['phone_edit'])
            user_steps[cid] = 14
        elif data.startswith('address'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['address_edit'])
            user_steps[cid] = 15


@bot.message_handler(commands=['start'])
def start_command(message):
    cid = message.chat.id
    if cid in admins :
        bot.send_message(cid, text['welcome'])
        home_command(message)
    else : 
        bot.send_message(cid, text['welcome'])
        home_command(message)
        if cid not in member_user_cid:
            first_name = message.chat.first_name
            if message.chat.last_name == None:
                last_name = None
            else:
                last_name = message.chat.last_name
            if message.chat.username == None:
                username = None
            else:
                username = message.chat.username
                insert_user_data(cid=cid, first_name=first_name, last_name=last_name, username=username, national_code=None, phone=None, address=None)
                member_user_cid.append(cid)
        else:
            pass
  

@bot.message_handler(commands=['home'])
def home_command(message):
    cid = message.chat.id
    if cid in admins:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_admin['create_test'], buttons_admin['create_test_group'])
        markup.add(buttons_admin['create_species'])
        bot.send_message(cid, text['home'], reply_markup=markup)
        user_steps[cid] = 0
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_user['account'])
        bot.send_message(cid, text['home'], reply_markup=markup)
        user_steps[cid] = 0


@bot.message_handler(func=lambda message: message.text==buttons['home'])
def home_handler(message):
    cid = message.chat.id
    if cid in admins:
        home_command(message)
    else:
        home_command(message)


@bot.message_handler(func=lambda message: message.text==buttons_user['account'])
def account_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = InlineKeyboardMarkup()
        user_data = show_user_data(cid)
        for user in user_data:
            if user['cid'] == cid:
                markup.add(InlineKeyboardButton(f"{text_user['first_name']} : {user['first_name']}", callback_data=f"first_name : {user['first_name']}"))
                markup.add(InlineKeyboardButton(f"{text_user['last_name']} : {user['last_name']}", callback_data=f"last_name : {user['last_name']}"))
                markup.add(InlineKeyboardButton(f"{text_user['username']} : {user['username']}", callback_data=f"username : {user['username']}"))
                markup.add(InlineKeyboardButton(f"{text_user['national_code']} : {user['national_code']}", callback_data=f"national_code : {user['national_code']}"))
                markup.add(InlineKeyboardButton(f"{text_user['phone']} : {user['phone']}", callback_data=f"phone : {user['phone']}"))
                markup.add(InlineKeyboardButton(f"{text_user['address']} : {user['address']}", callback_data=f"address : {user['address']}"))
                bot.send_message(cid, text_user['user_data'], reply_markup=markup)
                bot.send_message(cid, text_user['user_data_edit'])
    user_steps[cid] = 1

@bot.message_handler(func=lambda message: message.text==buttons_admin['create_test_group'])
def create_test_group_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = send_home()
        bot.send_message(cid, text_admin['name_test_group_input'], reply_markup=markup)
        user_steps[cid] = 1
    else :
        unknown_message()


@bot.message_handler(func=lambda message: message.text==buttons_admin['create_test'])
def create_test_handler(message):
    cid = message.chat.id
    if cid in admins:
        test_group = show_test_group()
        if not test_group:
            markup = send_home()
            bot.send_message(cid, text_admin['test_group_not'] ,reply_markup=markup)
        else :
            markup = InlineKeyboardMarkup()
            for group in test_group:
                markup.add(InlineKeyboardButton(group['name'], callback_data=f"test_group_{group['id']}"))
            bot.send_message(cid, text_admin['chooce_test_group'], reply_markup=markup)
    else :
        unknown_message(message)

@bot.message_handler(func=lambda message:message.text==buttons_admin['create_species'])
def create_species_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = send_home()
        bot.send_message(cid, text_admin['name_species_input'], reply_markup=markup)
        user_steps[cid] = 3


@bot.message_handler(func=lambda message : get_user_step(message.chat.id)==1)
def group_test_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        exist_test_group = show_test_group()
        exist_test_group_name = list() #list test group name for unique check
        for item in exist_test_group:
            exist_test_group_name.append(item['name'])
        if name in exist_test_group_name:
            bot.send_message(cid, text_admin['name_test_group_unique'])
        elif len(name) > 45:
            bot.send_message(cid, text_admin['name_test_group_check'])
        else:
            insert_test_group_data(name=name)
            bot.send_message(cid, text_admin['success_create_test_group'].format(name))
            user_steps[cid] = 0
            home_command(message)
    else:
        bot.send_message(cid, text_user['user_data_edit'])



@bot.message_handler(func=lambda message: get_user_step(message.chat.id)==2)
def test_handler(message):
    cid = message.chat.id
    if cid in admins:
        item_test_check = ['parameter', 'type', 'price', 'unit', 'minimum_range', 'maximum_range', 'analyze_date', 'description']
        item_test = message.text.split('\n')
        item_check = dict()
        item_title = list()
        for item in item_test :
            item_check.setdefault(item.split(':')[0],  item.split(':')[-1])
            item_title.append(item.split(':')[0])
        if len(item_test_check) != len(item_title):
            bot.send_message(cid, text_admin['send_full_test_item'])
        elif item_test_check != item_title:
            bot.send_message(cid, text_admin['test_item_check'])
        else:
            for key,value in item_check.items():  
                if key == 'parameter':
                    parameter = value
                    exist_test = show_test_parameter()
                    exist_test_parameter = list()
                    for item in exist_test:
                            exist_test_parameter.append(item['parameter'])
                    if parameter == "":
                        bot.send_message(cid, text_admin['parameter_test_null'])
                    else :
                        if parameter in exist_test_parameter:
                            bot.send_message(cid, text_admin['parameter_test_unique'])
                        elif len(parameter) > 45:
                            bot.send_message(cid, text_admin['parameter_test_check'])
                        else :
                            test.setdefault(key, parameter)
                elif key == 'type':
                    type = value
                    if type == "":
                        bot.send_message(cid, text_admin['type_test_null'])
                    else:
                        if type == 'quality' or type == 'quantity':
                            test.setdefault(key, type)
                        else : 
                            bot.send_message(cid, text_admin['type_test_check'])
                elif key == 'price':
                    price = value
                    if price == "":
                        bot.send_message(cid, text_admin['price_test_null'])
                    else:
                        try:
                            price = float(price)
                        except:
                            bot.send_message(cid, text_admin['price_test_check'])
                        else:
                            if len(str(price).split('.')[1]) > 10 or len(str(price).split('.')[-1]) > 2 :
                                bot.send_message(cid, text_admin['price_test_check'])
                            else:
                                test.setdefault(key, price)
                elif key == 'unit':
                    unit = value
                    if unit == "":
                        test.setdefault(key, None)
                    elif len(unit) > 10:
                        bot.send_message(cid, text_admin['unit_test_check'])
                    else:
                        test.setdefault(key, unit)
                elif key == 'minimum_range':
                    minimum_range = value
                    if minimum_range == "":
                        test.setdefault(key, None)
                    else:
                        try:
                            minimum_range = float(minimum_range)
                        except:
                            bot.send_message(cid, text_admin['minimum_range_test_check'])
                        else:
                            if len(str(minimum_range).split('.')[1]) > 5 or len(str(minimum_range).split('.')[-1]) > 3 :
                                bot.send_message(cid, text_admin['minimum_range_test_check'])
                            else:
                                test.setdefault(key, minimum_range)
                elif key == 'maximum_range':
                    maximum_range = value
                    if maximum_range == "":
                        test.setdefault(key, None)
                    else:
                        try:
                            maximum_range = float(maximum_range)
                        except:
                            bot.send_message(cid, text_admin['maximum_range_test_check'])
                        else:
                            if len(str(maximum_range).split('.')[1]) > 5 or len(str(maximum_range).split('.')[-1]) > 3 :
                                bot.send_message(cid, text_admin['maximum_range_test_check'])
                            else:
                                test.setdefault(key, maximum_range)
                elif key == 'analyze_date':
                    analyze_date = value
                    if analyze_date == "":
                        test.setdefault(key, None)
                    else:
                        try:
                            analyze_date = int(analyze_date)
                        except:
                            bot.send_message(cid, text_admin['analyze_date_test_check'])
                        else :
                            if 1 <= analyze_date <= 30:
                                test.setdefault(key, analyze_date)
                            else :
                                bot.send_message(cid, text_admin['analyze_date_test_check'])
                elif key == 'description':
                    description = value
                    if description == "":
                        test.setdefault(key, None)
                    elif len(description) > 255:
                        bot.send_message(cid, text_admin['description_test_check'])
                    else:
                        test.setdefault(key, description)

        if len(test) == 9:
            insert_test_data(**test)
            bot.send_message(cid, text_admin['success_create_test'].format(test['parameter']))
            user_steps[cid] = 0
            test.clear()
            home_command(message)

    else:
        unknown_message(message)

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3)
def species_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        exist_species = show_species()
        exist_species_name = list() #list species name for unique check
        for item in exist_species:
            exist_species_name.append(item['name'])
        if name in exist_species_name:
            bot.send_message(cid, text_admin['name_species_unique'])
        elif len(name) > 45:
            bot.send_message(cid,text_admin['name_species_check'])
        else:
            insert_species_data(name=name)
            bot.send_message(cid, text_admin['success_create_species'].format(name))
            user_steps[cid] = 0
            home_command(message)

    else:
        unknown_message(message)

    

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10)
def first_name_edit_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        first_name = message.text
        if len(first_name) > 64:
            bot.send_message(cid, text_user['first_name_check'])
        else:
            edit_user_first_name(first_name=first_name, cid=cid)
            bot.send_message(cid, text_user['first_name_success'], reply_markup=markup)
            account_handler(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11)
def last_name_edit_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        last_name = message.text
        if len(last_name) > 64:
            bot.send_message(cid, text_user['last_name_check'])
        else:
            edit_user_last_name(last_name=last_name, cid=cid)
            bot.send_message(cid, text_user['last_name_success'], reply_markup=markup)
            account_handler(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==12)
def username_edit_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        username = message.text
        exist_user = show_user_username()
        exist_user_username = list()
        for item in exist_user:
            exist_user_username.append(item['username'])
        english_flag = True
        for char in username:
            char_value = ord(char)
            if (char_value >= 33 and char_value <= 126):
                continue
            else:
                english_flag = False
                break
        if english_flag == True:
            if username in exist_user_username:
                bot.send_message(cid, text_user['username_unique'])
            elif len(username) > 32:
                bot.send_message(cid, text.user['username_check'])
            else:
                edit_user_username(username=username, cid=cid)
                bot.send_message(cid, text_user['username_success'], reply_markup=markup)
                account_handler(message)
        else:
            bot.send_message(cid, text_user['username_english'])


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==13)
def national_code_edit(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        national_code = message.text
        if len(national_code) != 10:
            bot.send_message(cid, text_user['national_code_check'])
        elif national_code.isnumeric() == False:
            bot.send_message(cid, text_user['national_code_check'])
        else:
            edit_user_national_code(national_code=national_code, cid=cid)
            bot.send_message(cid, text_user['national_code_success'], reply_markup=markup)
            account_handler(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==14)
def phone_edit(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        phone = message.text
        if is_valid(phone):
            edit_phone(phone=phone, cid=cid)
            bot.send_message(cid, text_user['phone_success'])
            account_handler(message)
        else :
            bot.send_message(cid, text_user['phone_check'], reply_markup=markup)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==15)
def address_edit(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        address = message.text
        if len(address) > 255:
            bot.send_message(cid, text_user['address_check'])
        else:
            edit_address(address=address, cid=cid)
            bot.send_message(cid, text_user['address_success'], reply_markup=markup)
            account_handler(message)


@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    cid = message.chat.id
    bot.send_message(cid, text['unknown_message'])


bot.infinity_polling()