import threading
from tkinter import *
from tkinter import ttk
from classes.conector import Conector
import pandas as pd

def main():
    conector = Conector()
    #conector.set_app_id("1184370")
    #conector.set_language("portuguese")
    #conector.set_filter("recent")
    #comentarios = conector.extrair_comentarios()
    conector.set_nome("baldu")
    conector.pesquisar_jogo()
    enche_linguica = 0
    while int(len(threading.enumerate())) > 1:
        enche_linguica = enche_linguica + 1
    print(conector.jogos["nome"])
main()