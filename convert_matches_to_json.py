from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six.moves import range

import sys
import os
import json
import numpy as np


def main(stats_path, save_path=None):
  # carrega estatisticas do arquivo
  stats = np.loadtxt(stats_path)

  # identifica vitorias
  wins = stats[stats != -1]

  # conta derrotas
  losses = len(stats) - len(wins)

  # computa estatisticas das vitorias
  mean = np.mean(wins)
  std = np.std(wins)

  # encontra caminho para arquivo de resultados
  if save_path is None:
    save_path = os.path.abspath('.')

  for i in range(4):
    # calcula tempo limite da marca
    tl = int(round(mean + i * std))

    # formata nome do arquivo de resultados
    id_str = 'b8x8-m10-n50-puser-hNone-t{}-sNone.json'.format(tl)

    # calcula vitorias e tempo excedidos
    win_count = np.sum(wins <= mean + i * std)
    tles = len(stats) - win_count - losses

    with open(os.path.join(save_path, id_str), 'w') as f:
      print(
          json.dumps({
              'board': (8, 8),
              'n_mines': 10,
              'player_type': 'user',
              'wins': win_count,
              'losses': losses,
              'tles': tles,
              'heuristic': None,
              'time_limit': tl
          }),
          file=f)


if __name__ == "__main__":
  main(sys.argv[1], sys.argv[2])
