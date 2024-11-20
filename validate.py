from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six.moves import range

import argparse
import random
import signal
import os
import json

import play


class TimeoutException(Exception):
  pass


def killgame(signum, frame):
  raise TimeoutException()


def save_validation_statistics(wins,
                               tles,
                               n_matches,
                               rows,
                               cols,
                               n_bombs,
                               player_type,
                               seed,
                               heuristic,
                               time_limit,
                               path=None):
  # transforma parametros do jogo em string identificadora
  id_str = 'b{}x{}-m{}-n{}-p{}-h{}-t{}-s{}.json'.format(
      rows, cols, n_bombs, n_matches, player_type, heuristic, time_limit, seed)

  # encontra caminho para arquivo de resultados
  if path is None:
    path = os.path.abspath('.')

  # salva dados em arquivo
  with open(os.path.join(path, id_str), 'w') as f:
    print(
        json.dumps({
            'board': (rows, cols),
            'n_mines': n_bombs,
            'player_type': player_type,
            'wins': wins,
            'losses': n_matches - wins - tles,
            'tles': tles,
            'heuristic': heuristic,
            'time_limit': time_limit
        }),
        file=f)


def main(player_type, rows, cols, n_bombs, seed, heuristic, time_limit,
         n_matches, save_path):
  # configura sinal de timeout
  signal.signal(signal.SIGALRM, killgame)

  # configura semente aleatoria
  random.seed(seed)

  # conta jogos vencidos e timeouts
  wins = 0
  tles = 0

  for _ in range(n_matches):
    # configura alarme de timeout
    signal.alarm(time_limit)

    # pega semente aleatoria para gerar um jogo
    game_seed = random.getrandbits(10)

    # joga enquanto o tempo nao e esgotado
    try:
      wins += play.main(
          player_type,
          rows,
          cols,
          n_bombs,
          game_seed,
          heuristic,
          gui_mode=False)
    except TimeoutException:
      print('TLE')
      tles += 1

  # salva resultado do experimento
  save_validation_statistics(wins, tles, n_matches, rows, cols, n_bombs,
                             player_type, seed, heuristic, time_limit,
                             save_path)


if __name__ == "__main__":
  # parseia argumentos da linha de comando
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--rows', type=int, required=True, help='Numero de linhas do campo.')
  parser.add_argument(
      '--cols', type=int, required=True, help='Numero de colunas do campo.')
  parser.add_argument(
      '--n_bombs', type=int, required=True, help='Numero de bombas no campo.')
  parser.add_argument('--seed', type=str, help='Semente aleatoria.')
  parser.add_argument(
      '--n_matches',
      type=int,
      required=True,
      help='Numero de partidas a serem jogadas.')
  parser.add_argument(
      '--player_type', required=True, type=str, help='Tipo de jogador.')
  parser.add_argument(
      '--heuristic', type=str, help='Heuristica a ser utilizada.')
  parser.add_argument(
      '--time_limit',
      type=int,
      required=True,
      help='Tempo limite em segundos.')
  parser.add_argument(
      '--save_path',
      type=str,
      help='Caminho para salvar arquivo de resultados.')
  FLAGS, _ = parser.parse_known_args()

  main(FLAGS.player_type, FLAGS.rows, FLAGS.cols, FLAGS.n_bombs, FLAGS.seed,
       FLAGS.heuristic, FLAGS.time_limit, FLAGS.n_matches, FLAGS.save_path)
