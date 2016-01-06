import contextlib
import functools
import sys
import random

from blessings import Terminal

terminal = Terminal()

@contextlib.contextmanager
def reset_on_exit():
    try:
        with terminal.fullscreen():
            sys.stdout.write(
                terminal.civis +
                terminal.on_black +
                terminal.clear
            )
            yield
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(terminal.cnorm + terminal.normal)

def center():
    return terminal.height // 2, terminal.width // 2


def rand_coord():
    return (
        random.randint(0, terminal.height - 1),
        random.randint(0, terminal.width - 1)
    )


def rand_color():
    assert terminal.number_of_colors > 0
    return terminal.on_color(random.randint(1, terminal.number_of_colors - 1))


def clip(strips):
    '''
    Yield a sequence of strips after clipping them to (0, 0) to (height, width).
    '''
    for y, x, length in strips:
        if not(0 <= y < terminal.height):
            continue
        if x < 0:
            length += x
            x = 0
        if length + x > terminal.width:
            length = terminal.width - x
        if length > 0:
            yield y, x, length


def render(strips):
    return ''.join(
        terminal.move(y, x) + ' ' * length
        for y, x, length in clip(strips)
    )

