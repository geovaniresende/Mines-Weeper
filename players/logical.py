from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six.moves import range

import numpy as np


def model_counting_heuristic(board, current_moves, border_list):
  # checa se existe borda
  if len(current_moves):
    # encontra posicao que em menos modelos apresenta bomba
    least_bombed_pos = np.argmin(current_moves)

    # desempacota movimento escolhido
    row, col = border_list[least_bombed_pos]

    return 'C', row, col
  else:
    # fallback para movimento aleatorio
    return random_coherent_move(board, current_moves, border_list)


def random_coherent_move(board, current_moves, border_list):
  # determina celulas fechadas
  closed_cells = np.transpose(np.where(board == -1))

  # sorteia uniformemente uma das celulas disponiveis
  move_index = np.random.choice(len(closed_cells), 1)
  row, col = closed_cells[move_index[0]]

  return 'C', row, col


class LogicalPlayer:
  def __init__(self, no_move_strategy=None):
    self._sure_moves = []

    if no_move_strategy is not None:
      self._no_move_strategy = no_move_strategy
    else:
      self._no_move_strategy = random_coherent_move

  def init(self):
    pass

  def strategy(self, board):
    # se ainda ha movimentos no buffer, executa o proximo desses movimentos
    if len(self._sure_moves):
      move = self._sure_moves[0]
      self._sure_moves = self._sure_moves[1:]
      return move

    # determina modelos possiveis no tabuleiro atual
    current_moves, border_list = self._get_possible_board_models(board)

    # determina posicoes totalmente determinadas pelo campo ja preenchido
    self._sure_moves = self._get_sure_moves(current_moves, border_list)

    # joga nas aberturas possiveis se existirem, usa estrategia predefinida para essa situacao, caso contrario
    if len(self._sure_moves):
      move = self._sure_moves[0]
      self._sure_moves = self._sure_moves[1:]
      return move
    else:
      return self._no_move_strategy(board, current_moves, border_list)

  def _get_sure_moves(self, current_moves, border_list):
    # recupera movimentos que em todos os modelos sao seguros
    sure_moves = []
    for i, current_move in enumerate(current_moves):
      row, col = border_list[i]
      if current_move == 0:
        sure_moves.append(('C', row, col))

    return sure_moves

  def _get_possible_board_models(self, board):
    # determina posicoes na borda
    border_list, insiders_list = self._get_border_and_insiders(board)

    # salva os movimentos de modelos que atendem o tabuleiro
    current_moves = np.zeros(len(border_list), dtype=np.int64)

    # copia o tabuleiro para fazer computacoes
    safe_board = np.zeros_like(board, dtype=np.uint8)

    # itera sobre possibilidades
    for possibility in range(2**len(border_list)):
      # preenche a copia do tabuleiro de acordo com 'possibility'
      for index, border_pos in enumerate(border_list):
        # ve se 'possibility' preve bomba na posicao 'border_pos'
        has_bomb = bool(possibility & (1 << index))

        # desempacota 'border_pos'
        i, j = border_pos

        if has_bomb:
          safe_board[i, j] = 1
        else:
          safe_board[i, j] = 0

      # checa se modelo gerado e possivel
      if self._check_model_veracity(board, safe_board, insiders_list):
        # itera sobre as posicoes de borda e salva movimentos determinados por 'possibility'
        for index, border_pos in enumerate(border_list):
          # desempacota 'border_pos'
          i, j = border_pos

          current_moves[index] += safe_board[i, j]

    return current_moves, border_list

  def _get_border_and_insiders(self, board):
    border = []
    insiders = []
    for i, row in enumerate(board[1:, 1:]):
      for j, pos in enumerate(row):
        # checa se posicao esta aberta
        if pos != -1:
          # adiciona posicao aberta aos vizinhos da borda
          insiders.append((i + 1, j + 1))

          # itera sobre vizinhanca de posicao fechada buscando posicoes abertas
          for di in range(-1, 2):
            for dj in range(-1, 2):
              if i + di + 1 < board.shape[0] and \
                  j + dj + 1 < board.shape[1] and \
                  board[i + di + 1, j + dj + 1] == -1:
                border.append((i + di + 1, j + dj + 1))

    # remove elementos repetidos
    border = np.array(border, dtype=np.int32)
    if border.size:
      border = np.unique(border, axis=0)

    return border, insiders

  def _check_model_veracity(self, board, safe_board, insiders):
    # itera sobre posicoes abertas vizinhas a borda
    for i, j in insiders:
      # checa se modelo atende restricoes de posicao aberta '(i, j)'
      if np.sum(safe_board[i - 1:i + 2, j - 1:j + 2]) != board[i, j]:
        return False

    return True
