# antiga_logica.py

# if len(jogadas_rodada):
#             maior_carta_rodada = max(
#                 jogadas_rodada, key=lambda jogada: jogada.valor_carta
#             )
#             if maior_carta_rodada.jogador == self.parceiro:
#                 # descarte
#                 carta_jogada = self.get_menor_carta_mao()
#                 # print(f"Descarte da carta {carta_jogada.num}")
#             else:

#                 media_carta_mao = self.get_media_carta_mao()

#                 if media_carta_mao.num >= maior_carta_rodada.valor_carta:
#                     carta_jogada = media_carta_mao
#                 else:
#                     maior_carta_mao = self.get_maior_carta_mao()
#                     if maior_carta_mao.num >= maior_carta_rodada.valor_carta:
#                         # Cobrir a maior carta
#                         carta_jogada = maior_carta_mao
#                         # print(f"Cobre com a carta {carta_jogada.num}")
#                     else:
#                         # Descarte
#                         carta_jogada = self.get_menor_carta_mao()
#                         # print(f"Descarte da carta {carta_jogada.num}")
#     else:
#         # jogar a maior na primeira carta da rodada
#         carta_jogada = self.get_maior_carta_mao()
