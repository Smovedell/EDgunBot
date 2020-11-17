from telebot import types
import parse



token = 'Your token'

msgs = [] # тут храним сообщения которые получаем при продукции
media = [] # тут все фотки, между которыми переключаемся 
count = 0 # позиция фотки (изначально 0)


#-----------------------------------------------------------------------------
main_kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard = True)
itembtn1 = types.KeyboardButton('Продукция')
itembtn2 = types.KeyboardButton('Аксессуары')
itembtn3 = types.KeyboardButton('Связаться с нами')
itembtn4 = types.KeyboardButton('Сделать заказ')
itembtn5 = types.KeyboardButton('Сотрудничество')
main_kb.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
#-----------------------------------------------------------------------------




#-----------------------------------------------------------------------------
back_kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
back_button = types.KeyboardButton('В главное меню')
back_kb.add(back_button)
#-----------------------------------------------------------------------------




#-----------------------------------------------------------------------------
guns_kb = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
guns_kb.add(back_button)
for gun in parse.get_products('n', 'products'):
	button = types.KeyboardButton(gun)
	guns_kb.add(button)
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
buff_kb = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
buff_kb.add(back_button)
for prop in parse.get_products('n', 'related'):
	button = types.KeyboardButton(prop)
	buff_kb.add(button)

for prop in parse.get_products('n', 'related/?PAGEN_1=2'):
	button = types.KeyboardButton(prop)
	buff_kb.add(button)
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
yes_no_inline = types.InlineKeyboardMarkup(row_width = 2)
yesb = types.InlineKeyboardButton('Да', callback_data = 'yes')
nob = types.InlineKeyboardButton('Нет', callback_data = 'no')
yes_no_inline.add(yesb, nob)
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
inline_buff_kb = types.InlineKeyboardMarkup(row_width = 2)
b1 = types.InlineKeyboardButton('Назад', callback_data = 'back')
b2 = types.InlineKeyboardButton('Заказать', callback_data = 'order')
inline_buff_kb.add(b1, b2)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
inline_prod_kb = types.InlineKeyboardMarkup(row_width = 2)
btn1 = types.InlineKeyboardButton('Еще фото', callback_data = 'more_photos')
btn2 = types.InlineKeyboardButton('Характеристики', callback_data = 'config')
btn3 = types.InlineKeyboardButton('Подробное описание', callback_data = 'more_info')
btn4 = types.InlineKeyboardButton('Назад', callback_data = 'back_prod')
inline_prod_kb.add(btn1, btn2)
inline_prod_kb.row_width = 1
inline_prod_kb.add(btn3)
inline_prod_kb.row_width = 2
inline_prod_kb.add(b2, btn4)

back_menu_btn = types.InlineKeyboardButton('Назад', callback_data = 'back_menu_prod')
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
vacancy_list = []

class Vacancy:
	def __init__(self, name):
		self.name = name
		self.wage = None
		self.skill = None
		self.descr = None


v1 = Vacancy('Упаковщик')
v2 = Vacancy('Сборщик')
v3 = Vacancy('Проектировщик')

v1.descr = 'Описание упаковщика'
v2.descr = 'Описание сборщика'
v3.descr = 'Описание проеткировщика'

v1.wage = 30000
v2.wage = 35000
v3.wage = 45000

v1.skill = 'Необходимые навыки упаковщика'
v2.skill = 'Необходимые навыки сборщика'
v3.skill = 'Необходимые навыки проеткировщика'

vacancy_list.append(v1)
vacancy_list.append(v2)
vacancy_list.append(v3)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
coop_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
coop_kb.add(back_button)
for v in vacancy_list:
	coopbtn = types.KeyboardButton(v.name)
	coop_kb.add(coopbtn)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
inline_coop_kb = types.InlineKeyboardMarkup(row_width = 2)
coopyesb = types.InlineKeyboardButton('Да', callback_data = 'c_yes')
coopnob = types.InlineKeyboardButton('Нет', callback_data = 'c_no')
inline_coop_kb.add(coopyesb, coopnob)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
coop_yes_no_inline = types.InlineKeyboardMarkup(row_width = 2)
cyesb = types.InlineKeyboardButton('Да', callback_data = 'coop_yes')
coop_yes_no_inline.add(cyesb, nob)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
choice_photo_kb = types.InlineKeyboardMarkup(row_width = 2)
left_button = types.InlineKeyboardButton('<', callback_data = 'left')
right_button = types.InlineKeyboardButton('>', callback_data = 'right')
choice_photo_kb.add(left_button, right_button, back_menu_btn)
#-----------------------------------------------------------------------------

