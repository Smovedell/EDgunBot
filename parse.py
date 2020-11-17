import requests
from bs4 import BeautifulSoup as BS

source = 'http://www.edgun.ru/'

def get_html(url): #возвращает хтмл страницу
	r = requests.get(url)
	html = BS(r.content, 'lxml')
	return html

def get_products(mode, q): #возвращает список названия/цены
	rez = {}

	html = get_html(source + q)


	guns = html.find('div', class_ = 'items clearfix').find_all('div', class_ = 'item')
	for gun in guns:
		name = gun.find('div', class_ = 'description').find('span', class_ = 'name').text
		price = gun.find('div', class_ = 'description').find('span', class_ = 'price').text
		price = price.replace('\n', '').replace('от', '').replace('  ', ' ') + '₽'
		rez[name] = price

	if mode == 'n':
		return list(rez.keys())

	if mode == 'p':
		return list(rez.values())

	if mode == 'np':
		return rez



def get_hrefs(questions):
	rez = {}

	for q in questions:
		html = get_html(source + q)


		guns = html.find('div', class_ = 'items clearfix').find_all('div', class_ = 'item')
		for gun in guns:
			name = gun.find('div', class_ = 'description').find('span', class_ = 'name').text
			href = 'http://www.edgun.ru' + gun.find('a').get('href')
			rez[name] = href

	return rez



def get_imgs(questions):
	rez = {}

	for q in questions:
		html = get_html(source + q)


		guns = html.find('div', class_ = 'items clearfix').find_all('div', class_ = 'item')
		for gun in guns:
			name = gun.find('div', class_ = 'description').find('span', class_ = 'name').text
			href = 'http://www.edgun.ru' + gun.find('img').get('src')
			rez[name] = href

	return rez


def text_for_buff(href):
	html = get_html(href)
	text = html.find('div', class_ = 'left').text
	strings = text.replace('\t', '').replace('\n', '').split('\r') 
	text = ''
	for s in strings:
		if s:
			s = s.strip()
			text += f'{s}\n\n'
	return text



def get_characteristic(name):
	href = get_hrefs(['products']).get(name)
	rez = ''
	html = get_html(href)
	char = html.find('ul', class_ = 'characteristic').find_all('li', class_ = 'clearfix')
	for c in char:
			first = c.find('div', class_ = 'first').find('span').text
			second = c.find('div', class_ = 'second').find('span').text
			rez += f'<b>{first}: </b>\t{second}\n'

	return rez


def more_photos(name):
	href = get_hrefs(['products']).get(name)
	rez = []
	html = get_html(href)
	photos = html.find('div', class_ = 'gallery').find('ul').find_all('li')
	for p in photos:
		photo = 'http://www.edgun.ru' + p.find('img').get('src')
		rez.append(photo)

	if name == 'Пневматическая винтовка "Матадор"':
		rez.pop(2)

	return rez

def text_for_prod(name):
	href = get_hrefs(['products']).get(name)
	html = get_html(href)
	m = html.find('div', class_ = 'left')
	text = ''
	if name == 'Dedal Stalker 6x32':
		text = m.find('span').text

	elif name == 'Электронный измерительный комплекс':
		strings = m.text.replace('\r', '').replace('\xa0', '').replace('\t', '').split('\n')
		for s in strings:
			s = s.strip()
			if s:
				text += f'{s}\n'
		text = '\n'.join(text.split('\n')[:-4])

	else:
		pars = m.find_all('p')
		for p in pars:
			text += f'{p.text.strip()}\n'

	return text


def more_text(name):
	href = get_hrefs(['products']).get(name)
	html = get_html(href)
	m = html.find('div', class_ = 'info_page')
	text = ''
	if name == 'Dedal Stalker 6x32':
		strings = m.text.replace('\r', '').replace('\xa0', '').replace('\t', '').split('\n')
		newstrings = []
		for s in strings:
			s = s.strip()
			if s:
				newstrings.append(s)

		newstrings[1] += ' ' + m.find('iframe').get('src')
		vids = [' ' + vid.get('src') for vid in m.find_all('iframe')][1:]

		newstrings[-7] += '\n\n <b>Некоторые видео</b> \n'
		newstrings[-6] = f'<b>{newstrings[-6]}</b>\n' + vids[0] + '\n'
		newstrings[-5] = f'<b>{newstrings[-5]}</b>'
		newstrings[-4] += '\n' + vids[1] + '\n'
		newstrings[-3] = f'<b>{newstrings[-3]}</b>\n' + vids[2] + '\n'
		newstrings[-2] = f'<b>{newstrings[-2]}</b>'
		newstrings[-1] += '\n' + vids[3]

		text = '\n'.join(newstrings)


	elif name == 'Электронный измерительный комплекс':
		m = html.find('div', class_ = 'left')
		strings = m.text.replace('\r', '').replace('\xa0', '').replace('\t', '').split('\n')
		newstrings = []
		for s in strings:
			s = s.strip()
			if s:
				newstrings.append(s)
		vids = [' ' + vid.get('src') for vid in m.find_all('iframe')]

		newstrings[-4] += '\n\n<b>Некоторые видео</b>\n'

		for i in range(1, 4):
			newstrings[-i] = f'<b>{newstrings[-i]}</b>\n' + vids[3 - i] + '\n'

		text = '\n'.join(newstrings)
		

	else:
		pars = m.find_all('p')
		for p in pars:
			text += f'{p.text.strip()}\n'

		vids = [' ' + vid.get('src') for vid in m.find_all('iframe')]
		heads = [' ' + h.text for h in m.find_all('h4')]
		text += '\n<b>Некоторые видео</b>\n\n'

		for i in range(len(vids)):
			text += f'<b>{heads[i]} </b> \n{vids[i]}\n'


	return text
