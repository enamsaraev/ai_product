import requests
import re
import os
import pandas as pd
from pathlib import Path
from decouple import config

from ai.service.data.characteristics import characteristics


class RequestData:
	def __init__(self, code, name, brand, model, article):
		self.url = config('REQUEST_URL')
		self.token = config('GPT_TOKEN')
		self.model_url = config('MODEL_URL')

		self.DOCUMENT_PATH = config('LINK_DOCUMENT_PATH')
		self.LINK_SHEET = 'Смартфоны'

		self.BRANDS = ['APPLE', 'SAMSUNG', 'REDMI', 'TECNO', 'INFINIX']

		self.code = code
		self.name = name
		self.brand = brand
		self.model = model
		self.article = article

	def get_data(self):
		df_link = self.get_link()
		if df_link.empty:
			gpt_link = self.get_link_from_gpt()

			try:
				text = gpt_link['result']['alternatives'][0]['message']['text']
			except Exception:
				return
			
			links = self.parse_link(text)
			if not links:
				return
			
			link = links[0]
		
		else:
			link = df_link['Ссылка на сайт поставщика/вендора'].values[0]

		return (
			link, 
			self.brand,
			self.model,
			self.article,
		)

	def get_link(self):
		df_links = pd.read_excel(
			os.path.join(Path(__file__).resolve().parent.parent.parent, f'{self.DOCUMENT_PATH}links.xlsx'), 
			sheet_name=self.LINK_SHEET
		)

		return df_links.loc[
			(df_links['Код Товара'] == int(self.code) if self.code.isdigit() else self.code) &
			(df_links['Ситилинк - Полное Наименование'] == self.name) &
			(df_links['Бренд'] == self.brand) &
			(df_links['Модель'] == self.model) &
			(df_links['PartNumber/Артикул Производителя'] == self.article)
		]

	def get_link_from_gpt(self):
		default_text_msg = "предоставь ссылку на сайт (на страницу с описанием товара)\
			 		для товара бренда '{brand}', модели '{model}', с артикулом '{article}'"
		response = self.make_request(
			default_text_msg.format(
				brand=self.brand,
				model=self.model,
				article=self.article
			)
		)
		return response

	def make_request(self, text_msg):
		data = {}
		data['modelUri'] = self.model_url
		data['completionOptions'] = {
			'stream': False,
			'temperature': 0.3,
			'maxTokens': 1000
		}
		data['messages'] = [
			{
				"role": "system",
				"text": text_msg
			}
		]

		try:
			response = requests.post(self.url, headers={'Authorization': f'Api-Key {self.token}'}, json=data).json()
		except Exception:
			return {}
		
		return response
	
	def parse_link(self, text):
		return re.findall(r'(https?://\S+)', text)


class GPTProductCharacteristics:
	def __init__(self, link, brand, model, article):
		self.url = config('REQUEST_URL')
		self.token = config('GPT_TOKEN')
		self.model_url = config('MODEL_URL')

		self.characteristics = characteristics

		self.link = link
		self.brand = brand
		self.model = model
		self.article = article

		self.result = {}

	def get_characteristics(self):
		if not self.link:
			return
		
		list_of_split_characteristics = self.split_chars()
		for part in list_of_split_characteristics:
			text_msg = self.get_text_msg(part)

			response = self.make_request(text_msg)
			if not response:
				continue

			try:
				text = response['result']['alternatives'][0]['message']['text'] + '\n'
			except:
				continue

			self.update_result(text, part)

	def make_request(self, text_msg):
		data = {}
		data['modelUri'] = self.model_url
		data['completionOptions'] = {
			'stream': False,
			'temperature': 0.3,
			'maxTokens': 1000
		}
		data['messages'] = [
			{
				"role": "system",
				"text": text_msg
			}
		]

		try:
			response = requests.post(self.url, headers={'Authorization': f'Api-Key {self.token}'}, json=data).json()
		except Exception:
			return {}
		
		return response

	def get_text_msg(self, chars):
		default_text_msg = "по ссылке {link}  \
							можно найти информацию о товаре бренда {brand}, модели {model}, с артикулом {article}. \
							Напиши, в каждой новой строке только значение для каждой характеристики ниже в формате 'ДА' или 'НЕТ' \
							{chars} "
		return default_text_msg.format(
			link=self.link, 
			brand=self.brand, 
			model=self.model, 
			article=self.article,
			chars=', '.join([f'{c}' for c in chars])
		)
	
	def split_chars(self):
		parts = [self.characteristics[i:i+10] for i in range(0, len(self.characteristics)-9, 10)]
		parts.append(self.characteristics[len(parts)*10::])
		return parts
	
	def update_result(self, text, part):
		new_characteristics = {}
		splitted_text = text.split('\n')
		for idx, c in enumerate(part, 0):
			if len(splitted_text) == len(part):
				new_characteristics[c] = splitted_text[idx]
			else:
				value = self.get_c_value(c, text)
				if value:
					new_characteristics[c] = value
		
		self.result.update(new_characteristics)

	def get_c_value(self, c, text):
		c = c.replace('(', '\(')
		c = c.replace(')', '\)')
		char_value = re.findall(rf"\b{c}.*\b", text)
		if not char_value:
			return ''

		return 'ДА' if 'ДА' in char_value[0] else 'НЕТ'