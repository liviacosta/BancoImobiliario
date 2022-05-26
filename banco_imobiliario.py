from typing import List

from models import *

NUM_PROPRIEDADES = 20


class BancoImobiliario:
    def __init__(self, total_rodada: int):
        self.jogadores = self._get_jogadores()
        self.tabuleiro: Tabuleiro = Tabuleiro()
        self.total_rodada = total_rodada
        self.total_partidas = 0
        self.total_partidas_time_out = 0
        self.total_partidas_com_vitoria = 0
        self.vitorias = dict()
        self.total_turnos_por_partida = dict()

    def _get_jogadores(self):
        return [
            Impulsivo("Impulsivo"),
            Exigente("Exigente"),
            Cauteloso("Cauteloso"),
            Aleatorio("Aleatorio")
        ]

    def _populate_random_tabuleiro(self):
        for index in range(NUM_PROPRIEDADES):
            propriedade = f"Propriedade-{index}"
            self.tabuleiro.adicionar_propriedade(
                Propriedade(nome=propriedade, preco_compra=random.choice(range(50, 220)), preco_aluguel=random.choice(range(50, 100)))
            )

    def _iniciar_jogo(self):
        self._cria_novo_tabuleiro()
        self._jogar()

    def _cria_novo_tabuleiro(self):
        self.tabuleiro: Tabuleiro = Tabuleiro()
        self.tabuleiro.adicionar_jogadores(self.jogadores)
        self._populate_random_tabuleiro()

    def _jogar(self):
        while len(self.tabuleiro.jogadores) > 1 and self.tabuleiro.rodada < self.total_rodada:
            for n, jogador in enumerate(self.tabuleiro.jogadores):
                if not jogador.ainda_no_jogo:
                    break
                else:
                    jogador.anda()

                    propriedade = self.tabuleiro.propriedades[jogador.posicao_tabuleiro]

                    if propriedade.disponivel_para_compra():
                        jogador.checa_perfil_compra_propriedade(propriedade)

                    if propriedade.proprietario is not None and propriedade.proprietario is not jogador:
                        propriedade.recebe_aluguel(jogador)

                    if not jogador.valida_jogador_no_jogo():
                        self.tabuleiro.remove_jogador(jogador)
                        self.tabuleiro.devolve_propriedade(jogador)
                        if len(self.tabuleiro.jogadores) == 1:
                            break

            self.tabuleiro.rodada += 1

        if self.tabuleiro.rodada >= self.total_rodada:
            self.total_partidas_time_out += 1
            self._ordenar_saldo_jogadores()
        elif len(self.tabuleiro.jogadores) == 1:
            self.total_turnos_por_partida[self.total_partidas] = self.tabuleiro.rodada
            self.total_partidas_com_vitoria += 1
        self._adicionar_vitoria()

    def _ordenar_saldo_jogadores(self):
        self.tabuleiro.jogadores.sort(key=lambda x: (x.saldo, x.qtd_jogadas), reverse=True)
        return self.tabuleiro.jogadores

    def _adicionar_vitoria(self):
        if self.tabuleiro.jogadores[0].nome.upper() in self.vitorias.keys():
            self.vitorias[self.tabuleiro.jogadores[0].nome.upper()] += 1
        else:
            self.vitorias[self.tabuleiro.jogadores[0].nome.upper()] = 1

    def _partida(self):
        while self.total_partidas < 300:
            self._iniciar_jogo()
            self.total_partidas += 1

    def _get_porcentagem_vitoria(self, jogador: Jogador):
        if jogador.nome.upper() in self.vitorias.keys():
            total_vitorias_do_jogador = self.vitorias[jogador.nome.upper()]
            return '{:.2f}'.format((total_vitorias_do_jogador / 300)*100)
        return 0

    def _get_media_turno(self):
        return '{:.2f}'.format(sum(self.total_turnos_por_partida)/len(self.total_turnos_por_partida))

    def _get_jogador_mais_vitorioso(self):
        return max(self.vitorias, key=self.vitorias.get)

    def run(self):
        self._partida()
        print("#" * 20 + f" Total Partidas finalizadas por TIME OUT => {self.total_partidas_time_out}")
        print("#" * 20 + f" Média turnos por partida => {self._get_media_turno()}")
        print("#" * 20 + f" Porcentagem vitórias jogador IMPULSIVO => {self._get_porcentagem_vitoria(self.jogadores[0])}")
        print("#" * 20 + f" Porcentagem vitórias jogador EXIGENTE => {self._get_porcentagem_vitoria(self.jogadores[1])}")
        print("#" * 20 + f" Porcentagem vitórias jogador CAUTELOSO => {self._get_porcentagem_vitoria(self.jogadores[2])}")
        print("#" * 20 + f" Porcentagem vitórias jogador ALEATORIO => {self._get_porcentagem_vitoria(self.jogadores[3])}")
        print("#" * 20 + f" Jogador mais vitorioso => {self._get_jogador_mais_vitorioso()}")
