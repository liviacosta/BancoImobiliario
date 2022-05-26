import random


class Tabuleiro:
    def __init__(self):
        self.propriedades: [Propriedade] = []
        self.jogadores: [Jogador] = []
        self.rodada: int = 1

    def adicionar_propriedade(self, propriedade):
        self.propriedades.append(propriedade)

    def adicionar_jogadores(self, jogadores):
        for j in jogadores:
            j.saldo = 300
            j.posicao_tabuleiro = 0
            j.ainda_no_jogo = True
            j.qtd_jogadas = 0
            self.jogadores.append(j)

    def sortear_ordem_jogadores(self):
        random.shuffle(self.jogadores)

    def remove_jogador(self, jogador):
        self.jogadores.remove(jogador)

    def devolve_propriedade(self, jogador):
        for propriedade in self.propriedades:
            if propriedade.proprietario == jogador:
                propriedade.devolver_para_banco()


class Propriedade:
    def __init__(self, nome, preco_compra, preco_aluguel, proprietario=None):
        self.nome = nome
        self.preco_compra = preco_compra
        self.preco_aluguel = preco_aluguel
        self.proprietario = proprietario

    def __repr__(self):
        return f'{self.nome}'

    def disponivel_para_compra(self):
        return self.proprietario is None

    def comprar(self, jogador: 'Jogador'):
        if self.disponivel_para_compra():
            if jogador.jogador_tem_saldo_suficiente(self.preco_compra):
                jogador.atualiza_saldo(self.preco_compra)
                self.proprietario = jogador
                return True
        return False

    def recebe_aluguel(self, jogador: 'Jogador'):
        if jogador.jogador_tem_saldo_suficiente(self.preco_aluguel):
            jogador.atualiza_saldo(self.preco_aluguel)
            self.proprietario.saldo += self.preco_aluguel
        else:
            jogador.atualiza_saldo(self.preco_aluguel)

    def devolver_para_banco(self):
        self.proprietario = None
        return True


class Jogador:
    def __init__(self, nome, saldo_inicial=300.00):
        self.nome = nome
        self.saldo = saldo_inicial
        self.ainda_no_jogo = True
        self.posicao_tabuleiro = 0
        self.saldo_inicial = saldo_inicial
        self.credito_rodada = 100
        self.qtd_jogadas = 0

    def __repr__(self):
        return f'{self.nome}'

    def atualiza_saldo(self, amount):
        self.saldo = self.saldo - amount

    def jogador_tem_saldo_suficiente(self, valor_a_pagar):
        return True if self.saldo >= valor_a_pagar else False

    def valida_jogador_no_jogo(self):
        if self.saldo < 0:
            self.ainda_no_jogo = False
        return self.ainda_no_jogo

    def anda(self):
        dado = random.choice(range(1, 7))
        self.posicao_tabuleiro += dado
        self.qtd_jogadas += 1

        if self.posicao_tabuleiro > 19:
            self.posicao_tabuleiro -= 19
            self.saldo += self.credito_rodada

        return self.posicao_tabuleiro

    def mensagem_compra(self, propriedade):
        print(f"Jogador ({self.nome.upper()}) - Comprou a propriedade ({propriedade.nome.upper()}) por ${propriedade.preco_compra}")
        print(f"Jogador ({self.nome.upper()}) - Saldo -> ${self.saldo}")

    def mensagem_nao_vai_comprar(self, propriedade):
        print(f"Jogador ({self.nome.upper()}) - Não comprará a propriedade ({propriedade.nome.upper()})")


class Impulsivo(Jogador):
    def checa_perfil_compra_propriedade(self, propriedade):
        if self.saldo >= propriedade.preco_compra:
            propriedade.comprar(self)
            return True
        return False


class Exigente(Jogador):
    def checa_perfil_compra_propriedade(self, propriedade):
        if self.saldo >= propriedade.preco_compra and propriedade.preco_aluguel > 50:
            propriedade.comprar(self)
            return True
        return False


class Cauteloso(Jogador):
    def checa_perfil_compra_propriedade(self, propriedade):
        if self.saldo - propriedade.preco_compra >= 80:
            propriedade.comprar(self)
            return True
        return False


class Aleatorio(Jogador):
    def checa_perfil_compra_propriedade(self, propriedade):
        if self.saldo >= propriedade.preco_compra and random.choice([True, False]):
            propriedade.comprar(self)
            return True
        return False
