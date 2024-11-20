from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def read_int(msg=''):
  return int(input(msg))


def str2bool(v):
  if v.lower() in ('yes', 'true', 't', 'y', '1'):
    return True
  elif v.lower() in ('no', 'false', 'f', 'n', '0'):
    return False
  else:
    raise argparse.ArgumentTypeError('Boolean value expected.')
