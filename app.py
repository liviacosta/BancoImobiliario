from banco_imobiliario import BancoImobiliario

NUM_PARTIDAS_TIME_OUT = 1000

if __name__ == '__main__':
    BancoImobiliario(total_rodada=NUM_PARTIDAS_TIME_OUT).run()
