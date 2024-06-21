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
import datetime

bot = telebot.TeleBot(BOT_TOKEN, num_threads=10)
hideboard = ReplyKeyboardRemove()
users = list() #[cid, ...]
user_steps = dict() # {cid, step,...}
test = dict() # {test_group_id : ... , parameter : ..., type : ... , price : ... , unit : ..., minimum_range : ... , maximum_range : ... , analyze_date : ..., description : ...}
breed = dict() # {species : ..., name : ..., specifications : ...}
breed_id_dict = dict() #{breed_id : breed_id}
pet_id_dict = dict() #{'id' : id}
pet_reception = dict() #{id : {test_id,...}}
reception_id_dict = dict() #{id : id}

def get_member_user(): #return member user
    member_user = show_member_user()
    return member_user

def get_user_step(cid): #return user steps
    return user_steps.setdefault(cid, 0)

def send_home():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons['home'])
        return markup

def is_valid_phone(phone):
	Pattern = re.compile("^(0|0098|\+98)?9\d{9}$") #start - group(0 or 0098 or +98) - 9 - exactly 9 digits - end
	return Pattern.match(phone)

def is_valid_date(date): #check persian date string : year/month/day
    try:
        persian_date = datetime.datetime.strptime(date, '%Y/%m/%d').date()
    except:
        return False
    else:
        gregorian_date = jdatetime.date.togregorian(persian_date)
        return gregorian_date
    
def show_persian_datetime(datetime): #return persian datetime as srting
    persian_datetime = jdatetime.datetime.fromgregorian(datetime=datetime)
    persian_datetime_str = jdatetime.datetime.strftime(persian_datetime, "%Y/%m/%d %H:%M:%S")
    return persian_datetime_str

def show_persian_date(date): #return persian date as srting
    persian_date = jdatetime.date.fromgregorian(date=date)
    persian_date_str = jdatetime.date.strftime(persian_date, "%Y/%m/%d")
    return persian_date_str

def reception_pet_markup(cid): #generate markup pet name with cid
    markup = InlineKeyboardMarkup()
    for key,value in show_pet_id(cid).items():
        markup.add(InlineKeyboardButton(value, callback_data=f"choose_pet_{key}"))
    return markup

def reception_test_markup(pet_id): #generate markup test item and order and return for add and remove and order 
    markup = InlineKeyboardMarkup()
    for item in show_test():
        if item['id'] in pet_reception[pet_id]:
            markup.add(InlineKeyboardButton(f"🧪{text_user['parameter']} : {item['parameter']} - {text_user['price']} : {item['price']}{text_user['toman']}🧪", callback_data=f"remove_test_{item['id']}_{pet_id}"))
        else:
            markup.add(InlineKeyboardButton(f"{text_user['parameter']} : {item['parameter']} - {text_user['price']} : {item['price']}{text_user['toman']}", callback_data=f"choose_test_{item['id']}_{pet_id}"))
    markup.add(InlineKeyboardButton(text_user['order'], callback_data=f"order_{pet_id}"))
    markup.add(InlineKeyboardButton(text['return'], callback_data='return_pet_markup'))
    return markup

def show_reception_markup(cid): #generate markup reception item for user
    markup = InlineKeyboardMarkup()
    for item in show_reception_request_user(cid):
        if item['code'] == None:
            persian_date_str = show_persian_date(item['request_date'])
            markup.add(InlineKeyboardButton(f"{text_user['test_for']} {item['name']} {text_user['reception_request_date']}:{persian_date_str}", callback_data=f"request_{item['id']}"))
        else:
            persian_date_str = show_persian_date(item['reception_date'])
            markup.add(InlineKeyboardButton(f"{text_user['test_for']} {item['name']} {text_user['reception_reception_date']}:{persian_date_str} {text_user['reception_code']} {item['code']} ", callback_data=f"reception_{item['id']}"))
    return markup

def reception_receipt_markup(reception_id): #generate markup receptit and return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text_user['send_receipt'], callback_data=f"send_receipt_{reception_id}"))
    markup.add(InlineKeyboardButton(text['return'], callback_data='return_reception_markup'))
    return markup

def request_markup(): #generate markup reception without code
    markup = InlineKeyboardMarkup()
    for item in show_request():
        persian_datetime_str = show_persian_datetime(item['request_date'])
        markup.add(InlineKeyboardButton(f"{item['username']} - {persian_datetime_str}", callback_data=f"request_{item['name']}_{item['id']}")) 
    return markup 

def reception_markup(): #generate markup reception with code
    markup = InlineKeyboardMarkup()
    for item in show_reception():
        persian_datetime_str = show_persian_datetime(item['reception_date'])
        markup.add(InlineKeyboardButton(f"{item['username']} - {persian_datetime_str} - {item['code']}", callback_data=f"reception_{item['name']}_{item['id']}"))
    return markup

def request_edit_markup(reception_id): #generate markup request manage
    markup = InlineKeyboardMarkup()
    for key in show_reception_data(reception_id).keys():
        if key == 'code':
            markup.add(InlineKeyboardButton(text_admin[key], callback_data=f"{key}_edit_{reception_id}"))
            break
    markup.add(InlineKeyboardButton(text['return'], callback_data='return_request_markup'))
    return markup

def reception_edit_markup(reception_id): #generate markup reception manage
    markup = InlineKeyboardMarkup()
    for key,value in show_reception_data(reception_id).items():
        if key == 'code':
            continue
        elif isinstance(value, datetime.date):
            persian_date_str = show_persian_date(value)
            markup.add(InlineKeyboardButton(f"{text_admin[key]} : {persian_date_str}", callback_data=f"{key}_edit_{reception_id}"))
        elif value == None:
            markup.add(InlineKeyboardButton(f"{text_admin[key]}", callback_data=f"{key}_edit_{reception_id}"))
        else:
            markup.add(InlineKeyboardButton(f"{text_admin[key]} : {value}", callback_data=f"{key}_edit_{reception_id}"))
    markup.add(InlineKeyboardButton(text['return'], callback_data='return_reception_markup'))
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
            bot.send_message(cid, text_admin['template_test'])
            bot.send_message(cid, text_admin['template_input_test'])
            user_steps[cid] = 2
        elif data in species_enum: 
            breed.update({'species': data})
            bot.answer_callback_query(call_id, '✅')
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            bot.send_message(cid, text_admin['breed_name'])
            user_steps[cid] = 3
        elif data == 'no_specifications_breed': 
            insert_breed_data(species=breed['species'], name=breed['name'], specifications=None)
            markup = send_home()
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            bot.send_message(cid, text_admin['create_breed_success'].format(breed['name']), reply_markup=markup)
            breed.clear()
            user_steps[cid] = 0
        elif data == 'yes_specifications_breed': 
            bot.send_message(cid, text_admin['breed_specifications'])
            user_steps[cid] = 3.1
        elif data.startswith('request'): 
            reception_id = int(data.split('_')[-1])
            pet_name = data.split('_')[-2]
            comment = show_reception_comment(reception_id)
            receipt_image = show_reception_receipt_image_file_id(reception_id)
            total_price = show_reception_price(reception_id)
            markup = request_edit_markup(reception_id)
            bot.edit_message_text(text_admin['generate_reception_code'],cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
            bot.send_message(cid, text_admin['request_items'].format(pet_name))
            for item in show_reception_test(reception_id):
                bot.send_message(cid, f"❎{item}❎")
            if comment != None:
                bot.send_message(cid, text['comment'].format(comment))
            bot.send_message(cid, f"{text_user['total_price']} {total_price}{text_user['toman']}")
            if receipt_image != None:
                bot.send_photo(cid, receipt_image, text_admin['receipt'])
        elif data == 'return_request_markup':
            markup = request_markup()
            bot.send_message(cid, text_admin['requests_test'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('reception'):
            reception_id = int(data.split('_')[-1])
            pet_name = data.split('_')[-2]
            comment = show_reception_comment(reception_id)
            receipt_image = show_reception_receipt_image_file_id(reception_id)
            total_price = show_reception_price(reception_id)
            markup = reception_edit_markup(reception_id)
            bot.edit_message_text(text_admin['reception_edit'],cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
            bot.send_message(cid, text_admin['request_items'].format(pet_name))
            for item in show_reception_test(reception_id):
                bot.send_message(cid, f"❎{item}❎")
            if comment != None:
                bot.send_message(cid, text['comment'].format(comment))
            bot.send_message(cid, f"{text_user['total_price']} {total_price}{text_user['toman']}")
            if receipt_image != None:
                bot.send_photo(cid, receipt_image, text_admin['receipt'])
        elif data == 'return_reception_markup':
            markup = reception_markup()
            bot.send_message(cid, text_admin['reception_test'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('code_edit'):
            reception_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            code = ''.join(random.choices(string.digits + string.ascii_uppercase, k=5)) #generate random reception code (0-9 + uppercase)
            if check_reception_code(code):
                bot.send_message(cid, text_admin['reception_code_try_again'])
            else:
                reception_date = datetime.datetime.now() #calculate reception date
                edit_reception_code_date(code=code, reception_date=reception_date, id=reception_id)
                if (check_reception_test_analyze_date(reception_id)) != None: 
                    analyze_date = check_reception_test_analyze_date(reception_id) 
                    answer_date = reception_date + datetime.timedelta(analyze_date) #calculate answer date
                    edit_reception_answer_date(answer_date=answer_date, id=reception_id)
                bot.send_message(cid, text_admin['reception_code_success'])
        elif data.startswith('answer_date_edit'):
            reception_id = int(data.split('_')[-1])
            reception_id_dict.update({'id': reception_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_admin['reception_answer_date_edit'])
            user_steps[cid] = 4
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
            markup = InlineKeyboardMarkup()
            for item in show_breed_name(data):
                markup.add(InlineKeyboardButton(item['name'], callback_data=f"choose_breed_{item['id']}"))
            bot.edit_message_text(text_user['choose_breed'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('choose_breed'):
            breed_id = int(data.split('_')[-1])
            breed_id_dict.update({'breed_id': breed_id})
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
            try:
                bot.delete_message(cid, mid)
            except:
                pass
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
            if len(pet_reception[pet_id]) == 0:
                bot.answer_callback_query(call_id, '❌')
                bot.send_message(cid, text_user['no_choose_test'])
            else:
                try:
                    bot.delete_message(cid, mid)
                except:
                    pass
                bot.answer_callback_query(call_id, '✅')
                markup = InlineKeyboardMarkup() #markup for reception comment with yes and no
                markup.add(InlineKeyboardButton(text['no'], callback_data=f"no_reception_comment_{pet_id}"), InlineKeyboardButton(text['yes'], callback_data=f"yes_reception_comment_{pet_id}"))
                bot.send_message(cid, text_user['reception_comment'], reply_markup=markup)
        elif data == 'return_pet_markup':
            markup = reception_pet_markup(cid)
            bot.edit_message_text(text_user['choose_pet'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('no_reception_comment'):
            pet_id = int(data.split('_')[-1])   
            insert_reception_data(pet_id=pet_id)        
            reception_id = show_reception_id(pet_id)
            for item in pet_reception[pet_id]:
                insert_reception_test_data(reception_id=reception_id, test_id=item)
            pet_reception[pet_id].clear()
            bot.send_message(cid, text_user['reception_request_success'])
            total_price = show_reception_price(reception_id)
            bot.send_message(cid, f"{text_user['total_price']} {total_price}{text_user['toman']}")
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('yes_reception_comment'):
            pet_id = int(data.split('_')[-1])   
            pet_id_dict.update({'id': pet_id})
            bot.send_message(cid, text_user['reception_comment_input'])
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            user_steps[cid] = 12
        elif data.startswith('request') or data.startswith('reception'):
            reception_id = int(data.split('_')[-1])
            comment = show_reception_comment(reception_id)
            total_price = show_reception_price(reception_id)
            markup = reception_receipt_markup(reception_id)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
            for item in show_reception_test(reception_id):
                bot.send_message(cid, f"❎{item}❎")
            if comment != None:
                bot.send_message(cid, text['comment'].format(comment))
            bot.send_message(cid, f"{text_user['total_price']} {total_price}{text_user['toman']}")
        elif data == 'return_reception_markup':
            markup = show_reception_markup(cid)
            bot.send_message(cid, text_user['reception_manage'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('send_receipt'):
            reception_id = pet_id = int(data.split('_')[-1])
            reception_id_dict.update({'id': reception_id})
            bot.send_message(cid, text_user['send_receipt_image'])
            user_steps[cid] = 13
  
         
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
            users.append(cid)
            first_name = message.chat.first_name 
            if message.chat.last_name == None: 
                last_name = None
            else:
                last_name = message.chat.last_name
            insert_user_data(cid=cid, first_name=first_name, last_name=last_name, username=None, national_code=None, phone=None, address=None) 
        else:
            pass
  

@bot.message_handler(commands=['home'])
def home_command(message):
    cid = message.chat.id
    if cid in admins:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_admin['create_test'], buttons_admin['create_test_group'])
        markup.add(buttons_admin['create_breed'])
        markup.add(buttons_admin['reception_manage'], buttons_admin['request_manage'])
        bot.send_message(cid, text['home'], reply_markup=markup)
        user_steps[cid] = 0
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_user['account'], buttons_user['pets'])
        markup.add(buttons_user['reception_manage'], buttons_user['reception_request'])
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
        for key,value in show_user_data(cid).items(): #generate markup for edit username information
            if value == None:
                markup.add(InlineKeyboardButton(f"{text_user[key]}", callback_data=f"{key}_edit"))
            else :
                markup.add(InlineKeyboardButton(f"{text_user[key]} : {value}", callback_data=f"{key}_edit"))
        bot.send_message(cid, text_user['user_data'], reply_markup=markup)
    markup = send_home()
    bot.send_message(cid, text_user['user_data_edit'], reply_markup=markup)


@bot.message_handler(func=lambda message:message.text==buttons_user['pets'])
def pets_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
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
        bot.send_message(cid, text['choose_species'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text in show_pet(message.chat.id))
def pet_edit_handler(message):
    cid = message.chat.id
    name = message.text
    if cid not in admins:
        markup = InlineKeyboardMarkup()
        for key,value in show_pet_data(cid, name).items(): #generate markup for edit pet information
            if key == 'id':
                pet_id = value
                continue
            elif isinstance(value, datetime.date):
                persian_date_str = show_persian_date(value)
                markup.add(InlineKeyboardButton(f"{text_user[key]} : {persian_date_str}", callback_data=f"edit_{key}_{pet_id}"))
            elif key == 'gender' and value in gender_enum:
                markup.add(InlineKeyboardButton(f"{text_user[key]} : {text_user[value]}", callback_data=f"edit_{key}_{pet_id}"))
            elif value == None:
                markup.add(InlineKeyboardButton(f"{text_user[key]}", callback_data=f"edit_{key}_{pet_id}"))
            else:
                markup.add(InlineKeyboardButton(f"{text_user[key]} : {value}", callback_data=f"edit_{key}_{pet_id}"))
        bot.send_message(cid, text_user['pet_data'].format(name), reply_markup=markup)
        markup = send_home()
        bot.send_message(cid, text_user['pet_data_edit'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_user['reception_request'])
def reception_request_handler(message):
    cid = message.chat.id
    if cid not in admins:
        if no_user_username(cid):
            bot.send_message(cid,text_user['no_username'])
        else:
            markup = reception_pet_markup(cid)
            bot.send_message(cid, text_user['choose_pet'], reply_markup=markup)
    else:
       unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_user['reception_manage'])
def request_manage_user_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = show_reception_markup(cid)
        bot.send_message(cid, text_user['reception_manage'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message: message.text==buttons_admin['create_test_group'])
def create_test_group_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = send_home()
        bot.send_message(cid, text_admin['test_group_name'], reply_markup=markup)
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
            bot.send_message(cid, text_admin['choose_test_group'], reply_markup=markup)
    else :
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['create_breed'])
def create_breed_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = InlineKeyboardMarkup()
        for item in species_enum:
            markup.add(InlineKeyboardButton(text[item], callback_data=item))
        bot.send_message(cid, text['choose_species'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['request_manage'])
def request_manage_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = request_markup()
        bot.send_message(cid, text_admin['requests_test'], reply_markup=markup)
    else:
        unknown_message(message)
    

@bot.message_handler(func=lambda message:message.text==buttons_admin['reception_manage'])
def reception_manage_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = reception_markup()
        bot.send_message(cid,text_admin['reception_test'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1)
def group_test_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        if check_test_group_name(name):
            bot.send_message(cid, text_admin['test_group_name_unique'])
        elif len(name) > 45:
            bot.send_message(cid, text_admin['test_group_name_check'])
        else:
            insert_test_group_data(name=name)
            bot.send_message(cid, text_admin['create_test_group_success'].format(name))
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
        #item_title = list()
        for item in item_test :
            item_check.setdefault(item.split(':')[0],  item.split(':')[-1])
            #item_title.append(item.split(':')[0])
        if len(item_test_check) != len(item_check.keys()):
            bot.send_message(cid, text_admin['send_full_test_item'])
        elif item_test_check != list(item_check.keys()):
            bot.send_message(cid, text_admin['test_item_check'])
        else:
            for key,value in item_check.items():  
                if key == 'parameter':
                    parameter = value
                    if parameter == "":
                        bot.send_message(cid, text_admin['test_parameter_null'])
                    else :
                        if check_test_parameter(parameter):
                            bot.send_message(cid, text_admin['test_parameter_unique'])
                        elif len(parameter) > 45:
                            bot.send_message(cid, text_admin['test_parameter_check'])
                        else :
                            test.update({key: parameter})
                elif key == 'type':
                    type = value
                    if type == "":
                        bot.send_message(cid, text_admin['test_type_null'])
                    else:
                        if type == 'quality' or type == 'quantity':
                            test.update({key: type})
                        else : 
                            bot.send_message(cid, text_admin['test_type_check'])
                elif key == 'price':
                    price = value
                    if price == "":
                        bot.send_message(cid, text_admin['test_price_null'])
                    else:
                        try:
                            price = int(price)
                        except:
                            bot.send_message(cid, text_admin['test_price_check'])
                        else:
                            if len(str(price)) > 10:
                                bot.send_message(cid, text_admin['price_test_check'])
                            else:
                                test.update({key: price})
                elif key == 'unit':
                    unit = value
                    if unit == "":
                        test.update({key: None})
                    elif len(unit) > 10:
                        bot.send_message(cid, text_admin['test_unit_check'])
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
                            bot.send_message(cid, text_admin['test_minimum_range_check'])
                        else:
                            if len(str(minimum_range).split('.')[0]) > 5 or len(str(minimum_range).split('.')[-1]) > 3 :
                                bot.send_message(cid, text_admin['test_minimum_range_check'])
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
                            bot.send_message(cid, text_admin['test_maximum_range_check'])
                        else:
                            if len(str(maximum_range).split('.')[0]) > 5 or len(str(maximum_range).split('.')[-1]) > 3 :
                                bot.send_message(cid, text_admin['test_maximum_range_check'])
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
                            bot.send_message(cid, text_admin['test_analyze_date_check'])
                        else :
                            if 1 <= analyze_date <= 90:
                                test.update({key: analyze_date})
                            else :
                                bot.send_message(cid, text_admin['test_analyze_date_check'])
                elif key == 'description':
                    description = value
                    if description == "":
                        test.update({key: None})
                    elif len(description) > 255:
                        bot.send_message(cid, text_admin['test_description_check'])
                    else:
                        test.update({key: description})
        if len(test) == 9:
            insert_test_data(**test)
            bot.send_message(cid, text_admin['create_test_success'].format(test['parameter']))
            test.clear()
            user_steps[cid] = 0
            home_command(message)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3)
def breed_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        if check_breed_name(name):
            bot.send_message(cid, text_admin['breed_name_unique'])
        elif len(name) > 45:
            bot.send_message(cid,text_admin['breed_name_check'])
        else:
            breed.update({'name': name})
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text['no'], callback_data='no_specifications_breed'), InlineKeyboardButton(text['yes'], callback_data='yes_specifications_breed'))
            bot.send_message(cid, text_admin['breed_specifications_yn'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3.1)
def breed_specifications_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = send_home()
        specifications = message.text
        if len(specifications) > 255:
            bot.send_message(cid, text_admin['breed_specifications_check'])
        else:
            breed.update({'specifications': specifications})
            insert_breed_data(species=breed['species'], name=breed['name'], specifications=breed['specifications'])
            bot.send_message(cid, text_admin['create_breed_success'].format(breed['name']), reply_markup=markup)
            breed.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==4)
def reception_answer_date_edit(message):
    cid = message.chat.id
    if cid in admins:
        answer_date = message.text
        if is_valid_date(answer_date) == False:
            bot.send_message(cid, text_admin['reception_answer_date_check'])
        else:
            answer_date = is_valid_date(answer_date)
            edit_reception_answer_date(answer_date=answer_date, id=reception_id_dict['id'])
            bot.send_message(cid, text_admin['reception_answer_date_success']) 
            reception_id_dict.clear()
            user_steps[cid] = 0


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
            user_steps[cid] = 0
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
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.3)
def username_edit_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        username = message.text
        username_rules = True #flag for username check
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
                user_steps[cid] = 0
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
        if len(national_code) != 10 or national_code.isnumeric() == False:
            bot.send_message(cid, text_user['national_code_check'])
        else:
            edit_user_national_code(national_code=national_code, cid=cid)
            bot.send_message(cid, text_user['national_code_success'], reply_markup=markup)
            user_steps[cid] = 0
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
            user_steps[cid] = 0
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
            user_steps[cid] = 0
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
            insert_pet_data(user_id=cid, breed_id=breed_id_dict['breed_id'], name=name, gender=None, birth_date=None, weight=None, personality=None)
            bot.send_message(cid, text_user['create_pet_success'].format(name))
            breed_id_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)
    

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11.1)
def pet_birth_date_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = send_home()
        birth_date_str = message.text
        if is_valid_date(birth_date_str) == False:
            bot.send_message(cid, text_user['pet_birth_date_check'])
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
            bot.send_message(cid, text_user['pet_weight_check'])
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
            bot.send_message(cid, text_user['pet_personality_check'])
        else:
            edit_pet_personality(personality=personality, user_id=cid, id=pet_id_dict['id'])
            bot.send_message(cid, text_user['pet_personality_success'], reply_markup=markup)
            pet_id_dict.clear()  
            user_steps[cid] = 0     
    else:
        unknown_message(message)
        

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==12)
def reception_comment_handler(message):
    cid = message.chat.id
    if cid not in admins:
        comment = message.text
        if len(comment) > 255:
            bot.send_message(cid, text_user['reception_comment_check'])
        else:
            pet_id = pet_id_dict['id']
            insert_reception_data(pet_id=pet_id, comment=comment)
            reception_id = show_reception_id(pet_id)
            for item in pet_reception[pet_id]:
                insert_reception_test_data(reception_id=reception_id, test_id=item)
            pet_reception[pet_id].clear()
            bot.send_message(cid, text_user['reception_request_success'])
            total_price = show_reception_price(reception_id)
            bot.send_message(cid, f"{text_user['total_price']} {total_price}{text_user['toman']}")
            pet_id_dict.clear()
            user_steps[cid] = 0


@bot.message_handler(content_types=['photo'])
def receipt_handler(message):
    cid = message.chat.id
    if cid not in admins:
        if get_user_step(cid) == 13:
            receipt_image_file_id = message.photo[-1].file_id
            edit_reception_receipt_image_file_id(receipt_image_file_id=receipt_image_file_id, id=reception_id_dict['id'])
            bot.send_message(cid, text_user['send_receipt_success'])
            reception_id_dict.clear()
            user_steps[cid] = 0
        else:
            unknown_message(message)


@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    cid = message.chat.id
    bot.send_message(cid, text['unknown_message'])


users = get_member_user()
bot.infinity_polling()
