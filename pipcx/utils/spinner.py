"""
Ref: https://gist.github.com/nicodebo/b68034445da9be238e706a2d8166cf79
"""

from enum import Enum
import itertools
import sys
import time
import threading


class Sequence(Enum):
    """Enumeration of spinner sequence
    Ref: https://stackoverflow.com/questions/2685435/cooler-ascii-spinners
    """
    BASIC = ['-', '/', '|', '\\']
    ARROW = ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙']
    VERT_BAR = ['▁', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃']
    HORIZ_BAR = ['▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉']
    SPIN_RECT = ['▖', '▘', '▝', '▗']
    ELAST_BAR = ['▌', '▀', '▐▄']
    TETRIS = ['┤', '┘', '┴', '└', '├', '┌', '┬', '┐']
    TRIANGLE = ['◢', '◣', '◤', '◥']
    SQUARE_QRT = ['◰', '◳', '◲', '◱']
    CIRCLE_QRT = ['◴', '◷', '◶', '◵']
    CIRCLE_HLF = ['◐', '◓', '◑', '◒']
    BALLOON = ['.', 'o', 'O', '@', '*']
    BLINK = ['◡◡', '⊙⊙', '◠◠']
    TURN = ['◜ ', ' ◝', ' ◞', '◟ ']
    LOSANGE = ['◇', '◈', '◆']
    BRAILLE = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']

    def describe(self):
        return self.name, self.value

    @classmethod
    def default_sequence(cls):
        return Sequence.BASIC


class Spinner:
    """A shell spinner
    """

    def __init__(self, message="", interval=0.25, sequence="HORIZ_BAR", offset=1):
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self.init_spin)
        self.interval = interval  # speed rotation
        self.message = message  # spinner text
        self.offset = offset  # number of space to pad on the left
        self.spinner_cycle = itertools.cycle(self.set_spinner_seq(sequence))

    @staticmethod
    def set_spinner_seq(sequence):
        seq_list = [name for name, members in Sequence.__members__.items()]
        if sequence.upper() in seq_list:
            seq = Sequence[sequence.upper()].value
        else:
            seq = Sequence.default_sequence().value
        return seq

    def start(self):
        self.spin_thread.start()

    def stop(self):
        self.stop_running.set()
        self.spin_thread.join()
        # make sure to clear the line in case printing something shorter after
        sys.stdout.write("\033[K")

    def init_spin(self):
        while not self.stop_running.is_set():
            if not self.message:
                cur_mess = next(self.spinner_cycle)
            else:
                cur_mess = "{} {}".format(next(self.spinner_cycle),
                                          self.message)
            cur_mess = cur_mess.rjust(len(cur_mess) + self.offset, ' ')
            sys.stdout.write(cur_mess)
            sys.stdout.flush()
            time.sleep(self.interval)
            sys.stdout.write('\b' * len(cur_mess))
