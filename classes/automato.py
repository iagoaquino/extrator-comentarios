
class Estado:
    def __init__(self):
        self.transicoes = []
        self.transicoes_estrela = []
    def mostrar_transicoes(self):
        print(self.transicoes)
    def mostrar_transicoes_estrela(self):
        print(self.transicoes_estrela)
#definição classe automato    
class Automato:
    def __init__(self,palavras,quant_estados):
        self.alfabeto = []
        self.estados = []
        self.estados_aceitacao = []
        for i in range(quant_estados):
            estado = Estado()
            self.estados.append(estado)
        for letra in palavras:
            if  letra not in self.alfabeto:
                self.alfabeto.append(letra)
#metodos   
    def adicionar_transicao(self,estado_atual,alfabeto,estado_transicao):
        if alfabeto in self.alfabeto and estado_transicao in range(len(self.estados)):
            transicao = []
            transicao.append(alfabeto)
            transicao.append(estado_transicao)
            self.estados[estado_atual].transicoes.append(transicao)
        else:
            print("erro não foi possivel computar") 

    def adicionar_transicao_estrela(self,estado_atual,alfabeto,estado_transicao):
        if alfabeto in self.alfabeto and estado_transicao in range(len(self.estados)):
            transicao = []
            transicao.append(alfabeto)
            transicao.append(estado_transicao)
            self.estados[estado_atual].transicoes_estrela.append(transicao)
        else:
            print("erro não foi possivel computar") 

    def definir_aceitacao(self,num_estado):
        self.estados_aceitacao.append(num_estado)

    def checar_aceitacao(self,estado_atual):
        if estado_atual in self.estados_aceitacao:
            return 1
        return 0

    def fazer_transicao(self,estado_atual,alfabeto):
        novo_estado = estado_atual
        fez_transicao = 0
        for i in range(len(self.estados[estado_atual].transicoes)):
            if alfabeto == self.estados[estado_atual].transicoes[i][0]:
                novo_estado = self.estados[estado_atual].transicoes[i][1]
                fez_transicao = 1
        if fez_transicao == 1:
            return novo_estado,1
        else:
            return novo_estado,0
    
    def fazer_transicao_estrela(self,estado_atual,letra):
        novo_estado = estado_atual
        for i in range(len(self.estados[estado_atual].transicoes_estrela)):
            #print(letra+", transicoes estrela"+str(self.estados[estado_atual].transicoes_estrela[i][0]))
            if letra == self.estados[estado_atual].transicoes_estrela[i][0]:
                novo_estado = self.estados[estado_atual].transicoes_estrela[i][1]
                return novo_estado,1
        return novo_estado,0
            
    def mostrar_alfabeto(self):
        print(self.alfabeto)

    def mostrar_tamanho_estados(self):
        print(len(self.estados))

    def mostrar_transicoes(self):
        for pos in range(len(self.estados)):
            print("estado: "+str(pos))
            self.estados[pos].mostrar_transicoes()

    def mostrar_transicoes_estrela(self):
        for pos in range(len(self.estados)):
            print("estado: "+str(pos))
            self.estados[pos].mostrar_transicoes_estrela()
                    
    def mostrar_aceitacao(self):
        print(self.estados_aceitacao)

