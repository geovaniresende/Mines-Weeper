from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six.moves import range
from six.moves import tkinter

import functools


class GUI(tkinter.Frame, object):
  @classmethod
  def main(cls, width, height, callback):
    root = tkinter.Tk()
    window = cls(root, width, height, callback)
    root.mainloop()

  def __init__(self, master, width, height, callback):
    super(GUI, self).__init__(master)
    self.__width = width
    self.__height = height
    self.__build_buttons()
    self.grid()
    callback(self._push)

  def __build_buttons(self):
    self.__buttons = []
    for y in range(self.__height):
      row = []
      for x in range(self.__width):
        button = tkinter.Button(self)
        button.grid(row=y, column=x)
        button['text'] = '  '
        command = functools.partial(self._push, y, x)
        row.append(button)
      self.__buttons.append(row)

  def _push(self, **kwargs):
    self.__buttons[kwargs['row'] - 1][kwargs['col']
                                      - 1]['text'] = kwargs['val']
    self.update()
