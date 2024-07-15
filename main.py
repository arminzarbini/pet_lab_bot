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
test_group_dict = dict() #{id : id}
test = dict() # {test_group_id : ... , parameter : ..., type : ... , price : ... , unit : ..., minimum_range : ... , maximum_range : ... , analyze_date : ..., description : ...}
breed = dict() # {species : ..., name : ..., specifications : ...}
breed_id_dict = dict() #{breed_id : breed_id}
pet_id_dict = dict() #{'id' : id}
pet_reception = dict() #{id : {test_id,...}}
reception_id_dict = dict() #{id : id}
result_id_dict = dict()  #{id : id}
test_id_dict = dict() #{id : id}
species_enum = ['cat', 'dog', 'bird', 'rabbit', 'rat', 'other'] #ENUM for species in breed table
gender_enum = ['male', 'female'] #ENUM for gender in pet table
quality_enum = ['negative', 'positive'] #ENUM for result quality in result table
type_enum = ['quantity', 'quality']

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

def is_valid_datetime(str_datetime): #check persian datetime string : year/month/day hour:minute:second
    try:
        persian_date = jdatetime.datetime.strptime(str_datetime, '%Y/%m/%d %H:%M:%S')
    except:
        return False
    else:
        gregorian_date = jdatetime.datetime.togregorian(persian_date)
        return gregorian_date

def is_valid_date(str_date): #check persian date string : year/month/day
    try:
        persian_date = datetime.datetime.strptime(str_date, '%Y/%m/%d')
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

def reception_test_markup(pet_id): #generate markup test item for choose or remove and order and return
    markup = InlineKeyboardMarkup()
    for item in show_test():
        if item['id'] in pet_reception[pet_id]:
            markup.add(InlineKeyboardButton(f"🧪{text_user['parameter']}:{item['parameter']}-{text_user['price']}:{item['price']}{text_user['toman']}🧪", callback_data=f"remove_test_{item['id']}_{pet_id}"))
        else:
            markup.add(InlineKeyboardButton(f"{text_user['parameter']}:{item['parameter']}-{text_user['price']}:{item['price']}{text_user['toman']}", callback_data=f"choose_test_{item['id']}_{pet_id}"))
    markup.add(InlineKeyboardButton(text_user['order'], callback_data=f"order_{pet_id}"))
    markup.add(InlineKeyboardButton(text['return'], callback_data='return_pet_markup'))
    return markup

def show_reception_markup(cid): #generate markup reception item for user
    markup = InlineKeyboardMarkup()
    for item in show_reception_user(cid):
        if item['code'] == None:
            persian_date_str = show_persian_date(item['request_date'])
            markup.add(InlineKeyboardButton(f"{text_user['test']} {item['name']} {text_user['reception_request_date']}:{persian_date_str}", callback_data=f"reception_{item['id']}"))
        else:
            persian_date_str = show_persian_date(item['reception_date'])
            markup.add(InlineKeyboardButton(f"{text_user['test']} {item['name']} {text_user['reception_reception_date']}:{persian_date_str} {text_user['reception_code']} {item['code']}", callback_data=f"reception_{item['id']}"))
    return markup

def reception_receipt_markup(reception_id): #generate markup receptit and return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text_user['send_receipt'], callback_data=f"send_receipt_{reception_id}"))
    markup.add(InlineKeyboardButton(text['return'], callback_data='return_reception_markup'))
    return markup

def show_reception_code(cid): #generate markup code for get result
    markup = InlineKeyboardMarkup()
    for item in show_reception_user(cid):
        if item['code'] != None:
            markup.add(InlineKeyboardButton(item['code'], callback_data=f"result_code_{item['id']}"))
    return markup
    
def show_reception_code_test(reception_id): #generate markup test for get result
    markup = InlineKeyboardMarkup()
    for item in show_reception_test(reception_id):
        markup.add(InlineKeyboardButton(item['parameter'], callback_data=f"result_test_{item['test_id']}_{item['id']}"))
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
        markup.add(InlineKeyboardButton(f"{item['code']}-{item['name']}-{item['username']}", callback_data=f"reception_{item['name']}_{item['id']}"))
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
    markup.add(InlineKeyboardButton(text_admin['send_result'], callback_data=f"send_result_{reception_id}"))
    markup.add(InlineKeyboardButton(text['return'], callback_data='return_reception_markup'))    
    return markup
    
def send_result_markup(reception_id): #generate markup send result
    markup = InlineKeyboardMarkup()
    for item in show_reception_test(reception_id):
        markup.add(InlineKeyboardButton(item['parameter'], callback_data=f"send_test_result_{reception_id}_{item['test_id']}_{item['id']}"))
    markup.add(InlineKeyboardButton(text['return'], callback_data=f"return_reception_edit_markup_{reception_id}"))
    return markup

def send_test_result_markup(reception_id, reception_test_id, test_id, test_type): #generate markup send result test item
    markup = InlineKeyboardMarkup()
    for key,value in show_result_data(reception_test_id).items():
        if key == 'id':
            result_id = value
            continue
        elif test_type == 'quantity' and key == 'result_quality':
            continue
        elif test_type == 'quality' and (key == 'result_quantity' or key == 'analysis'):
            continue
        elif isinstance(value, datetime.datetime):
            persian_datetime_str = show_persian_datetime(value)
            markup.add(InlineKeyboardButton(f"{text_admin[key]} : {persian_datetime_str}", callback_data=f"{key}_edit_{test_id}_{result_id}"))
        elif value == None:
            markup.add(InlineKeyboardButton(f"{text_admin[key]}", callback_data=f"{key}_edit_{test_id}_{result_id}"))
        else:
            markup.add(InlineKeyboardButton(f"{text_admin[key]} : {value}", callback_data=f"{key}_edit_{test_id}_{result_id}"))
    markup.add(InlineKeyboardButton(text['return'], callback_data=f"return_send_result_markup_{reception_id}"))
    return markup
    
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    call_id = call.id
    data = call.data
    if cid in admins:
        if data.startswith('edit_group_test'): #admin : edit test group name with step 1.1
            test_group_id = int(data.split('_')[-1])
            test_group_dict.update({'id': test_group_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_admin['test_group_name'])
            user_steps[cid] = 1.1
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('test_group'):  #admin : create test with step 2
            test_group_id = int(data.split('_')[-1])
            test.update({'test_group_id': test_group_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_admin['template_test'])
            bot.send_message(cid, text_admin['template_test_input'])
            user_steps[cid] = 2
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('edit_select_test_group_test'): #admin : edit test with select parameter
            test_group_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            markup = InlineKeyboardMarkup()
            for item in show_test_test_group(test_group_id):
                markup.add(InlineKeyboardButton(item['parameter'], callback_data=f"edit_test_{item['id']}"))
            bot.send_message(cid, text_admin['edit_test'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('edit_test'): #admin : edit test with select items
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            markup = InlineKeyboardMarkup()
            for key,value in show_test_data(test_id).items():
                if key == 'id' or key == 'test_group_id':
                    continue
                elif value == None:
                    markup.add(InlineKeyboardButton(f"{text_admin[key]}", callback_data=f"{key}_edit_{test_id}"))
                else:
                    markup.add(InlineKeyboardButton(f"{text_admin[key]} : {value}", callback_data=f"{key}_edit_{test_id}"))
            bot.send_message(cid, text_admin['test_information'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('parameter_edit'): # admin : edit test parameter with step 2.1
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            test_id_dict.update({'id': test_id})
            bot.send_message(cid, text_admin['test_parameter'])
            user_steps[cid] = 2.1
        elif data.startswith('type_edit'): #admin : edit test type with select quality or quantity
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            markup = InlineKeyboardMarkup()
            for item in type_enum:
                markup.add(InlineKeyboardButton(text_admin[item], callback_data=f"{item}_{test_id}"))
            bot.send_message(cid, text_admin['test_type'], reply_markup=markup)
        elif data.startswith('quantity') or data.startswith('quality'): #admin : edit test type
            test_id = int(data.split('_')[-1])
            type = data.split('_')[0]
            edit_test_type(type=type, id=test_id)
            bot.send_message(cid, text_admin['test_type_success'])
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('price_edit'): #admin : edit test type with step 2.2
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            test_id_dict.update({'id': test_id})
            bot.send_message(cid, text_admin['test_price'])
            user_steps[cid] = 2.2
        elif data.startswith('unit_edit'): #admin : edit test unit with step 2.3
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            test_id_dict.update({'id': test_id})
            bot.send_message(cid, text_admin['test_unit'])
            user_steps[cid] = 2.3
        elif data.startswith('minimum_range_edit'): #admin : edit test minimum_range with step 2.4
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            test_id_dict.update({'id': test_id})
            bot.send_message(cid, text_admin['test_minimum_range'])
            user_steps[cid] = 2.4
        elif data.startswith('maximum_range_edit'): #admin : edit test maximum_range with step 2.5
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            test_id_dict.update({'id': test_id})
            bot.send_message(cid, text_admin['test_maximum_range'])
            user_steps[cid] = 2.5
        elif data.startswith('analyze_date_edit'): #admin : edit test analyze_date with step 2.6
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            test_id_dict.update({'id': test_id})
            bot.send_message(cid, text_admin['test_analyze_date'])
            user_steps[cid] = 2.6
        elif data.startswith('description_edit'): #admin : edit test description with step 2.7
            test_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            test_id_dict.update({'id': test_id})
            bot.send_message(cid, text_admin['test_description'])
            user_steps[cid] = 2.7
        elif data in species_enum: #admin : create breed with step 3
            breed.update({'species': data})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_admin['breed_name'])
            user_steps[cid] = 3
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data == 'no_specifications_breed':  #admin : create breed without specifications
            insert_breed_data(species=breed['species'], name=breed['name'], specifications=None)
            markup = send_home()
            bot.send_message(cid, text_admin['create_breed_success'].format(breed['name']), reply_markup=markup)
            breed.clear()
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data == 'yes_specifications_breed': #admin : create breed with specifications
            bot.send_message(cid, text_admin['breed_specifications'])
            user_steps[cid] = 3.1
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('edit_species_breed'): #admin : edit breed with select breed
            species = data.split('_')[-1]
            markup = InlineKeyboardMarkup()
            for item in show_breed(species):
                markup.add(InlineKeyboardButton(item['name'], callback_data=f"edit_breed_{item['id']}"))
            bot.send_message(cid, text_admin['edit_breed'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('edit_breed'): # admin : edit breed with select items
            breed_id = int(data.split('_')[-1])
            markup = InlineKeyboardMarkup()
            for key,value in show_breed_data(breed_id).items():
                if value == None:
                    markup.add(InlineKeyboardButton(f"{text[key]}", callback_data=f"{key}_edit_{breed_id}"))
                else:
                    markup.add(InlineKeyboardButton(f"{text[key]} : {value}", callback_data=f"{key}_edit_{breed_id}"))
            bot.send_message(cid, text_admin['breed_information'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('breed_name_edit'): #admin : edit breed with step 3.2
            breed_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            breed_id_dict.update({'breed_id': breed_id})
            bot.send_message(cid, text_admin['breed_name'])
            user_steps[cid] = 3.2
        elif data.startswith('specifications_edit'): #admin : edit breed with step 3.3
            breed_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            breed_id_dict.update({'breed_id': breed_id})
            bot.send_message(cid, text_admin['breed_specifications'])
            user_steps[cid] = 3.3
        elif data.startswith('request'): #admin : show request data
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
                bot.send_message(cid, f"❎{item['parameter']}❎")
            if comment != None:
                bot.send_message(cid, text['comment'].format(comment))
            bot.send_message(cid, f"{text_user['total_price']} {total_price}{text_user['toman']}")
            if receipt_image != None:
                bot.send_photo(cid, receipt_image, text_admin['receipt'])
        elif data == 'return_request_markup': #admin : return to select requests
            markup = request_markup()
            bot.send_message(cid, text_admin['requests_test'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('reception'): #admin : show reception data
            reception_id = int(data.split('_')[-1])
            pet_name = data.split('_')[-2]
            markup = reception_edit_markup(reception_id)
            bot.edit_message_text(text_admin['reception_edit'],cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data == 'return_reception_markup': #admin : return to select reception
            markup = reception_markup()
            bot.edit_message_text(text_admin['reception_test'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('code_edit'): #admin : create code and reception date and answer date
            reception_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            code = ''.join(random.choices(string.digits + string.ascii_uppercase, k=5)) #generate random reception code (0-9 + uppercase)
            if check_reception_code(code):
                bot.send_message(cid, text_admin['reception_code_try_again'])
            else:
                reception_date = datetime.datetime.now() #calculate reception date
                edit_reception_code_date(code=code, reception_date=reception_date, id=reception_id)
                if (check_reception_test_analyze_date(reception_id)) != None: 
                    analyze_date = check_reception_test_analyze_date(reception_id) #calculate maximum analyze date
                    answer_date = reception_date + datetime.timedelta(analyze_date) #calculate answer date
                    edit_reception_answer_date(answer_date=answer_date, id=reception_id)
                bot.send_message(cid, text_admin['reception_code_success'])
        elif data.startswith('answer_date_edit'): #admin : edit answer data with step 4
            reception_id = int(data.split('_')[-1])
            reception_id_dict.update({'id': reception_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_admin['reception_answer_date_edit'])
            user_steps[cid] = 4
        elif data.startswith('send_result'): #admin : select reception_test for create result
            reception_id = int(data.split('_')[-1])
            markup = send_result_markup(reception_id)
            bot.edit_message_text(text_admin['send_result'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('return_reception_edit_markup'): #admin : return to reception edit
            reception_id = int(data.split('_')[-1])
            markup = reception_edit_markup(reception_id)
            bot.edit_message_text(text_admin['reception_edit'],cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('send_test_result'):  #admin : create result
            reception_test_id = int(data.split('_')[-1])
            test_id = int(data.split('_')[-2])
            reception_id = int(data.split('_')[-3])
            insert_result_data(reception_test_id=reception_test_id)
            test_type = show_test_type_range(test_id)['type']
            markup = send_test_result_markup(reception_id, reception_test_id, test_id, test_type)
            bot.edit_message_text(text_admin['result_edit'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('return_send_result_markup'): #admin : return to select reception_test for create result
            reception_id = int(data.split('_')[-1])
            markup = send_result_markup(reception_id)
            bot.edit_message_text(text_admin['send_result'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)           
        elif data.startswith('result_date_edit'): #admin : edit result date with step 5
            result_id = int(data.split('_')[-1])
            result_id_dict.update({'id': result_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_admin['result_date_edit'])
            user_steps[cid] = 5
        elif data.startswith('result_quantity_edit'): #admin : edit result quantity with step 5.1
            result_id = int(data.split('_')[-1])
            test_id = int(data.split('_')[-2])
            result_id_dict.update({'id': result_id})
            test_id_dict.update({'id': test_id})
            bot.send_message(cid, text_admin['result_quantity_edit'])
            minimum_range = show_test_type_range(test_id_dict['id'])['minimum_range']
            maximum_range = show_test_type_range(test_id_dict['id'])['maximum_range']
            bot.send_message(cid, f"minimum range : {minimum_range}\nmaximum_range : {maximum_range}")
            user_steps[cid] = 5.1
        elif data.startswith('result_quality_edit'): #admin : select result quality with quality enum
            result_id = int(data.split('_')[-1])
            markup = InlineKeyboardMarkup()
            for item in quality_enum:
                markup.add(InlineKeyboardButton(text_admin[item], callback_data=f"{item}_{result_id}"))
            bot.edit_message_text(text_admin['result_quality_edit'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('positive') or data.startswith('negative'): #admin : edit result quality
            result_id = int(data.split('_')[-1])
            result_quality = data.split('_')[0]
            edit_result_quality(result_quality=result_quality, id=result_id)
            bot.send_message(cid, text_admin['result_quality_success'])
        elif data.startswith('conclusion_edit'): # admin : edit conclusion edit with step 5.2
            result_id = int(data.split('_')[-1])
            result_id_dict.update({'id': result_id})
            bot.send_message(cid, text_admin['result_conclusion_edit'])
            user_steps[cid] = 5.2
        elif data.startswith('information_user'): #admin : show user data and pet buttons
            user_id = int(data.split('_')[-1])
            for key, value in show_user_data(user_id).items():
                if value == None:
                    bot.send_message(cid, f"{text[key]} : ...")
                else:
                    bot.send_message(cid, f"{text[key]} : {value}")
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            markup = InlineKeyboardMarkup()
            for item in show_user_all_pet_data(user_id):
                markup.add(InlineKeyboardButton(f"{item['name']}", callback_data=f"information_pet_{item['id']}"))
            bot.send_message(cid, text_admin['choose_pet'], reply_markup=markup)
        elif data.startswith('information_pet'): #admin : show pet data
            pet_id = int(data.split('_')[-1])
            for key, value in show_user_pet_data(pet_id).items():
                if value == None:
                    bot.send_message(cid, f"{text[key]} : ...")
                elif isinstance(value, datetime.date):
                    persian_date_str = show_persian_date(value)
                    bot.send_message(cid, f"{text[key]} : {persian_date_str}")
                else:
                    bot.send_message(cid, f"{text[key]} : {value}")
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data == 'search_username': #admin : search username with step 6
            bot.send_message(cid, text_admin['enter_username'])
            user_steps[cid] = 6
            try:
                bot.delete_message(cid, mid)
            except:
                pass   
    else:
        if data == 'first_name_edit': #user : edit first name with step 10.1
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['first_name_edit'])
            user_steps[cid] = 10.1
        elif data == 'last_name_edit': #user : edit last name with step 10.2
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['last_name_edit'])
            user_steps[cid] = 10.2
        elif data == 'username_edit': #user : edit username with step 10.3
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['username_edit'])
            user_steps[cid] = 10.3
        elif data == 'national_code_edit': #user : edit national code with step 10.4
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['national_code_edit'])
            user_steps[cid] = 10.4 
        elif data == 'phone_edit': #user : edit phone with step 10.5
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['phone_edit'])
            user_steps[cid] = 10.5
        elif data == 'address_edit': #user : edit address with step 10.6
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['address_edit'])
            user_steps[cid] = 10.6
        elif data in species_enum: #user : create pet with select breed
            markup = InlineKeyboardMarkup()
            for item in show_breed(data):
                markup.add(InlineKeyboardButton(item['name'], callback_data=f"choose_breed_{item['id']}"))
            bot.edit_message_text(text_user['choose_breed'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('choose_breed'): #user : create pet with step 11
            breed_id = int(data.split('_')[-1])
            breed_id_dict.update({'breed_id': breed_id})
            bot.send_message(cid, text_user['pet_name'])
            user_steps[cid] = 11
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('edit_gender'): #user : edit gender with select gender enum
            pet_id = int(data.split('_')[-1])
            bot.answer_callback_query(call_id, '✅')
            markup = InlineKeyboardMarkup()
            for item in gender_enum:
                markup.add(InlineKeyboardButton(text_user[item], callback_data=f"{item}_{pet_id}"))
            bot.send_message(cid, text_user['pet_gender_edit'], reply_markup=markup)
        elif data.startswith('male') or data.startswith('female'): #user : edit gender
            pet_id = int(data.split('_')[-1])
            gender = data.split('_')[0]
            markup = send_home()
            edit_pet_gender(gender=gender, user_id=cid, id=pet_id)
            bot.send_message(cid, text_user['pet_gender_success'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('edit_birth_date'): #user : edit gender with step 11.1
            pet_id = int(data.split('_')[-1])
            pet_id_dict.update({'id': pet_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['pet_birth_date_edit'])
            user_steps[cid] = 11.1
        elif data.startswith('edit_weight'): #user : edit weight with step 11.2
            pet_id = int(data.split('_')[-1])
            pet_id_dict.update({'id': pet_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['pet_weight_edit'])
            user_steps[cid] = 11.2
        elif data.startswith('edit_personality'): #user : edit personality with step 11.3
            pet_id = int(data.split('_')[-1])
            pet_id_dict.update({'id': pet_id})
            bot.answer_callback_query(call_id, '✅')
            bot.send_message(cid, text_user['pet_personality_edit'])
            user_steps[cid] = 11.3
        elif data.startswith('choose_pet'): #user : create reception with select tests
            pet_id = int(data.split('_')[-1])
            pet_reception.setdefault(pet_id, set())
            bot.answer_callback_query(call_id, '✅')
            markup = reception_test_markup(pet_id)
            bot.edit_message_text(text_user['choose_test'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('choose_test'): #user : add test
            pet_id = int(data.split('_')[-1])
            test_id = int(data.split('_')[-2])
            pet_reception[pet_id].add(test_id)
            markup = reception_test_markup(pet_id)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('remove_test'): #user : remove test
            pet_id = int(data.split('_')[-1])
            test_id = int(data.split('_')[-2])
            pet_reception[pet_id].remove(test_id)
            markup = reception_test_markup(pet_id)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith("order"): #user : comment for recpetion
            pet_id = int(data.split('_')[-1])
            if len(pet_reception[pet_id]) == 0:
                bot.answer_callback_query(call_id, '❌')
                bot.send_message(cid, text_user['no_choose_test'])
            else:
                bot.answer_callback_query(call_id, '✅')
                markup = InlineKeyboardMarkup() #markup for reception comment with yes and no
                markup.add(InlineKeyboardButton(text['no'], callback_data=f"no_reception_comment_{pet_id}"), InlineKeyboardButton(text['yes'], callback_data=f"yes_reception_comment_{pet_id}"))
                bot.send_message(cid, text_user['reception_comment'], reply_markup=markup)
                try:
                    bot.delete_message(cid, mid)
                except:
                    pass
        elif data == 'return_pet_markup': #user : return to select pet for create reception
            markup = reception_pet_markup(cid)
            bot.edit_message_text(text_user['choose_pet'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('no_reception_comment'): #user : create reception with no comment and reception_test
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
        elif data.startswith('yes_reception_comment'): #user : create reception comment with step 12
            pet_id = int(data.split('_')[-1])   
            pet_id_dict.update({'id': pet_id})
            bot.send_message(cid, text_user['reception_comment_input'])
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            user_steps[cid] = 12
        elif data.startswith('reception'): #user : show request or reception data and send receipt
            reception_id = int(data.split('_')[-1])
            comment = show_reception_comment(reception_id)
            answer_date = show_reception_answer_date(reception_id)
            total_price = show_reception_price(reception_id)
            markup = reception_receipt_markup(reception_id)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
            for item in show_reception_test(reception_id):
                bot.send_message(cid, f"❎{item['parameter']}❎")
            if comment != None:
                bot.send_message(cid, text['comment'].format(comment))
            if answer_date != None:
                bot.send_message(cid, text_user['reception_answer_date'].format(show_persian_date(answer_date)))
            bot.send_message(cid, f"{text_user['total_price']} {total_price}{text_user['toman']}")
        elif data == 'return_reception_markup': #user : return to manage reception
            markup = show_reception_markup(cid)
            bot.send_message(cid, text_user['reception_manage'], reply_markup=markup)
            try:
                bot.delete_message(cid, mid)
            except:
                pass
        elif data.startswith('send_receipt'): #user : send receipt image with step 13
            reception_id = int(data.split('_')[-1])
            reception_id_dict.update({'id': reception_id})
            bot.send_message(cid, text_user['send_receipt_image'])
            user_steps[cid] = 13
        elif data.startswith('result_code'): #user : select reception code for show result
            reception_id = int(data.split('_')[-1])
            markup = show_reception_code_test(reception_id)
            bot.edit_message_text(text_user['test'], cid, mid)
            bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        elif data.startswith('result_test'): #user : select test for show result
            try:
                bot.delete_message(cid, mid)
            except:
                pass
            reception_test_id = int(data.split('_')[-1])
            test_id = int(data.split('_')[-2])
            test_type = show_test_type_range(test_id)['type']
            if len(show_result_user(reception_test_id)) == 0:
                bot.send_message(cid, text_user['result_not_ready'])
            else:
                for item in show_result_user(reception_test_id):
                    result_date_str = show_persian_datetime(item['date'])
                    if test_type == 'quality':
                        if item['result_quality'] == None:
                            bot.send_message(cid, text_user['result_not_ready'])
                            break
                        else:
                            if item['conclusion'] != None:
                                bot.send_message(cid, f"{text_user['result_date']} : {result_date_str}\n{text_user['result_quality']} : {item['result_quality']}\n{text_user['result_conclusion']} : {item['conclusion']}")
                            else:
                                bot.send_message(cid, f"{text_user['result_date']} : {result_date_str}\n{text_user['result_quality']} : {item['result_quality']}")
                    elif test_type == 'quantity':
                        if item['result_quantity'] == None:
                            bot.send_message(cid, text_user['result_not_ready'])
                            break
                        else:
                            minimum_range = show_test_type_range(test_id)['minimum_range']
                            maximum_range = show_test_type_range(test_id)['maximum_range']
                            if item['conclusion'] != None:
                                bot.send_message(cid, f"{text_user['result_date']} : {result_date_str}\n{text_user['minimum_range']} : {minimum_range}\n{text_user['maximum_range']} : {maximum_range}\n{text_user['result_quantity']} : {item['result_quantity']}\n{text_user['result_analysis']} : {item['analysis']}\n{text_user['result_conclusion']} : {item['conclusion']}")
                            else:
                                bot.send_message(cid, f"{text_user['result_date']} : {result_date_str}\n{text_user['minimum_range']} : {minimum_range}\n{text_user['maximum_range']} : {maximum_range}\n{text_user['result_quantity']} : {item['result_quantity']}\n{text_user['result_analysis']} : {item['analysis']}")
                           

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
            insert_user_data(cid=cid, first_name=first_name, last_name=last_name, username=None, national_code=None, phone=None, address=None) #create user if not exist
        else:
            pass
  

@bot.message_handler(commands=['home'])
def home_command(message):
    cid = message.chat.id
    if cid in admins:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons_admin['create_test'], buttons_admin['create_test_group'],)
        markup.add(buttons_admin['edit_test'], buttons_admin['edit_test_group'])
        markup.add(buttons_admin['edit_breed'], buttons_admin['create_breed'])
        markup.add(buttons_admin['reception_manage'], buttons_admin['request_manage'])
        markup.add(buttons_admin['username_infomration'])
        bot.send_message(cid, text['home'], reply_markup=markup)
        user_steps[cid] = 0
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add( buttons_user['pets'], buttons_user['account'])
        markup.add(buttons_user['reception_manage'], buttons_user['reception_request'])
        markup.add(buttons_user['recieve_result'])
        bot.send_message(cid, text['home'], reply_markup=markup)
        user_steps[cid] = 0


@bot.message_handler(func=lambda message: message.text==buttons['home'])
def home_handler(message):
    cid = message.chat.id
    if cid in admins:
        home_command(message)
    else:
        home_command(message)


@bot.message_handler(func=lambda message: message.text==buttons_user['account']) #user : edit user information with select items
def account_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = InlineKeyboardMarkup()
        for key,value in show_user_data(cid).items(): #generate markup for edit user information
            if value == None:
                markup.add(InlineKeyboardButton(f"{text[key]}", callback_data=f"{key}_edit"))
            else :
                markup.add(InlineKeyboardButton(f"{text[key]} : {value}", callback_data=f"{key}_edit"))
        bot.send_message(cid, text_user['user_information'], reply_markup=markup)
        markup = send_home()
        bot.send_message(cid, text_user['user_data_edit'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_user['pets']) #user : create pet or edit pet data with select buttons
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


@bot.message_handler(func=lambda message:message.text==buttons_user['create_pet']) #user : create pet with select species
def create_pet_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = InlineKeyboardMarkup()
        for item in species_enum:
            markup.add(InlineKeyboardButton(text[item], callback_data=item))
        bot.send_message(cid, text['choose_species'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text in show_pet(message.chat.id)) #user : edit pet data with select items
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
                markup.add(InlineKeyboardButton(f"{text[key]} : {persian_date_str}", callback_data=f"edit_{key}_{pet_id}"))
            elif key == 'gender' and value in gender_enum:
                markup.add(InlineKeyboardButton(f"{text[key]} : {text_user[value]}", callback_data=f"edit_{key}_{pet_id}"))
            elif value == None:
                markup.add(InlineKeyboardButton(f"{text[key]}", callback_data=f"edit_{key}_{pet_id}"))
            else:
                markup.add(InlineKeyboardButton(f"{text[key]} : {value}", callback_data=f"edit_{key}_{pet_id}"))
        bot.send_message(cid, text_user['pet_data'].format(name), reply_markup=markup)
        markup = send_home()
        bot.send_message(cid, text_user['pet_data_edit'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_user['reception_request']) #user : create reception with select pet
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


@bot.message_handler(func=lambda message:message.text==buttons_user['reception_manage']) #user : manage reception
def reception_manage_user_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = show_reception_markup(cid)
        bot.send_message(cid, text_user['reception_manage'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_user['recieve_result']) #user : select code for get result
def recieve_result_handler(message):
    cid = message.chat.id
    if cid not in admins:
        markup = show_reception_code(cid)
        bot.send_message(cid, text_user['reception_code'], reply_markup=markup)
    else:
        unknown_message(message)
        

@bot.message_handler(func=lambda message: message.text==buttons_admin['create_test_group']) #admin : create test group with step 1 
def create_test_group_handler_button(message):
    cid = message.chat.id
    if cid in admins:
        bot.send_message(cid, text_admin['test_group_name'])
        user_steps[cid] = 1
    else :
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['edit_test_group']) #admin : edit test group with select test group name
def edit_test_group_handler_button(message):
    cid = message.chat.id
    if cid in admins:
        markup = InlineKeyboardMarkup()
        for item in show_test_group():
            markup.add(InlineKeyboardButton(item['name'], callback_data=f"edit_group_test_{item['id']}"))
        bot.send_message(cid, text_admin['test_group_edit'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['create_test']) #admin : create test group with select test group name
def create_test_handler_button(message):
    cid = message.chat.id
    if cid in admins:
        if check_test_group_exists(): #check for test group exist
            markup = send_home()
            bot.send_message(cid, text_admin['test_group_not_exist'] ,reply_markup=markup)
        else :
            markup = InlineKeyboardMarkup()
            for item in show_test_group():
                markup.add(InlineKeyboardButton(item['name'], callback_data=f"test_group_{item['id']}"))
            bot.send_message(cid, text_admin['choose_test_group'], reply_markup=markup)
    else :
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['edit_test']) #admin : edit test with select test group name
def edit_test_handler_button(message):
    cid = message.chat.id
    if cid in admins:
        markup = InlineKeyboardMarkup()
        for item in show_test_group():
            markup.add(InlineKeyboardButton(item['name'], callback_data=f"edit_select_test_group_test_{item['id']}"))
        bot.send_message(cid, text_admin['edit_test_test_group'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['create_breed']) #admin : create breed with select species enum
def create_breed_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = InlineKeyboardMarkup()
        for item in species_enum:
            markup.add(InlineKeyboardButton(text[item], callback_data=item))
        bot.send_message(cid, text['choose_species'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['edit_breed']) #admin : edit breed with select species enum
def edit_breed_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = InlineKeyboardMarkup()
        for item in species_enum:
            markup.add(InlineKeyboardButton(text[item], callback_data=f"edit_species_breed_{item}"))
        bot.send_message(cid, text['choose_species'], reply_markup=markup)
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:message.text==buttons_admin['request_manage']) #admin : check and confirm requests
def request_manage_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = request_markup()
        bot.send_message(cid, text_admin['requests_test'], reply_markup=markup)
    else:
        unknown_message(message)
    

@bot.message_handler(func=lambda message:message.text==buttons_admin['reception_manage']) #admin : manage reception
def reception_manage_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = reception_markup()
        bot.send_message(cid,text_admin['reception_test'], reply_markup=markup)
    else:
        unknown_message(message)

@bot.message_handler(func=lambda message:message.text==buttons_admin['username_infomration']) #admin : show usernames and search
def username_information_handler(message):
    cid = message.chat.id
    if cid in admins:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text_admin['search_username'], callback_data="search_username"))
        for item in show_all_user_data():
            markup.add(InlineKeyboardButton(item['username'], callback_data=f"information_user_{item['cid']}"))
        bot.send_message(cid, text_admin['choose_username'], reply_markup=markup)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1) #admin : create test group
def create_test_group_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        if check_test_group_name(name):
            bot.send_message(cid, text_admin['test_group_name_unique'])
        elif len(name) > 45:
            bot.send_message(cid, text_admin['test_group_name_check'])
        else:
            markup = send_home()
            insert_test_group_data(name=name)
            bot.send_message(cid, text_admin['create_test_group_success'].format(name), reply_markup=markup)
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==1.1) #admin : edit test group
def edit_test_group_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        if check_test_group_name(name):
            bot.send_message(cid, text_admin['test_group_name_unique'])
        elif len(name) > 45:
            bot.send_message(cid, text_admin['test_group_name_check'])
        else:
            markup = send_home()
            edit_test_group_name(name=name, id=test_group_dict['id'])
            bot.send_message(cid, text_admin['edit_test_group_success'], reply_markup=markup)
            test_group_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id)==2) #admin : create test
def create_test_handler(message):
    cid = message.chat.id
    if cid in admins:
        item_test_check = ['parameter', 'type', 'price', 'unit', 'minimum_range', 'maximum_range', 'analyze_date', 'description']
        item_test = message.text.split('\n')
        item_check = dict()
        for item in item_test :
            item_check.setdefault(item.split(':')[0],  item.split(':')[-1])
        if len(item_test_check) != len(item_check.keys()): #check to enter all items
            bot.send_message(cid, text_admin['send_full_test_item']) 
        elif item_test_check != list(item_check.keys()): #check to enter wrong items
            bot.send_message(cid, text_admin['test_item_check'])
        else:
            for key,value in item_check.items():  
                if key == 'parameter':
                    parameter = value
                    if parameter == "":
                        bot.send_message(cid, text_admin['test_parameter_null'])
                        break
                    else :
                        if check_test_parameter(parameter):
                            bot.send_message(cid, text_admin['test_parameter_unique'])
                            break
                        elif len(parameter) > 45:
                            bot.send_message(cid, text_admin['test_parameter_check'])
                            break
                        else :
                            test.update({key: parameter})
                elif key == 'type':
                    type = value
                    if type == "":
                        bot.send_message(cid, text_admin['test_type_null'])
                        break
                    else:
                        if type == 'quality' or type == 'quantity':
                            test.update({key: type})
                        else : 
                            bot.send_message(cid, text_admin['test_type_check'])
                            break
                elif key == 'price':
                    price = value
                    if price == "":
                        bot.send_message(cid, text_admin['test_price_null'])
                        break
                    else:
                        if price.isnumeric() == True and len(price) <= 10:
                            test.update({key: price})
                        else:
                            bot.send_message(cid, text_admin['test_price_check'])
                            break
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
                    if minimum_range == "" and test['type'] == 'quantity':
                        bot.send_message(cid, text_admin['test_type_minimum_range'])
                    elif minimum_range == "" and test['type'] == 'quality':
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
                    if maximum_range == "" and test['type'] == 'quantity':
                        bot.send_message(cid, text_admin['test_type_maximum_range'])
                    elif maximum_range == "" and test['type'] == 'quality':
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
                        if analyze_date.isnumeric() == True and 1 <= int(analyze_date) <= 90:
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
        if test['minimum_range'] >= test['maximum_range']:
            bot.send_message(cid, text_admin['minium_maximum_range'])
            test_group_dict.update({'id': test['test_group_id']})
            test.clear()
            test.update({'test_group_id': test_group_dict['id']})
            test_group_dict.clear()
        elif text['maximum_range'] <= test['minimum_range']:
            bot.send_message(cid, text_admin['maximum_minimum_range'])
            test_group_dict.update({'id': test['test_group_id']})
            test.clear()
            test.update({'test_group_id': test_group_dict['id']})
            test_group_dict.clear()
        else:
            if len(test) == 9:
                markup = send_home()
                insert_test_data(**test)
                bot.send_message(cid, text_admin['create_test_success'].format(test['parameter']), reply_markup=markup)
                test.clear()
                user_steps[cid] = 0
            else:
                test_group_dict.update({'id': test['test_group_id']})
                test.clear()
                test.update({'test_group_id': test_group_dict['id']})
                test_group_dict.clear()         
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==2.1) #admin : edit test parameter
def edit_test_parameter_handler(message):
    cid = message.chat.id
    if cid in admins:
        parameter = message.text
        if check_test_parameter(parameter):
            bot.send_message(cid, text_admin['test_parameter_unique'])
        elif len(parameter) > 45:
            bot.send_message(cid, text_admin['test_parameter_check'])
        else:
            edit_test_parameter(parameter=parameter, id=test_id_dict['id'])
            bot.send_message(cid, text_admin['test_parameter_success'])
            test_id_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==2.2) #admin : edit test price
def edit_test_price_handler(message):
    cid = message.chat.id
    if cid in admins:
        price = message.text
        if price.isnumeric() == True and len(price) <= 10:
            edit_test_price(price=price, id=test_id_dict['id'])
            bot.send_message(cid, text_admin['test_price_success'])
            test_id_dict.clear()
            user_steps[cid] = 0
        else:
            bot.send_message(cid, text_admin['test_price_check'])    
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==2.3) #admin : edit test unit
def edit_test_unit_handler(message):
    cid = message.chat.id
    if cid in admins:
        unit = message.text
        if len(unit) > 10:
            bot.send_message(cid, text_admin['test_unit_check'])
        else: 
            edit_test_unit(unit=unit, id=test_id_dict['id'])
            bot.send_message(cid, text_admin['test_unit_success'])
            test_id_dict.clear()
            user_steps[cid] = 0


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==2.4) #admin : edit test minimum_range
def edit_test_minimum_range_handler(message):
    cid = message.chat.id
    if cid in admins:
        minimum_range = message.text
        try:
            minimum_range = float(minimum_range)
        except:
            bot.send_message(cid, text_admin['test_minimum_range_check'])
        else:
            if len(str(minimum_range).split('.')[0]) > 5 or len(str(minimum_range).split('.')[-1]) > 3 :
                bot.send_message(cid, text_admin['test_minimum_range_check'])
            else:
                maximum_range = show_test_type_range(test_id_dict['id'])['maximum_range']
                if maximum_range != None:
                    if minimum_range >= maximum_range:
                        bot.send_message(cid, text_admin['minium_maximum_range'])
                    else:
                        edit_test_minimum_range(minimum_range=minimum_range, id=test_id_dict['id'])
                        bot.send_message(cid, text_admin['test_minimum_range_success'])
                        test_id_dict.clear()
                        user_steps[cid] = 0
    else:
        unknown_message(message)
            

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==2.5) #admin : edit test maximum_range
def edit_test_maximum_range_handler(message):
    cid = message.chat.id
    if cid in admins:
        maximum_range = message.text
        try:
            maximum_range = float(maximum_range)
        except:
            bot.send_message(cid, text_admin['test_maximum_range_check'])
        else:
            if len(str(maximum_range).split('.')[0]) > 5 or len(str(maximum_range).split('.')[-1]) > 3 :
                bot.send_message(cid, text_admin['test_maximum_range_check'])
            else:
                minimum_range = show_test_type_range(test_id_dict['id'])['minimum_range']
                if minimum_range != None:
                    if maximum_range <= minimum_range:
                        bot.send_message(cid, text_admin['maximum_minimum_range'])
                    else:
                        edit_test_maximum_range(maximum_range=maximum_range, id=test_id_dict['id'])
                        bot.send_message(cid, text_admin['test_maximum_range_success'])
                        test_id_dict.clear()
                        user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==2.6) #admin : edit test analyze_date
def edit_test_analyze_date_handler(message):
    cid = message.chat.id
    if cid in admins:
        analyze_date = message.text
        if analyze_date.isnumeric() == True and 1 <= int(analyze_date) <= 90:
            edit_test_analyze_date(analyze_date=analyze_date, id=test_id_dict['id'])
            bot.send_message(cid, text_admin['test_analyze_date_success'])
            test_id_dict.clear()
            user_steps[cid] = 0
        else:
            bot.send_message(cid, text_admin['test_analyze_date_check'])
    else:
        unknown_message(message)
    
            
@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==2.7) #admin : edit test description
def edit_test_description_handler(message):
    cid = message.chat.id
    if cid in admins:
        description = message.text
        if len(description) > 255:
            bot.send_message(cid, text_admin['test_description_check'])
        else:
            edit_test_description(description=description, id=test_id_dict['id'])
            bot.send_message(cid, text_admin['test_description_success'])
            test_id_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)
    
                
@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3) #admin : create breed name
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
            markup = InlineKeyboardMarkup() #to define specifications
            markup.add(InlineKeyboardButton(text['no'], callback_data='no_specifications_breed'), InlineKeyboardButton(text['yes'], callback_data='yes_specifications_breed'))
            bot.send_message(cid, text_admin['breed_specifications_yn'], reply_markup=markup)
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3.1) #admin : create breed specifications
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3.2) # admin : edit breed name
def edit_breed_name_handler(message):
    cid = message.chat.id
    if cid in admins:
        name = message.text
        if check_breed_name(name):
            bot.send_message(cid, text_admin['breed_name_unique'])
        elif len(name) > 45:
            bot.send_message(cid,text_admin['breed_name_check'])
        else:
            edit_breed_name(name=name, id=breed_id_dict['breed_id'])
            bot.send_message(cid, text_admin['edit_breed_name'])
            breed_id_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==3.3) # admin : edit breed specifications
def edit_breed_specifications_handler(message):
    cid = message.chat.id
    if cid in admins:
        specifications = message.text
        if len(specifications) > 255:
            bot.send_message(cid, text_admin['breed_specifications_check'])
        else:
            edit_breed_specifications(specifications=specifications, id=breed_id_dict['breed_id'])
            bot.send_message(cid, text_admin['edit_breed_specifications'])
            breed_id_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==4) #admin : edit answer date
def reception_answer_date_edit_handler(message):
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
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==5) #admin : edit result date
def result_date_edit_handler(message):
    cid = message.chat.id
    mid = message.message_id
    if cid in admins:
        result_date = message.text
        if is_valid_datetime(result_date) == False:
            bot.send_message(cid, text_admin['result_date_check'])
        else :
            result_date = is_valid_datetime(result_date)
            edit_result_date(result_date=result_date, id=result_id_dict['id'])
            bot.send_message(cid, text_admin['result_date_success'])
            result_id_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==5.1) #admin : edit result quantity
def result_quantity_edit_handler(message):
    cid = message.chat.id
    if cid in admins:
        result_quantity = message.text
        try:
            result_quantity = float(result_quantity)
        except:
            bot.send_message(cid, text_admin['result_quantity_check'])
        else:
            if len(str(result_quantity).split('.')[0]) > 5 or len(str(result_quantity).split('.')[-1]) > 3 :
                bot.send_message(cid, text_admin['result_quantity_check'])
            else:
                edit_result_quantity(result_quantity=result_quantity, id=result_id_dict['id'])
                bot.send_message(cid, text_admin['result_quantity_success'])
                minimum_range = show_test_type_range(test_id_dict['id'])['minimum_range']
                maximum_range = show_test_type_range(test_id_dict['id'])['maximum_range']
                if result_quantity > maximum_range:
                    analysis = 'high'
                elif result_quantity < minimum_range:
                    analysis = 'low'
                else:
                    analysis = 'normal'
                edit_result_analysis(analysis=analysis, id=result_id_dict['id'])
                bot.send_message(cid, text_admin['result_analysis_success'].format(analysis))
                result_id_dict.clear()
                test_id_dict.clear()
                user_steps[cid] = 0
    else:
        unknown_message(message)


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==5.2) #admin : edit conclusion
def result_conclusion_edit_handler(message):
    cid = message.chat.id
    if cid in admins:
        conclusion = message.text
        if len(conclusion) > 65535:
            bot.send_message(cid, text_admin['result_conclusion_check'])
        else:
            edit_result_conclusion(conclusion=conclusion, id=result_id_dict['id'])
            bot.send_message(cid, text_admin['result_conclusion_success'])
            result_id_dict.clear()
            user_steps[cid] = 0
    else:
        unknown_message(message)

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==6) #admin : search username for show user data and pet buttons
def search_username_handler(message):
    cid = message.chat.id
    if cid in admins:
        username = message.text
        user_id = get_cid(username)
        if user_id == False:
            bot.send_message(cid, text_admin['username_not'])
        else:
            for key, value in show_user_data(user_id).items():
                if value == None:
                    bot.send_message(cid, f"{text[key]} : ...")
                else:
                    bot.send_message(cid, f"{text[key]} : {value}")
            markup = InlineKeyboardMarkup()
            for item in show_user_all_pet_data(user_id):
                markup.add(InlineKeyboardButton(f"{item['name']}", callback_data=f"information_pet_{item['id']}"))
            bot.send_message(cid, text_admin['choose_pet'], reply_markup=markup)
            user_steps[cid] = 0


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.1) #user : edit first name
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.2) #user : edit last name
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.3) #user : edit username
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
  

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.4) #user : edit national code
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.5) #user : edit phone
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==10.6) #user : edit address
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11) #user : create pet
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
    

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11.1) #user : edit gender
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11.2) #user : edit weight
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


@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==11.3) #user : edit personality
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
        

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==12) #user : create reception with comment and reception_test
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


@bot.message_handler(content_types=['photo']) #user : receipt image 
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
