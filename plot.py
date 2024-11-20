from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six.moves import range

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt


def plot(board_spec,
         n_mines,
         tl_spec,
         n_samples,
         wins,
         losses,
         tles,
         labels,
         path=None):
  indices = np.arange(n_samples)
  width = 0.45

  p_wins = plt.bar(indices, wins, width=width, color=(0, 0, 0.8))
  p_losses = plt.bar(
      indices, losses, bottom=wins, width=width, color=(0.8, 0, 0))
  p_tles = plt.bar(
      indices, tles, width=width, bottom=wins + losses, color=(0.7, 0, 0.7))

  plt.ylabel('Partidas (em %)')
  plt.title(
      'Performance de agentes em campo minado\nTabuleiro {}x{}, {} Minas\nTempo limite = {}s'.
      format(board_spec[0], board_spec[1], n_mines, tl_spec))
  plt.xticks(indices, labels)
  plt.yticks(np.arange(111, step=10), np.arange(101, step=10))
  plt.legend(
      (p_wins[0], p_losses[0], p_tles[0]), ('Vitorias', 'Derrotas',
                                            'Tempo excedido'),
      loc='upper left')

  if path is None:
    path = '.'
  path = os.path.abspath(path)

  plt.savefig(
      os.path.join(path, 'b{}x{}-m{}-t{}.png'.format(
          board_spec[0], board_spec[1], n_mines, tl_spec)),
      bbox_inches='tight')


def beautify(user, heur):
  if user == 'user':
    user = 'Humano'
  elif user == 'logical':
    user = 'Logico'

  if heur is None:
    return user
  elif heur == 'model_counting':
    return user + ' com contagem de modelos'


def retrieve_data(folder_path, board_spec, n_mines, tl_spec):
  # inicializa listas
  n_samples = 0
  wins = []
  losses = []
  tles = []
  labels = []

  # itera sobre os jsons da pasta dada
  for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.json'):
      # abre arquivo json
      data = json.load(open(os.path.join(folder_path, filename)))

      # checa se conforma com especificacao dada
      if board_spec == data['board'] and n_mines == data['n_mines'] and tl_spec == data['time_limit']:
        # converte para porcentagem
        total = data['wins'] + data['losses'] + data['tles']

        # converte dados
        wins.append(100 * data['wins'] // total)
        losses.append(100 * data['losses'] // total)
        tles.append(100 * data['tles'] // total)
        labels.append(beautify(data['player_type'], data['heuristic']))
        n_samples += 1

  return n_samples, np.array(wins), np.array(losses), np.array(tles), labels


if __name__ == '__main__':
  folder_path = sys.argv[1]
  save_path = sys.argv[2]

  for board_spec, n_mines, tl_spec in [([8, 8], 10, 59), ([8, 8], 10, 98),
                                       ([8, 8], 10, 136), ([8, 8], 10, 175)]:
    n_samples, wins, losses, tles, labels = retrieve_data(
        folder_path, board_spec, n_mines, tl_spec)
    plot(board_spec, n_mines, tl_spec, n_samples, wins, losses, tles, labels,
         save_path)
