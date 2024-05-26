import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardRemove
from DML import *
from DQL import *
from config import *
from text import *
import re


bot = telebot.TeleBot(BOT_TOKEN, num_threads=10)
hideboard = ReplyKeyboardRemove()
users = list() #[cid, ...]
user_steps = dict() # {cid, step,...}
test = dict() # {test_group_id : ... , parameter : ..., type : ... , price : ... , unit : ..., minimum_range : ... , maximum_range : ... , analyze_date : ..., description : ...}
breed = dict() # {species : ..., name : ..., specifications : ...}
user_pets = dict() #{breed_id : ..., name : ...}


def get_member_user():
    member_user = show_member_user()
    return member_user


def get_user_step(cid):
    return user_steps.setdefault(cid, 0)

def send_home():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons['home'])
        return markup


def is_valid(phone):
	Pattern = re.compile("^(0|0098|\+98)?9\d{9}$") #start - group(0 or 0098 or +98) - 9 - exactly 9 digits - end
	return Pattern.match(phone)



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    call_id = call.id
    data = call.data
    if cid in admins:
        if data.startswith('test_group'):
            test_group_id = int(data.split('_')[-1])
            test.update({'test_group_id': test_group_id})
            bot.answer_callback_query(call_id, '✅')
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            markup = send_home()
            bot.send_message(cid, text_admin['template_test'], reply_markup=markup)
            bot.send_message(cid, text_admin['template_input_test'])
            user_steps[cid] = 2
        elif data in species:
            breed.update({'species': data})
            bot.answer_callback_query(call_id, '✅')
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            markup = send_home()
            bot.send_message(cid, text_admin['name_breed_input'], reply_markup=markup)
            user_steps[cid] = 3
        elif data == 'no_specifications_breed':
            insert_breed_data(species=breed['species'], name=breed['name'], specifications=None)
            markup = send_home()
            bot.send_message(cid, text_admin['success_create_breed'].format(breed['name']), reply_markup=markup)
            breed.clear()
            user_steps[cid] = 0
        elif data == 'yes_specifications_breed':
            bot.send_message(cid, text_admin['specifications_breed_input'])
            user_steps[cid] = 3.1
    else:
        if data.startswith('first_name'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['first_name_edit'])
            user_steps[cid] = 1.1
        elif data.startswith('last_name'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['last_name_edit'])
            user_steps[cid] = 1.2
        elif data.startswith('username'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['username_edit'])
            user_steps[cid] = 1.3
        elif data.startswith('national_code'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['national_code_edit'])
            user_steps[cid] = 1.4
        elif data.startswith('phone'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['phone_edit'])
            user_steps[cid] = 1.5
        elif data.startswith('address'):
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['address_edit'])
            user_steps[cid] = 1.6
        elif data in species:
            chosen_breed = show_breed_name(data)
            markup = InlineKeyboardMarkup()
            for key,value in chosen_breed.items():
                markup.add(InlineKeyboardButton(value, callback_data=f"chosen_breed_id_{key}"))
            bot.edit_message_text(text_user['choose_breed'], cid, mid, call_id)
            bot.edit_message_reply_markup(cid, mid, call_id, reply_markup=markup)
        elif data.startswith('chosen_breed_id'):
            breed_id = int(data.split('_')[-1])
            user_pets.update({'breed_id': breed_id})
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            bot.send_message(cid, text_user['pet_name'])
            user_steps[cid] = 2
            


@bot.message_handler(commands=['start'])
def start_command(message):
    cid = message.chat.id
    if cid in admins :
        bot.send_message(cid, text['welcome'])
        home_command(message)
    else : 
        bot.send_message(cid, text['welcome'])
        home_command(message)
        if cid not in users:
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
        else:
            pass
  

@bot.message_handler(commands=['home'])
def home_command(message):
    cid = message.chat.id
    if cid in admins:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_admin['create_test'], buttons_admin['create_test_group'])
        markup.add(buttons_admin['create_breed'])
        bot.send_message(cid, text['home'], reply_markup=markup)
        user_steps[cid] = 0
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_user['account'], buttons_user['pets'])
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
        for item in show_user_data(cid):
            markup.add(InlineKeyboardButton(f"{text_user['first_name']} : {item['first_name']}", callback_data=f"first_name : {item['first_name']}"))
            markup.add(InlineKeyboardButton(f"{text_user['last_name']} : {item['last_name']}", callback_data=f"last_name : {item['last_name']}"))
            markup.add(InlineKeyboardButton(f"{text_user['username']} : {item['username']}", callback_data=f"username : {item['username']}"))
            markup.add(InlineKeyboardButton(f"{text_user['national_code']} : {item['national_code']}", callback_data=f"national_code : {item['national_code']}"))
            markup.add(InlineKeyboardButton(f"{text_user['phone']} : {item['phone']}", callback_data=f"phone : {item['phone']}"))
            markup.add(InlineKeyboardButton(f"{text_user['address']} : {item['address']}", callback_data=f"address : {item['address']}"))
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
        if check_test_group_exists():
            markup = send_home()
            bot.send_message(cid, text_admin['test_group_not'] ,reply_markup=markup)
        else :
            markup = InlineKeyboardMarkup()
            for item in show_test_group():
                markup.add(InlineKeyboardButton(item['name'], callback_data=f"test_group_{item['id']}"))
            bot.send_message(cid, text_admin['chooce_test_group'], reply_markup=markup)
    else :
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['create_breed'])
def create_breed_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = InlineKeyboardMarkup()
        for item in species:
            markup.add(InlineKeyboardButton(text[item], callback_data=item))
        bot.send_message(cid, text['chooce_species'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_user['pets'])
def pets_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_user['create_pet'])
        bot.send_message(cid, text_user['pet_menu'], reply_markup=markup)
    else:
        unknown_message()


@bot.message_handler(func=lambda message:message.text==buttons_user['create_pet'])
def create_pet_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = InlineKeyboardMarkup()
        for item in species:
            markup.add(InlineKeyboardButton(text[item], callback_data=item))
        bot.send_message(cid, text['chooce_species'], reply_markup=markup)
    else:
        unknown_message()


@bot.message_handler(func=lambda message : get_user_step(message.chat.id)==1)
def group_test_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        if check_test_group_name(name):
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1.1)
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
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1.2)
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
    else:
        unknown_message(message)



@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1.3)
def username_edit_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        username = message.text
        username_rules = True
        for char in username:
            char_value = ord(char)
            if (char_value >= 48 and char_value <= 57) or (char_value >= 97 and char_value <= 122) or char_value==95: #username rules based on telegram (0-9 or a-z or _)
                continue
            else:
                username_rules = False
                break
        if username_rules == True:
            if check_user_username(username):
                bot.send_message(cid, text_user['username_unique'])
            elif len(username) > 32:
                bot.send_message(cid, text.user['username_check'])
            else:
                edit_user_username(username=username, cid=cid)
                bot.send_message(cid, text_user['username_success'], reply_markup=markup)
        else:
            bot.send_message(cid, text_user['username_rules'])
    else:
        unknown_message(message)
  


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1.4)
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
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1.5)
def phone_edit(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        phone = message.text
        if is_valid(phone):
            edit_phone(phone=phone, cid=cid)
            bot.send_message(cid, text_user['phone_success'])
        else :
            bot.send_message(cid, text_user['phone_check'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1.6)
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
    else:
        unknown_message(message)



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
                    if parameter == "":
                        bot.send_message(cid, text_admin['parameter_test_null'])
                    else :
                        if check_test_parameter(parameter):
                            bot.send_message(cid, text_admin['parameter_test_unique'])
                        elif len(parameter) > 45:
                            bot.send_message(cid, text_admin['parameter_test_check'])
                        else :
                            test.update({key: parameter})
                elif key == 'type':
                    type = value
                    if type == "":
                        bot.send_message(cid, text_admin['type_test_null'])
                    else:
                        if type == 'quality' or type == 'quantity':
                            test.update({key: type})
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
                                test.update({key: price})
                elif key == 'unit':
                    unit = value
                    if unit == "":
                        test.update({key: None})
                    elif len(unit) > 10:
                        bot.send_message(cid, text_admin['unit_test_check'])
                    else:
                        test.update({key: unit})
                elif key == 'minimum_range':
                    minimum_range = value
                    if minimum_range == "":
                        test.update({key: None})
                    else:
                        try:
                            minimum_range = float(minimum_range)
                        except:
                            bot.send_message(cid, text_admin['minimum_range_test_check'])
                        else:
                            if len(str(minimum_range).split('.')[1]) > 5 or len(str(minimum_range).split('.')[-1]) > 3 :
                                bot.send_message(cid, text_admin['minimum_range_test_check'])
                            else:
                                test.update({key: minimum_range})
                elif key == 'maximum_range':
                    maximum_range = value
                    if maximum_range == "":
                        test.update({key: None})
                    else:
                        try:
                            maximum_range = float(maximum_range)
                        except:
                            bot.send_message(cid, text_admin['maximum_range_test_check'])
                        else:
                            if len(str(maximum_range).split('.')[1]) > 5 or len(str(maximum_range).split('.')[-1]) > 3 :
                                bot.send_message(cid, text_admin['maximum_range_test_check'])
                            else:
                                test.update({key: maximum_range})
                elif key == 'analyze_date':
                    analyze_date = value
                    if analyze_date == "":
                        test.update({key: None})
                    else:
                        try:
                            analyze_date = int(analyze_date)
                        except:
                            bot.send_message(cid, text_admin['analyze_date_test_check'])
                        else :
                            if 1 <= analyze_date <= 30:
                                test.update({key: analyze_date})
                            else :
                                bot.send_message(cid, text_admin['analyze_date_test_check'])
                elif key == 'description':
                    description = value
                    if description == "":
                        test.update({key: None})
                    elif len(description) > 255:
                        bot.send_message(cid, text_admin['description_test_check'])
                    else:
                        test.update({key: description})


        if len(test) == 9:
            insert_test_data(**test)
            bot.send_message(cid, text_admin['success_create_test'].format(test['parameter']))
            user_steps[cid] = 0
            test.clear()
            home_command(message)
    else:
        name = message.text
        if len(name) > 45:
            bot.send_message(cid, text_user['pet_name_check'])
        else:
            user_pets.update({'name': name})
            insert_pet_data(user_id=cid, breed_id=user_pets['breed_id'], name=user_pets['name'], gender=None, age=None, weight=None, personality=None)
            bot.send_message(cid, text_user['create_pet_success'].format(name))
            user_steps[cid] = 0
            user_pets.clear()


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3)
def breed_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        if check_breed_name(name):
            bot.send_message(cid, text_admin['name_breed_unique'])
        elif len(name) > 45:
            bot.send_message(cid,text_admin['name_breed_check'])
        else:
            breed.update({'name': name})
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text_admin['no'], callback_data='no_specifications_breed'), InlineKeyboardButton(text_admin['yes'], callback_data='yes_specifications_breed'))
            bot.send_message(cid, text_admin['specifications_breed'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3.1)
def breed_specifications_handler(message):
    cid = message.chat.id
    if cid in admins:
        specifications = message.text
        if len(specifications) > 255:
            bot.send_message(cid, text_admin['specifications_breed_check'])
        else:
            breed.update({'specifications': specifications})
            insert_breed_data(species=breed['species'], name=breed['name'], specifications=breed['specifications'])
            bot.send_message(cid, text_admin['success_create_breed'].format(breed['name']))
            user_steps[cid] = 0
            breed.clear()
            home_command(message)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    cid = message.chat.id
    bot.send_message(cid, text['unknown_message'])

users = get_member_user()
bot.infinity_polling()