import telebot
from telebot import types
import parse
import cfg
import re


bot = telebot.TeleBot(cfg.token)

user_dict = {}


class User:
    def __init__(self, chat_id):
    	self.chat_id = chat_id
    	self.name = None
    	self.number = None
    	self.town = None
    	self.mail = None
    	self.product = None
    	self.costs = None
    	self.vacancy = None
    	self.msg = None



number_pattern = re.compile(r'\+\d+')
mail_pattern = re.compile(r'\S+\@\D+\.\D+')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	chat_id = message.chat.id
	user = User(chat_id)
	user_dict[chat_id] = user
	bot.send_message(chat_id, 'Главное меню', parse_mode = 'HTML',  reply_markup=cfg.main_kb)



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def main_func(message):

	if message.text == cfg.back_button.text:	#главное меню
		send_welcome(message)

	if message.text == cfg.itembtn1.text:		#продукция
		prod(message)

	if message.text == cfg.itembtn2.text:		#аксессуары
		buff(message)

	if message.text == cfg.itembtn3.text:		#связаться с нами
		contact(message)

	if message.text == cfg.itembtn4.text:		#сделать заказ
		order(message)

	if message.text == cfg.itembtn5.text:		#сотрудничество
		coop(message)




#--------------------next_step_handler for prod--------------------------------

def prod(message):
	markup = cfg.guns_kb
	msg = bot.send_message(message.chat.id, 'Выберите интересующий вас товар', reply_markup = markup)
	bot.register_next_step_handler(msg, prod_menu_step)
	



def prod_menu_step(message):
	if message.text == cfg.back_button.text:
		send_welcome(message)
	else:
		try:
			url = 'products'
			chat_id = message.chat.id
			find = 0



			if message.text in parse.get_products('n', url):
				find = 1
				costs = parse.get_products('np', url).get(message.text)
				url = ['products']
			if find != 1:
				raise Exception


			msg = bot.send_message(chat_id, 'Подождите...', reply_markup = types.ReplyKeyboardRemove())
			
			product = message.text
			user = user_dict[chat_id]
			user.product = product
			user.costs = costs
			user.msg = message

			photo = parse.get_imgs(url).get(product)
			href = parse.get_hrefs(url).get(product)
			text = f'<b>{message.text}</b>\n\n' + parse.text_for_prod(message.text)
			bot.delete_message(msg.chat.id, msg.message_id)
			markup = cfg.inline_prod_kb
			if message.text == 'Электронный измерительный комплекс':
				markup = types.InlineKeyboardMarkup(row_width = 1)
				markup.add(cfg.btn3)
				markup.row_width = 2
				markup.add(cfg.b2, cfg.btn4)

			if message.text == 'Dedal Stalker 6x32':
				markup = types.InlineKeyboardMarkup(row_width = 1)
				markup.add(cfg.btn2, cfg.btn3)
				markup.row_width = 2
				markup.add(cfg.b2, cfg.btn4)

			bot.send_photo(chat_id, photo, text + f'\nЦена: {costs}',parse_mode = 'HTML', reply_markup = markup)

		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, buff_choice_step)



#--------------------next_step_handler for prod--------------------------------


#--------------------next_step_handler for buff--------------------------------

def buff(message):
	markup = cfg.buff_kb
	msg = bot.send_message(message.chat.id, 'Выберите интересующий вас аксессуар', reply_markup = markup)
	bot.register_next_step_handler(msg, buff_choice_step)





def buff_choice_step(message):
	if message.text == cfg.back_button.text:
		send_welcome(message)
	else:
		try:
			url = ['related', 'related/?PAGEN_1=2']
			chat_id = message.chat.id
			find = 0



			for u in url:
				if message.text in parse.get_products('n', u):
					find = 1
					costs = parse.get_products('np', u).get(message.text)
					break

			if find != 1:
				raise Exception
	

			msg = bot.send_message(chat_id, 'Подождите...', reply_markup = types.ReplyKeyboardRemove())
			
			product = message.text
			user = user_dict[chat_id]
			user.product = product
			user.costs = costs
			photo = parse.get_imgs(url).get(product)
			href = parse.get_hrefs(url).get(product)
			text = parse.text_for_buff(href)

			bot.delete_message(msg.chat.id, msg.message_id)
			bot.send_photo(chat_id, photo, text + f'Цена: {costs}', reply_markup = cfg.inline_buff_kb)

		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, buff_choice_step)
		

#--------------------next_step_handler for buff--------------------------------




#------------------------------------------------------------------------------
def contact(message):
	text = '''
				Наш официальный сайт: edgun.ru\n
				Форум нашего сообщества, в котором вы сможете обсудить актуальные новости компании: http://edgun.ru/forum\n
				Официальное представительство в городах России: http://www.edgun.ru/contacts
				'''
	text = text.replace('\t','')
	bot.send_message(message.chat.id, text, reply_markup=cfg.back_kb)


#------------------------------------------------------------------------------


#--------------------next_step_handler for orders--------------------------------


def order(message):
	msg = bot.send_message(message.chat.id, 'Введите ваше имя', reply_markup = cfg.back_kb)
	bot.register_next_step_handler(msg, order_name_step)


def order_name_step(message):
	if message.text == cfg.back_button.text:
		send_welcome(message)
	else:
		try:
			chat_id = message.chat.id
			user = user_dict[chat_id]
			user.name = message.text
			msg = bot.send_message(chat_id, 'Введите ваш номер телефона\nВНИМАНИЕ! Номер должен быть вида +71234567890 и состоять из 11 цифр')
			bot.register_next_step_handler(msg, order_number_step)
		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, order_name_step)


def order_number_step(message):
	if message.text == cfg.back_button.text:
		order_name_step(message)
	else:
		try:
			chat_id = message.chat.id
			number = message.text

			numfind = number_pattern.search(number).group()
			done = numfind and len(numfind) == 12

			if not done:
				msg = bot.reply_to(message, 'Недопустимое значение')
				bot.register_next_step_handler(msg, order_number_step)
				return

			user = user_dict[chat_id]
			user.number = f'{number[:2]} ({number[2:5]}) {number[5:8]}-{number[8:10]}-{number[10:12]}'
			msg = bot.send_message(chat_id, 'Введите ваш город')
			bot.register_next_step_handler(msg, order_town_step)
		except Exception as e:
			msg = bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, order_number_step)


def order_town_step(message):
	if message.text == cfg.back_button.text:
		order_number_step(message)
	else:
		try:
			chat_id = message.chat.id
			town = message.text
			user = user_dict[chat_id]
			user.town = town
			msg = bot.send_message(chat_id, 'Введите ваш email. aaa@aaa.aa')
			bot.register_next_step_handler(msg, order_mail_step)
		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, order_town_step)



def order_mail_step(message):
	if message.text == cfg.back_button.text:
		order_town_step(message)
	else:
		try:
			chat_id = message.chat.id
			mail = message.text

			if not mail_pattern.search(mail):
				msg = bot.reply_to(message, 'Недопустимое значение. Проверьте корректность введенных данных')
				bot.register_next_step_handler(msg, order_mail_step)
				return

			user = user_dict[chat_id]
			user.mail = mail

			if user.product and user.costs:
				order_final(message)

			else:
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
				but1 = types.KeyboardButton('Продукция')
				but2 = types.KeyboardButton('Аксессуары')
				markup.add(but1, but2, cfg.back_button)

				msg = bot.send_message(chat_id, 'Что вы хотите приобрести?', reply_markup = markup)
				bot.register_next_step_handler(msg, order_product_step)
		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, order_mail_step)



def order_product_step(message):
	if message.text == cfg.back_button.text:
		order_mail_step(message)
	else:
		try:
			chat_id = message.chat.id

			if message.text == 'Продукция':
				markup = cfg.guns_kb
				url = ['products',]
			elif message.text == 'Аксессуары':
				markup = cfg.buff_kb
				url = ['related', 'related/?PAGEN_1=2']
			else:
				raise Exception

			msg = bot.send_message(chat_id, 'Выберите товар', reply_markup = markup)
			bot.register_next_step_handler(msg, order_choice_step, url)
		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, order_product_step)


def order_choice_step(message, url):
	if message.text == cfg.back_button.text:
		order_product_step(message)
	else:
		try:
			chat_id = message.chat.id
			find = 0

			for u in url:
				if message.text in parse.get_products('n', u):
					find = 1
					costs = parse.get_products('np', u).get(message.text)
					break

			if find != 1:
				bot.reply_to(message, 'Недопустимое значение')
				bot.register_next_step_handler(message, order_choice_step, url)

			product = message.text
			user = user_dict[chat_id]
			user.product = product
			user.costs = costs


			msg = bot.send_message(chat_id, 'Подождите...', reply_markup = types.ReplyKeyboardRemove())
			bot.delete_message(msg.chat.id, msg.message_id)
			order_final(message)

		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, order_choice_step, url)



def order_final(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	text= f'''
			<b>Имя: </b>{user.name}
			<b>Телефон: </b>{user.number}
			<b>Город: </b>{user.town}
			<b>Email: </b>{user.mail}
			<b>Товар: </b>{user.product}
			<b>Цена: </b>{user.costs}

			<b>Отправить заявку?</b>
        	'''

	text = text.replace('\t', '').strip()
	bot.send_message(chat_id, text, parse_mode = 'HTML', reply_markup = cfg.yes_no_inline)


#--------------------next_step_handler for orders--------------------------------

#--------------------next_step_handler for coop--------------------------------

def coop(message):
	msg = bot.send_message(message.chat.id, 'Введите ваше имя', reply_markup = cfg.back_kb)
	bot.register_next_step_handler(msg, coop_name_step)


def coop_name_step(message):
	if message.text == cfg.back_button.text:
		send_welcome(message)
	else:
		try:
			chat_id = message.chat.id
			user = user_dict[chat_id]
			user.name = message.text
			msg = bot.send_message(chat_id, 'Введите ваш номер телефона\nВНИМАНИЕ! Номер должен быть вида +71234567890 и состоять из 11 цифр')
			bot.register_next_step_handler(msg, coop_number_step)
		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, coop_name_step)


def coop_number_step(message):
	if message.text == cfg.back_button.text:
		coop_name_step(message)
	else:
		try:   
			chat_id = message.chat.id
			number = message.text

			numfind = number_pattern.search(number).group()
			done = numfind and len(numfind) == 12

			if not done:
				msg = bot.reply_to(message, 'Недопустимое значение')
				bot.register_next_step_handler(msg, coop_number_step)
				return

			user = user_dict[chat_id]
			user.number = f'{number[:2]} ({number[2:5]}) {number[5:8]}-{number[8:10]}-{number[10:12]}'
			msg = bot.send_message(chat_id, 'Введите ваш город')
			bot.register_next_step_handler(msg, coop_town_step)
		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, coop_number_step)


def coop_town_step(message):
	if message.text == cfg.back_button.text:
		coop_number_step(message)
	else:
		try:
			chat_id = message.chat.id
			town = message.text
			user = user_dict[chat_id]
			user.town = town
			msg = bot.send_message(chat_id, 'Введите ваш email. aaa@aaa.aa')
			bot.register_next_step_handler(msg, coop_mail_step)
		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, coop_town_step)


def coop_mail_step(message):
	if message.text == cfg.back_button.text:
		coop_town_step(message)
	else:
		try:
			chat_id = message.chat.id
			mail = message.text

			if not mail_pattern.search(mail):
				msg = bot.reply_to(message, 'Недопустимое значение. Проверьте корректность введенных данных')
				bot.register_next_step_handler(msg, coop_mail_step)
				return

			user = user_dict[chat_id]
			user.mail = mail
			user.msg = message
			msg = bot.send_message(chat_id, 'Выберите должность', reply_markup = cfg.coop_kb)
			bot.register_next_step_handler(msg, coop_choice_step)

		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, coop_mail_step)


def coop_choice_step(message):
	if message.text == cfg.back_button.text:
		coop_mail_step(message)
	else:
		try:
			chat_id = message.chat.id
			find = 0
			for v in cfg.vacancy_list:
				if message.text == v.name:
					find = 1
					vacancy = v
					break

			if find != 1:
				raise Exception

			msg = bot.send_message(chat_id, 'Подождите...', reply_markup = types.ReplyKeyboardRemove())
			
			text = f'''
					<b>Должность: </b>{vacancy.name} 
					<b>Описание: </b>{vacancy.descr}
					<b>Навыки: </b>{vacancy.skill}
					<b>Зарплата: </b>{vacancy.wage}

					Выбрать эту должность?
					'''

			text = text.replace('\t', '').strip()		

			user = user_dict[chat_id]
			user.vacancy = vacancy.name


			bot.delete_message(msg.chat.id, msg.message_id)
			bot.send_message(chat_id, text, parse_mode = 'HTML', reply_markup = cfg.inline_coop_kb)

		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, coop_choice_step)


def coop_about_step(message):
	if message.text == cfg.back_button.text:
		coop_choice_step(message)
	else:
		try:
			chat_id = message.chat.id
			msg = bot.send_message(chat_id, 'Расскажите о себе')
			bot.register_next_step_handler(msg, coop_final)

		except Exception as e:
			bot.reply_to(message, 'Недопустимое значение')
			bot.register_next_step_handler(message, coop_about_step)


def coop_final(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	text= f'''
			<b>Имя: </b>{user.name}
			<b>Телефон: </b>{user.number}
			<b>Город: </b>{user.town}
			<b>Email: </b>{user.mail}
			<b>Должность: </b>{user.vacancy}
			<b>О себе: </b>{message.text}

			<b>Отправить заявку?</b>
        	'''

	text = text.replace('\t', '').strip()
	bot.send_message(chat_id, text, parse_mode = 'HTML', reply_markup = cfg.coop_yes_no_inline)

#--------------------next_step_handler for coop--------------------------------


@bot.callback_query_handler(func=lambda call: True)
def callback_order(call):

	if call.data == "yes":
		m = call.message.text.split('\n')
		newtext = '\n'.join(m[:-1])
		text = f'<b>ЗАКАЗ!</b> \nНикнейм: @{call.message.chat.username}\n' + newtext
		bot.send_message(-432590869, text = text, parse_mode = 'HTML')
		bot.edit_message_text('Заявка отправлена!', call.message.chat.id, call.message.message_id)
		send_welcome(call.message)

	if call.data == "no":
		bot.edit_message_text('Заявка удалена!', call.message.chat.id, call.message.message_id)
		chat_id = call.message.chat.id
		user = user_dict[chat_id]
		user.product = None
		user.costs = None
		send_welcome(call.message)

	if call.data == 'back':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		chat_id = call.message.chat.id
		user = user_dict[chat_id]
		user.product = None
		user.costs = None
		buff(call.message)

	if call.data == 'order':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		order(call.message)

	if call.data == 'back_prod':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		chat_id = call.message.chat.id
		user = user_dict[chat_id]
		user.product = None
		user.costs = None
		prod(call.message)


	if call.data == 'more_photos':
		name = call.message.caption.split('\n')[0].strip()
		photos = parse.more_photos(name)

		for photo in photos:
			cfg.media.append(types.InputMediaPhoto(photo))
		
		bot.edit_message_media(media = cfg.media[cfg.count], chat_id = call.message.chat.id, message_id = call.message.message_id, reply_markup = cfg.choice_photo_kb)

	if call.data == 'right':
		cfg.count += 1
		num = cfg.count % len(cfg.media)
		bot.edit_message_media(media = cfg.media[num], chat_id = call.message.chat.id, message_id = call.message.message_id, reply_markup = cfg.choice_photo_kb)

	if call.data == 'left':
		cfg.count -= 1
		num = cfg.count % len(cfg.media)
		bot.edit_message_media(media = cfg.media[num], chat_id = call.message.chat.id, message_id = call.message.message_id, reply_markup = cfg.choice_photo_kb)


	if call.data == 'config':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		markup = types.InlineKeyboardMarkup()
		markup.add(cfg.back_menu_btn)
		bot.send_message(call.message.chat.id, parse.get_characteristic(call.message.caption.split('\n')[0].strip()),
    						 parse_mode = 'HTML', reply_markup = markup)

	if call.data == 'more_info':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		markup = types.InlineKeyboardMarkup()
		markup.add(cfg.back_menu_btn)
		bot.send_message(call.message.chat.id, parse.more_text(call.message.caption.split('\n')[0].strip()),
    						 parse_mode = 'HTML', reply_markup = markup)


	if call.data == 'back_menu_prod':
		chat_id = call.message.chat.id
		user = user_dict[chat_id]
		name = user.msg
		cfg.media.clear()
		cfg.count = 0
		bot.delete_message(call.message.chat.id, call.message.message_id)
		prod_menu_step(name)

	if call.data == 'c_yes':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		coop_about_step(call.message)

	if call.data == 'c_no':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		chat_id = call.message.chat.id
		user = user_dict[chat_id]
		name = user.msg
		user.vacancy = None
		coop_mail_step(name)

	if call.data == 'coop_yes':
		m = call.message.text.split('\n')
		newtext = '\n'.join(m[:-1])
		text = f'<b>РЕЗЮМЕ!</b> \nНикнейм: @{call.message.chat.username}\n' + newtext
		bot.send_message(-432590869, text = text, parse_mode = 'HTML')
		bot.edit_message_text('Заявка отправлена!', call.message.chat.id, call.message.message_id)
		send_welcome(call.message)



bot.infinity_polling()

