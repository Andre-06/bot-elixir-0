import gspread
import pandas as pd
import data_base
from time import sleep
from datetime import datetime
from google.oauth2 import service_account

import functions

scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

json_file = "credentials.json"

url_maugrin = "https://docs.google.com/spreadsheets/d/194P12H9b6_Pi06k3z9iYCyjZRJHX4dU2LG4PJHDed4k/edit#gid=0"

def login():
    try:
        credentials = service_account.Credentials.from_service_account_file(json_file)
        scoped_credentials = credentials.with_scopes(scopes)
        gc = gspread.authorize(scoped_credentials)
    except gspread.exceptions.APIError:
        print('\n\n\n================================')
        print('===========   AGUARDANDO  ============')
        print('================================')
        sec = int(datetime.now().strftime('%S'))
        sleep(60 - sec)
        credentials = service_account.Credentials.from_service_account_file(json_file)
        scoped_credentials = credentials.with_scopes(scopes)
        gc = gspread.authorize(scoped_credentials)

    return gc
def reader_all(url, pg="STATS"):
    gc = login()
    planilha = gc.open_by_url(url)
    aba = planilha.worksheet(pg)
    dados = aba.get_all_values()
    return dados

def finder(url, find='', in_row=None, in_col=None, pg="STATS"):
    gc = login()
    planilha = gc.open_by_url(url)
    aba = planilha.worksheet(pg)
    try:
        dado = aba.find(find, in_row=in_row, in_column=in_col)
    except gspread.exceptions.APIError:
        print('\n\n\n================================')
        print('===========   AGUARDANDO  ============')
        print('================================')
        sec = int(datetime.now().strftime('%S'))
        sleep(60 - sec)

        dado = aba.find(find, in_row=in_row, in_column=in_col)
    return dado

def reader(url, cell='', row='', col='', pg="STATS"):
    gc = login()
    planilha = gc.open_by_url(url)
    aba = planilha.worksheet(pg)

    if cell != '':
        dado = aba.cell(**cell).value

    if row != '':
        dado = aba.row_values(row)

    if col != '':
        dado = aba.col_values(col)

    return dado

def writer(url, list=[], pg="STATS"):
    gc = login()
    planilha = gc.open_by_url(url)
    planilha = planilha.worksheet(pg)
    planilha.append_row(list, value_input_option='USER_ENTERED')

def atributo_gs(atb, token, get_mod = False, get_atb = False):
    url = data_base.get_link(token)

    if get_atb != False and get_mod != False:

        db = finder(url, find=atb)
        print(db)

        new_cell = {'row': int(db.row) - 3,
                    'col': db.col}
        val = reader(url, new_cell)
        print(f"val: {val}")
        val1 = int(val)

        new_cell = {'row': int(db.row) - 4,
                    'col': db.col}
        val = reader(url, new_cell)
        print(f"val: {val}")
        val2 = val

        valF = (val1, val2)

        return valF

    if get_atb != False:
        db = finder(url, find=atb)
        print(db)
        print(db.col)
        print(db.row)
        new_cell = {'row': int(db.row) - 3,
                    'col': db.col}
        val = reader(url, new_cell)
        print(f"val: {val}")
        return int(val)

    if get_mod != False:
        db = finder(url, find=atb)
        print(db)
        print(db.col)
        print(db.row)
        new_cell = {'row': int(db.row) - 4,
                    'col': db.col}
        val = reader(url, new_cell)
        print(f"val: {val}")
        return val

def pericia_gs(pericia, token, get_per = False, get_mod = False):
    url = data_base.get_link(token)

    pericias_esquerda = ['Lábia', 'Domesticar', 'Convencer', 'Percepção', 'Artes', 'Natureza']

    if pericia.lower().startswith('craf'): pericia = 'Crafting'
    elif pericia.lower().startswith('uso'): pericia = 'Uso de Armas'
    elif pericia.lower().startswith('lab'): pericia = 'Lábia'
    elif pericia.lower().startswith('percep'): pericia = 'Percepção'
    elif pericia.lower().startswith('maos'): pericia = 'Mãos Leves'
    else: pericia = pericia.title()

    if get_per != False and get_mod != False:
        if pericia.title() in pericias_esquerda:
            col = 11
            sum_per = -1
            sum_mod = -2
        else:
            col = 4
            sum_per = 2
            sum_mod = 3

        db = finder(url, find=pericia, in_col=col)
        print(db)
        new_cell = {'row': db.row,
                    'col': int(db.col) + sum_per}

        val = reader(url, new_cell)
        print(f"val: {val}")
        val1 = int(val)

        new_cell = {'row': db.row,
                    'col': int(db.col) + sum_mod}

        val = reader(url, new_cell)
        print(f"val: {val}")
        val2 = val

        valF = (val1, val2)
        return valF

    if get_per != False:
        if pericia.title() in pericias_esquerda:
            col = 11
            sum_per = -1
        else:
            col = 4
            sum_per = 2

        db = finder(url, find=pericia, in_col=col)
        print(db)

        new_cell = {'row': db.row,
                    'col': int(db.col) + sum_per}

        val = reader(url, new_cell)
        print(f"val: {val}")
        return int(val)

    if get_mod != False:
        if pericia.title() in pericias_esquerda:
            col = 11
            sum_mod = -2
        else:
            col = 4
            sum_mod = 3

        db = finder(url, find=pericia, in_col=col)
        print(db)

        new_cell = {'row': db.row,
                    'col': int(db.col) + sum_mod}

        val = reader(url, new_cell)
        print(f"val: {val}")
        return val

def arma(token, acharArma, weight = False, damage = False):
    url = data_base.get_link(token)

    return_ = []

    invent = reader(url, col=17)[8:28]
    row = functions.index_(acharArma, invent)[1] + 9
    col = 17

    if weight == True:
        cell_weight = {'row' : row,
                    'col' : int(col) + 2}
        peso = reader(url, cell_weight)
        return_.append(peso)

    if damage == True:
        cell_damage = {'row': row,
                       'col': int(col) + 1}
        dano = reader(url, cell_damage)
        return_.append(dano)
    print(return_)
    return return_