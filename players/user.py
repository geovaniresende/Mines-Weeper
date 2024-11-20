from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def init():
  print('Type C #row #col to click on the cell (#row, #col)')
  print('Type F #row #col to mark cell (#row, #col) as a bomb')


def strategy(board):
  type_of_move, row, col = input().split()
  row = int(row)
  col = int(col)
  return type_of_move, row, col
