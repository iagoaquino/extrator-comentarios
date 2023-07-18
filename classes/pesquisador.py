from classes.automato import Automato
import threading
import requests
class Pesquisador:
    def __init__(self):
        self.letras = "qazwsxedcrfvtgbyhnujmikolpç"
        self.numeros = "1234567890"
        self.simbolos = ",<.>;:/?~^=+!@#$%¨&*()-_ "
        self.quantidade_total_jogos = 0
        self.quantidade_total_jogos_analisados = 0
        self.jogos = {
            "nome" : [],
            "codigo" : []
        }

    def set_quantidade_total_jogos(self,quantidade_total_jogos):
        self.quantidade_total_jogos = quantidade_total_jogos
    
    def get_quantidade_total_jogos(self):
        return self.quantidade_total_jogos
    
    def set_quantidade_total_jogos_analisados(self, quantidade_total_jogos_analisados):
        self.quantidade_total_jogos_analisados = quantidade_total_jogos_analisados

    def get_quantidade_total_jogos_analisados(self):
        return self.quantidade_total_jogos_analisados
    
    def get_alfabeto(self):
        return self.letras + self.letras.upper() + self.simbolos + self.numeros
    
    def pesquisar_nome(self, vetor, automato):
        for conteudo in vetor:
            self.set_quantidade_total_jogos_analisados(self.get_quantidade_total_jogos_analisados()+1)
            nome = conteudo["name"]
            estado_atual = 0
            for letra in nome:
                checador = 0
                estado_atual,checador = automato.fazer_transicao(estado_atual,letra.lower())
                if automato.checar_aceitacao(estado_atual) == 1:
                    self.jogos["nome"].append(conteudo["name"])
                    self.jogos["codigo"].append(conteudo["codigo"])
                    break
    
    def criar_automato_busca(self,nome):
        automato_padrao = Automato(self.get_alfabeto(),len(nome)+1)
        for pos in range(len(nome)):
            if pos == 0:
                automato_padrao.adicionar_transicao(pos,nome[pos],pos+1)
                for letra in self.get_alfabeto():
                    if letra != nome[pos]: 
                        automato_padrao.adicionar_transicao(pos,letra,pos)   
            elif pos == 1:
                automato_padrao.adicionar_transicao(pos,nome[pos],pos+1)
                automato_padrao.adicionar_transicao(pos,nome[pos-1],pos)
                for letra in self.get_alfabeto():
                    if letra != nome[pos] and letra != nome[pos-1]:
                        automato_padrao.adicionar_transicao(pos,letra,0)
            else:
                automato_padrao.adicionar_transicao(pos, nome[pos],pos+1)
                for letra in self.get_alfabeto():
                    if letra != nome[pos]:
                        automato_padrao.adicionar_transicao(pos,letra,0)
        automato_padrao.definir_aceitacao(len(nome))
        return automato_padrao
    
    def pesquisar_jogo(self,nome):
        lista_jogos = []
        dados = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        print(dados)
        automato = self.criar_automato_busca(nome,self.get_alfabeto())
        dados = dados.json()
        dados = dados["applist"]["apps"]
        self.set_quantidade_total_jogos(len(dados))
        self.set_quantidade_total_jogos_analisados(0)
        self.jogos["nome"] = []
        self.jogos["codigo"] = []
        primeira_metade        = dados[0 * int(len(dados)/5)        : 1 * int(len(dados)/5)  + 1]
        segunda_metade         = dados[1 * int(len(dados)/5)    + 1 : 2 * int(len(dados)/5)  + 1]
        teceira_metade         = dados[2 * int(len(dados)/5)    + 1 : 3 * int(len(dados)/5)  + 1]
        quarta_metade          = dados[3 * int(len(dados)/5)    + 1 : 4 * int(len(dados)/5)  + 1]
        quinta_metade          = dados[4 * int(len(dados)/5)    + 1 : 5 * int(len(dados)/5)  + 1]

        #sexta_metade           = dados[5 * int(len(dados)/6)    + 1 : 6 * int(len(dados)/6)  + 1]
        #setima_metade          = dados[6 * int(len(dados)/20)    + 1 : 7 * int(len(dados)/20)  + 1]
        #oitava_metade          = dados[7 * int(len(dados)/20)    + 1 : 8 * int(len(dados)/20)  + 1]
        #nona_metade            = dados[8 * int(len(dados)/20)    + 1 : 9 * int(len(dados)/20)  + 1]   
        #decima_metade          = dados[9 * int(len(dados)/20)    + 1 : 10 * int(len(dados)/20) + 1]
        #decima_primeira_metade = dados[10* int(len(dados)/20)    + 1 : 11 * int(len(dados)/20) + 1]
        #decima_segunda_metade  = dados[11 * int(len(dados)/20)   + 1 : 12 * int(len(dados)/20) + 1]
        #decima_terceira_metade = dados[12 * int(len(dados)/20)   + 1 : 13 * int(len(dados)/20) + 1]
        #decima_quarta_metade   = dados[13 * int(len(dados)/20)   + 1 : 14 * int(len(dados)/20) + 1]
        #decima_quinta_metade   = dados[14 * int(len(dados)/20)   + 1 : 15 * int(len(dados)/20) + 1]
        #decima_sexta_metade    = dados[15 * int(len(dados)/20)   + 1 : 16 * int(len(dados)/20) + 1]
        #decima_setima_metade   = dados[16 * int(len(dados)/20)   + 1 : 17 * int(len(dados)/20) + 1]
        #decima_oitava_metade   = dados[17 * int(len(dados)/20)   + 1 : 18 * int(len(dados)/20) + 1]
        #decima_nona_metade     = dados[18 * int(len(dados)/20)   + 1 : 19 * int(len(dados)/20) + 1]
        #vigesima_metade        = dados[19 * int(len(dados)/20)   + 1 : int(len(dados))]

        threading.Thread(target=self.pesquisar_nome, args=(primeira_metade, automato, ), daemon=True).start()
        threading.Thread(target=self.pesquisar_nome, args=(segunda_metade, automato, ), daemon=True).start()
        threading.Thread(target=self.pesquisar_nome, args=(teceira_metade, automato, ), daemon=True).start()
        threading.Thread(target=self.pesquisar_nome, args=(quarta_metade, automato, ), daemon=True).start()
        threading.Thread(target=self.pesquisar_nome, args=(quinta_metade, automato, ), daemon=True).start()
        
        #threading.Thread(target=percorrer_vetor, args=(sexta_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(setima_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(oitava_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(nona_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_primeira_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_segunda_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_terceira_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_quarta_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_quinta_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_sexta_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_setima_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_oitava_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(decima_nona_metade, automato, ), daemon=True).start()
        #threading.Thread(target=percorrer_vetor, args=(vigesima_metade, automato, ), daemon=True).start()

    

    

    