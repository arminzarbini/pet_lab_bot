import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardRemove
from DML import *
from DQL import *
from config import *
from text import *
import re
import jdatetime
from datetime import datetime
import random
import string

bot = telebot.TeleBot(BOT_TOKEN, num_threads=10)
hideboard = ReplyKeyboardRemove()
users = list() #[cid, ...]
user_steps = dict() # {cid, step,...}
test = dict() # {test_group_id : ... , parameter : ..., type : ... , price : ... , unit : ..., minimum_range : ... , maximum_range : ... , analyze_date : ..., description : ...}
breed = dict() # {species : ..., name : ..., specifications : ...}
user_pets = dict() #{breed_id : ..., name : ...}
pet_id_dict = dict() #{'id' : id}
pet_reception = dict() #{id : {test_id,...}}

def get_member_user():
    member_user = show_member_user()
    return member_user

def get_user_step(cid):
    return user_steps.setdefault(cid, 0)

def send_home():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons['home'])
        return markup

def is_valid_phone(phone):
	Pattern = re.compile("^(0|0098|\+98)?9\d{9}$") #start - group(0 or 0098 or +98) - 9 - exactly 9 digits - end
	return Pattern.match(phone)

def is_valid_date(birth_date):
    try:
        persian_date = datetime.strptime(birth_date, '%Y/%m/%d').date()
    except:
        return False
    else:
        gregorian_date = jdatetime.date.togregorian(persian_date)
        return gregorian_date
    
def reception_pet_markup(cid):
    markup = InlineKeyboardMarkup()
    for key,value in show_pet_id(cid).items():
        markup.add(InlineKeyboardButton(value, callback_data=f"choose_pet_{key}"))
    return markup
    
def reception_test_markup(pet_id):
    markup = InlineKeyboardMarkup()
    for item in show_test():
        if item['id'] in pet_reception[pet_id]:
            markup.add(InlineKeyboardButton(f"🧪{text_user['parameter']} : {item['parameter']} - {text_user['price']} : {item['price']}{text_user['toman']}🧪", callback_data=f"remove_test_{item['id']}_{pet_id}"))
        else:
            markup.add(InlineKeyboardButton(f"{text_user['parameter']} : {item['parameter']} - {text_user['price']} : {item['price']}{text_user['toman']}", callback_data=f"choose_test_{item['id']}_{pet_id}"))
    markup.add(InlineKeyboardButton(text_user['order'], callback_data=f"order_{pet_id}"))
    markup.add(InlineKeyboardButton(text_user['return'], callback_data='return'))
    return markup

def reception_request_markup():
    markup = InlineKeyboardMarkup()
    for item in show_reception_request():
        persian_datetime = jdatetime.datetime.fromgregorian(datetime=item['request_date'])
        persian_datetime_str = jdatetime.datetime.strftime(persian_datetime, "%Y/%m/%d %H:%M:%S")
        markup.add(InlineKeyboardButton(f"{item['username']} - {persian_datetime_str}", callback_data=f"request_{item['name']}_{item['id']}")) 
    return markup 

def reception_edit_markup(reception_id):
    markup = InlineKeyboardMarkup()
    reception_data = show_reception_data(reception_id)
    for key,value in reception_data.items():
        markup.add(InlineKeyboardButton(f"{text_admin[key]} : {value}", callback_data=f"{key}_edit_{reception_id}"))
    return markup
    
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
        elif data in species_enum:
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
        elif data.startswith('request'):
            reception_id = int(data.split('_')[-1])
            pet_name = data.split('_')[-2]
            markup = reception_edit_markup(reception_id)
            bot.edit_message_text(text_admin['reception_data_edit'],cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
            bot.send_message(cid, text_admin['request_items'].format(pet_name))
            for item in show_reception_test(reception_id):
                bot.send_message(cid, item)
        elif data.startswith('code_edit'):
            reception_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            if check_reception_code_exist(reception_id):
                bot.send_message(cid, text_admin['reception_code_exist'])
            else:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                if check_reception_code(code):
                    bot.send_message(cid, text_admin['reception_code_try_again'])
                else:
                    reception_date = datetime.now()
                    edit_reception_code(code=code, reception_date=reception_date, id=reception_id)
                    bot.send_message(cid, text_admin['reception_code_success'])
    else:
        if data == 'first_name_edit':
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['first_name_edit'])
            user_steps[cid] = 10.1
        elif data == 'last_name_edit':
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['last_name_edit'])
            user_steps[cid] = 10.2
        elif data == 'username_edit':
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['username_edit'])
            user_steps[cid] = 10.3
        elif data == 'national_code_edit':
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['national_code_edit'])
            user_steps[cid] = 10.4
        elif data == 'phone_edit':
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['phone_edit'])
            user_steps[cid] = 10.5
        elif data == 'address_edit':
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['address_edit'])
            user_steps[cid] = 10.6
        elif data in species_enum:
            chosen_breed = show_breed_name(data)
            markup = InlineKeyboardMarkup()
            for key,value in chosen_breed.items():
                markup.add(InlineKeyboardButton(value, callback_data=f"chosen_breed_id_{key}"))
            bot.edit_message_text(text_user['choose_breed'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('chosen_breed_id'):
            breed_id = int(data.split('_')[-1])
            user_pets.update({'breed_id': breed_id})
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            bot.send_message(cid, text_user['pet_name'])
            user_steps[cid] = 11
        elif data.startswith('edit_gender'):
            pet_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            markup = InlineKeyboardMarkup()
            for item in gender_enum:
                markup.add(InlineKeyboardButton(text_user[item], callback_data=f"{item}_{pet_id}"))
            bot.send_message(cid, text_user['pet_gender_edit'], reply_markup=markup)
        elif data.startswith('male') or data.startswith('female'):
            pet_id = int(data.split('_')[-1])
            gender = data.split('_')[0]
            markup = send_home()
            edit_pet_gender(gender=gender, user_id=cid, id=pet_id)
            bot.send_message(cid, text_user['pet_gender_success'], reply_markup=markup)
        elif data.startswith('edit_birth_date'):
            pet_id = int(data.split('_')[-1])
            pet_id_dict.update({'id': pet_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['pet_birth_date_edit'])
            user_steps[cid] = 11.1
        elif data.startswith('edit_weight'):
            pet_id = int(data.split('_')[-1])
            pet_id_dict.update({'id': pet_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['pet_weight_edit'])
            user_steps[cid] = 11.2
        elif data.startswith('edit_personality'):
            pet_id = int(data.split('_')[-1])
            pet_id_dict.update({'id': pet_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['pet_personality_edit'])
            user_steps[cid] = 11.3
        elif data.startswith('choose_pet'):
            pet_id = int(data.split('_')[-1])
            pet_reception.setdefault(pet_id, set())
            bot.answer_callback_query(call_id, '✅')
            markup = reception_test_markup(pet_id)
            bot.edit_message_text(text_user['choose_test'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('choose_test'):
            pet_id = int(data.split('_')[-1])
            test_id = int(data.split('_')[-2])
            pet_reception[pet_id].add(test_id)
            markup = reception_test_markup(pet_id)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('remove_test'):
            pet_id = int(data.split('_')[-1])
            test_id = int(data.split('_')[-2])
            pet_reception[pet_id].remove(test_id)
            markup = reception_test_markup(pet_id)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith("order"):
            pet_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            if len(pet_reception[pet_id]) == 0:
                bot.send_message(cid, text_user['no_choose_test'])
            else:
                insert_reception_data(pet_id=pet_id)
                reception_id = show_reception(pet_id)
                for item in pet_reception[pet_id]:
                    insert_reception_test_data(reception_id=reception_id, test_id=item)
                pet_reception[pet_id].clear()
                try:
                    bot.delete_message(cid, mid)
                except:
                    pass
                bot.send_message(cid, text_user['reception_request_success'])
        elif data == 'return':
            markup = reception_pet_markup(cid)
            bot.edit_message_text(text_user['choose_pet'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
            

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
            insert_user_data(cid=cid, first_name=first_name, last_name=last_name, username=username, national_code=None, phone=None, address=None) #unique_username
        else:
            pass
  

@bot.message_handler(commands=['home'])
def home_command(message):
    cid = message.chat.id
    if cid in admins:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_admin['create_test'], buttons_admin['create_test_group'])
        markup.add(buttons_admin['create_breed'])
        markup.add(buttons_admin['reception_request'])
        bot.send_message(cid, text['home'], reply_markup=markup)
        user_steps[cid] = 0
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_user['account'], buttons_user['pets'])
        markup.add(buttons_user['reception_request'])
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
        for key,value in user_data.items():
            markup.add(InlineKeyboardButton(f"{text_user[key]} : {value}", callback_data=f"{key}_edit"))
        bot.send_message(cid, text_user['user_data'], reply_markup=markup)
    markup = send_home()
    bot.send_message(cid, text_user['user_data_edit'], reply_markup=markup)


@bot.message_handler(func=lambda message: message.text==buttons_admin['create_test_group'])
def create_test_group_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = send_home()
        bot.send_message(cid, text_admin['name_test_group_input'], reply_markup=markup)
        user_steps[cid] = 1
    else :
        unknown_message(message)


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
        for item in species_enum:
            markup.add(InlineKeyboardButton(text[item], callback_data=item))
        bot.send_message(cid, text['chooce_species'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_user['pets'])
def pets_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        if len(show_pet(cid))!=0:
            for item in show_pet(cid):
                markup.add(item)
        markup.add(buttons_user['create_pet'])
        bot.send_message(cid, text_user['pet_menu'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_user['create_pet'])
def create_pet_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = InlineKeyboardMarkup()
        for item in species_enum:
            markup.add(InlineKeyboardButton(text[item], callback_data=item))
        bot.send_message(cid, text['chooce_species'], reply_markup=markup)
    else:
        unknown_message(message)
        

@bot.message_handler(func=lambda message:message.text==buttons_user['reception_request'])
def reception_request_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = reception_pet_markup(cid)
        bot.send_message(cid, text_user['choose_pet'], reply_markup=markup)
    else:
       unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['reception_request'])
def reception_request_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = reception_request_markup()
        bot.send_message(cid, text_admin['requests_test'], reply_markup=markup)
    else:
        unknown_message(message)
    

@bot.message_handler(func=lambda message:message.text in show_pet(message.chat.id))
def pet_edit_handler(message):
    cid = message.chat.id
    name = message.text
    if cid not in admins:
        pet_data = show_pet_data(cid, name)
        markup = InlineKeyboardMarkup()
        for key,value in pet_data.items():
            if key == 'id':
                pet_id = value
                continue
            markup.add(InlineKeyboardButton(f"{text_user[key]} : {value}", callback_data=f"edit_{key}_{pet_id}"))
        bot.send_message(cid, text_user['pet_data'].format(name), reply_markup=markup)
        markup = send_home()
        bot.send_message(cid, text_user['pet_data_edit'], reply_markup=markup)
    else:
        unknown_message(message)


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
                            if len(str(price).split('.')[0]) > 8 or len(str(price).split('.')[-1]) > 2 :
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
                            if len(str(minimum_range).split('.')[0]) > 5 or len(str(minimum_range).split('.')[-1]) > 3 :
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
                            if len(str(maximum_range).split('.')[0]) > 5 or len(str(maximum_range).split('.')[-1]) > 3 :
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
        unknown_message(message)


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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.1)
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.2)
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.3)
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
  

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.4)
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.5)
def phone_edit(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        phone = message.text
        if is_valid_phone(phone):
            edit_phone(phone=phone, cid=cid)
            bot.send_message(cid, text_user['phone_success'])
        else :
            bot.send_message(cid, text_user['phone_check'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.6)
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11)
def pet_handler(message):
    cid = message.chat.id
    if cid not in admins:
        name = message.text
        if len(name) > 45:
            bot.send_message(cid, text_user['pet_name_check'])
        else:
            user_pets.update({'name': name})
            insert_pet_data(user_id=cid, breed_id=user_pets['breed_id'], name=user_pets['name'], gender=None, birth_date=None, weight=None, personality=None)
            bot.send_message(cid, text_user['create_pet_success'].format(name))
            user_steps[cid] = 0
            user_pets.clear()
    else:
        unknown_message(message)
    

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11.1)
def pet_birth_date_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        birth_date_str = message.text
        if is_valid_date(birth_date_str) == False:
            bot.send_message(cid, text_user['pet_birth_date_check'], reply_markup=markup)
        else:
            birth_date = is_valid_date(birth_date_str)
            edit_pet_birth_date(birh_date=birth_date, user_id=cid, id=pet_id_dict['id'])
            bot.send_message(cid, text_user['pet_birth_date_success'], reply_markup=markup) 
            pet_id_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11.2)
def pet_weight_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        weight = message.text
        try:
            weight = float(weight)
        except:
            bot.send_message(cid, text_user['pet_weight_check'], reply_markup=markup)
        else:
            if len(str(weight).split('.')[0]) > 3 or len(str(weight).split('.')[-1]) > 3:
                bot.send_message(cid, text_user['pet_weight_check'], reply_markup=markup)
            else:
                edit_pet_weight(weight=weight, user_id=cid, id=pet_id_dict['id'])
                bot.send_message(cid, text_user['pet_weight_success'], reply_markup=markup) 
                pet_id_dict.clear()  
                user_steps[cid] = 0               
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11.3)
def pet_personality_edit_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        personality = message.text
        if len(personality) > 255:
            bot.send_message(cid, text_user['pet_personality_check'], reply_markup=markup)
        else:
            edit_pet_personality(personality=personality, user_id=cid, id=pet_id_dict['id'])
            bot.send_message(cid, text_user['pet_personality_success'], reply_markup=markup)
            pet_id_dict.clear()  
            user_steps[cid] = 0     
    else:
        unknown_message(message)
        

@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    cid = message.chat.id
    bot.send_message(cid, text['unknown_message'])


users = get_member_user()
bot.infinity_polling()