from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from classes.conector import Conector
from functools import partial
import threading
import pandas as pd

conector = Conector()

class FilterDropDown(DropDown):
    pass

class LanguageDropDown(DropDown):
    pass

class TypeDropDown(DropDown):
    pass

class TypeButton(Button):
    pass

class FilterButton(Button):
    pass
class LanguageButton(Button):
    pass

class Tela(BoxLayout):
    def __init__(self,**kwargs):
        super(Tela, self).__init__(**kwargs)
        self.orientation = "horizontal"

        #dropdown do filtro
        botao_filter = FilterButton(text="sort by")
        filter_dropdown = FilterDropDown()
        botao_filter.bind(on_press=filter_dropdown.open)
        self.ids.selecionador.add_widget(botao_filter)
        filter_dropdown.bind(on_select=lambda instance, x: setattr(botao_filter, 'text', x))

        #dropdown da linguagem
        botao_language = LanguageButton(text="language")
        language_dropdown = LanguageDropDown()
        botao_language.bind(on_press=language_dropdown.open)
        self.ids.selecionador.add_widget(botao_language)
        language_dropdown.bind(on_select=lambda instance, x: setattr(botao_language, 'text', x))

        #dropdown do tipo
        botao_type = TypeButton(text="type")
        type_dropdown = TypeDropDown()
        botao_type.bind(on_press=type_dropdown.open)
        self.ids.selecionador.add_widget(botao_type)
        type_dropdown.bind(on_select=lambda instance, x: setattr(botao_type, 'text', x))

        #botão de finalizar
        botao_finalizar = Button(text="gerar arquivo xlsx", size_hint=(0.7, 0.5), on_release=self.gerar)
        self.ids.finalizador.add_widget(botao_finalizar)

    def gerar(self,nome):
        print(self.children[0].children[1].children[1].text)
        conector.set_app_id(str(self.ids.codigo_jogo.text))
        conector.set_language(str(self.children[0].children[1].children[1].text))
        conector.set_filter(str(self.children[0].children[1].children[2].text))
        conector.set_comment_type(str(self.children[0].children[1].children[0].text))
        print("codigo="+str(conector.get_app_id())+" , language="+conector.get_language()+" , filter="+conector.get_filter()+" , type="+conector.get_comment_type())
        comentarios = conector.extrair_comentarios()
        print(comentarios)
        comentarios_df = pd.DataFrame(comentarios)
        with pd.ExcelWriter(str(self.ids.codigo_jogo.text)+ ".xlsx") as writer:
            comentarios_df.to_excel(writer)


    def pesquisa(self):
        conector.set_nome(self.ids.nome.text)
        conector.pesquisar_jogo()
        while len(threading.enumerate()) > 1:
            print(100 * conector.quantidade_total_jogos_analisados / conector.quantidade_total_jogos)
        for i in range(len(conector.jogos["nome"])):
            print(conector.jogos["codigo"][i])
            self.ids.resultado.add_widget(Button(text=conector.jogos["nome"][i], on_press=self.setar_codigo))



    def setar_codigo(self, *args):
        nome = ""
        pos = 0
        for arg in args:
            nome = arg.text
        for nome_jogo in conector.jogos["nome"]:
            if nome_jogo == nome:
                conector.set_app_id(conector.jogos["codigo"][pos])
            pos = pos+1
        self.ids.codigo_jogo.text = str(conector.get_app_id())

    def criar_thread_pesquisa(self):
        self.pesquisa()

    def adcionar_botoes(self,conector):
        for i in range(len(conector.jogos)):
            self.children[0].add_widget(Button(text="criou"))

class Interface(App):
    def build(self):
        return Tela()

Interface().run()