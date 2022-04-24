import pandas as pd
import sqlalchemy
import mysql.connector
from main import *

class Connector:
	def __init__(self, rules = None):
		self.rules = rules
	def execute(self, script: str, fetchall: bool = False):
		connection = mysql.connector.connect(**self.rules)
		cursor = connection.cursor()
		cursor.execute(script)
		if fetchall == True:
			return cursor.fetchall()
		cursor.close()
		connection.close()

rules = {
	'host': 'localhost',
	'user': 'root',
	'passwd': '',
	'database': 'elixirdatabase'
}

cursor = Connector(rules)

def id_name_db(id_ = False, name = False):
	if id_ != False:
		db = cursor.execute(f"select personagem.nome from personagem where p.idpersonagem = {id_}", True)
		return db[0][0]
	if name != False:
		db = cursor.execute(f"select p.idpersonagem from personagem as p where p.nome like '{name}'", True)
		return db[0][0]

def atributo_db(atb, token = False, id_ = False, get_mod = False, get_atb = False):
	if 'int' in atb.lower():
		atb = 'inte'
	elif 'hab' in atb.lower():
		atb = 'pod'
	colunaAtb = f'a.{atb.lower()}'
	colunaMod = f'a.mod{atb.lower()}'

	if token != False:
		id_ = id_name_db(name=token)

	print(colunaAtb)
	print(colunaMod)

	if get_atb != False:
		db = cursor.execute(f"""select {colunaAtb} 
						  from personagem as p join atributos as a
						  on p.atributostable = a.idatributos
						  where p.idpersonagem = {id_}""", True)
		print(db)
		print(db[0][0])
		return db[0][0]

	if get_mod != False:
		db = cursor.execute(f"""select {colunaMod} 
						  from personagem as p join atributos as a
						  on p.atributostable = a.idatributos
						  where p.idpersonagem = {id_}""", True)
		print(db)
		print(db[0][0])
		return db[0][0]

def qual_sinal_db(a):
	modi = round((int(a)-10)/2 + 0.5, 0)
	print(f'modi: {modi}')
	if modi >= 0.0:
		return '+'
	elif modi < 0.0:
		return  '-'

def personagens_db():
	db = cursor.execute('select personagem.nome from personagem', True)
	listaPersonagens = []
	for row in db:
		personagem = row[0].replace(',', '')
		listaPersonagens.append(personagem)
	print(listaPersonagens)
	return listaPersonagens

def val_personagem_existe(token):
	for per in personagens_db():
		if token.title().replace(' ', '') in per.title().replace(" ", ''):
			print('Analisado: ' + str(per).title())
			print('Igual: ' + str(token.title()))
			print('foi')
			return True

def inventario(token, acharItem = False, peso = False, idinventario = False):
	_id = id_name_db(name=token)

	returnPeso = ''
	returnIdinventario = ''
	returnAcharItem = ''

	if peso == True:
		returnPeso = ', i.peso'
	if idinventario == True:
		returnIdinventario = ', i.idinventario'
	if acharItem != False:
		returnAcharItem = f" and i.item like '%{acharItem}%'"

	db = cursor.execute(f"""select i.item{returnPeso}{returnIdinventario}
		from personagem as p join inventario as i
		on p.idpersonagem = i.idpersonagem
		where p.idpersonagem = {_id}{returnAcharItem}""", True)

	return db

def arma(token, acharArma = False, peso = False, dano = False, idarma = False):
	print(token)
	_id = id_name_db(name=token)
	returnPeso = ''
	returnDano = ''
	returnIdarma = ''
	returnAcharArma = ''

	if peso == True:
		returnPeso = ', a.peso'
	if idarma == True:
		returnIdarma = ', a.idarmas'
	if dano == True:
		returnDano = ', a.dano'
	if acharArma != False:
		returnAcharArma = f" and a.item like '%{acharArma}%'"

	db = cursor.execute(f"""SELECT a.item{returnPeso}{returnDano}{returnIdarma}
			FROM personagem AS p JOIN armas AS a
			ON p.idpersonagem = a.idpersonagem
			where p.idpersonagem = {_id}{returnAcharArma}""", True)

	return db

def get_link(token):
	_id = id_name_db(name=token)
	db = cursor.execute(f"""SELECT p.urlplanilha FROM personagem as p WHERE p.idpersonagem = {_id}""", True)
	if db[0][0] == None:
		return IndexError
	else:
		return db[0][0]

def return_fetchall(script: str):
	db = cursor.execute(script, True)
	return db

def script_sql(script):
	cursor.execute(script)
