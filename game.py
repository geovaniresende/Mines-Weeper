from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import itertools


class Game:

  def __init__(self, rows, cols, n_bombs, seed=None, callback=None):
    # inicializa funcao de callback
    self._callback = callback

    # inicializa status do jogo
    self.game_over = False
    self.victory = False

    # atributos do jogo
    self._rows = rows
    self._cols = cols
    self._n_bombs = n_bombs
    self._n_invisible_cells = rows * cols

    # tabuleiros interno e visivel
    bombs = np.zeros([rows + 2, cols + 2], dtype=np.uint8)
    self._board = np.zeros(bombs.shape, dtype=np.int8)
    self.board = -np.ones(bombs.shape, dtype=np.int8)

    # sorteia com base na semente da entrada
    np.random.seed(seed)

    # sorteia "n_bombs" posicoes para se colocar bombas
    y = np.arange(1, rows + 1, dtype=np.uint8)
    x = np.arange(1, cols + 1, dtype=np.uint8)
    pos = np.transpose([np.repeat(x, rows), np.tile(y, cols)])
    np.random.shuffle(pos)
    y = pos[:self._n_bombs, 0]
    x = pos[:self._n_bombs, 1]
    bombs[y, x] = 1

    # calcula quantidade bombas adjacentes a cada celula
    for i in range(self._rows):
      for j in range(self._cols):
        self._board[i + 1, j + 1] = np.sum(bombs[i:i + 3, j:j + 3])

    # unifica tabuleiros internos
    self._board[bombs == 1] = -1

    # corta ultima linha e coluna
    self._board = self._board[:rows + 1, :cols + 1]
    self.board = self.board[:rows + 1, :cols + 1]

    # facilita visualizacao
    self.board[0] = np.arange(self.board.shape[0])
    self.board[:, 0] = np.arange(self.board.shape[0])

  def _callback_handler(self, row, col, val):
    if self._callback is not None:
      self._callback(row=row, col=col, val=val)

  def click(self, i, j):
    # se clicou em bomba, fim de jogo
    if self._board[i, j] == -1:
      self.game_over = True

      if self._callback is not None:
        self._callback(row=i, col=j, val='*')

      return

    # ignorar cliques em celulas ja clicadas
    if self.board[i, j] > -1:
      return

    # abre celula atual
    self._n_invisible_cells -= 1
    self.board[i, j] = self._board[i, j]
    self._callback_handler(i, j, self._board[i, j])

    # expande celula atual
    ngh = list(itertools.product((-1, 0, 1), (-1, 0, 1)))
    q = [(i, j)]
    for i, j in q:
      # se celula nao possui bombas adjacentes, abre celulas vizinhas
      if self.board[i, j] == 0:
        for di, dj in ngh:
          if 0 < i + di <= self._rows and \
              0 < j + dj <= self._cols and \
              self.board[i + di, j + dj] == -1:
            # abre celula vizinha
            self._n_invisible_cells -= 1
            self.board[i + di, j + dj] = self._board[i + di, j + dj]
            self._callback_handler(i + di, j + dj, self._board[i + di, j + dj])

            # celula vizinha sera expandida
            q.append((i + di, j + dj))

    # checa se jogo foi vencido nesse movimento
    if self._n_invisible_cells == self._n_bombs:
      self.victory = True

  def flag(self, i, j):
    # so permite marcar celulas fechadas
    if self.board[i, j] == -1:
      self._callback_handler(i, j, 'F')
