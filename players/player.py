from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Player:

  def __init__(self, player):
    player.init()
    self.strategy = player.strategy

  def make_move(self, board):
    return self.strategy(board)
