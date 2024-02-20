#!/usr/bin/env python3
# Originally from http://waf.googlecode.com/svn/trunk/waflib/ansiterm.py
# Taken from https://github.com/pycontribs/tendo/blob/master/tendo/ansiterm.py
import sys
import os
from ctypes import windll, c_short, c_int, c_ulong, c_char

try:

    if (not sys.stderr.isatty()) or (not sys.stdout.isatty()):
        raise ValueError('not a tty')

    from ctypes import *  # noqa

    class COORD(Structure):
        _fields_ = [("X", c_short), ("Y", c_short)]

    class SMALL_RECT(Structure):
        _fields_ = [
            ("Left", c_short), ("Top", c_short), ("Right", c_short),
            ("Bottom", c_short)
        ]

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        _fields_ = [
            ("Size", COORD), ("CursorPosition", COORD),
            ("Attributes", c_short), ("Window", SMALL_RECT),
            ("MaximumWindowSize", COORD)
        ]

    class CONSOLE_CURSOR_INFO(Structure):
        _fields_ = [('dwSize', c_ulong), ('bVisible', c_int)]

    sbinfo = CONSOLE_SCREEN_BUFFER_INFO()
    csinfo = CONSOLE_CURSOR_INFO()
    hconsole = windll.kernel32.GetStdHandle(-11)
    windll.kernel32.GetConsoleScreenBufferInfo(hconsole, byref(sbinfo))
    if sbinfo.Size.X < 10 or sbinfo.Size.Y < 10:
        raise Exception('small console')
    windll.kernel32.GetConsoleCursorInfo(hconsole, byref(csinfo))

except Exception:
    pass

else:
    import re
    import threading

    try:
        _type = unicode
    except:
        _type = str

    def to_int(number, default):
        return number and int(number) or default
    wlock = threading.Lock()

    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    class AnsiTerm(object):

        def __init__(self):
            self.encoding = sys.stdout.encoding
            self.hconsole = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            self.cursor_history = []
            self.orig_sbinfo = CONSOLE_SCREEN_BUFFER_INFO()
            self.orig_csinfo = CONSOLE_CURSOR_INFO()
            windll.kernel32.GetConsoleScreenBufferInfo(
                self.hconsole, byref(self.orig_sbinfo)
            )
            windll.kernel32.GetConsoleCursorInfo(
                hconsole, byref(self.orig_csinfo)
            )

        def screen_buffer_info(self):
            sbinfo = CONSOLE_SCREEN_BUFFER_INFO()
            windll.kernel32.GetConsoleScreenBufferInfo(
                self.hconsole, byref(sbinfo)
            )
            return sbinfo

        def clear_line(self, param):
            mode = param and int(param) or 0
            sbinfo = self.screen_buffer_info()
            if mode == 1:  # Clear from begining of line to cursor position
                line_start = COORD(0, sbinfo.CursorPosition.Y)
                line_length = sbinfo.Size.X
            elif mode == 2:  # Clear entire line
                line_start = COORD(
                    sbinfo.CursorPosition.X, sbinfo.CursorPosition.Y
                )
                line_length = sbinfo.Size.X - sbinfo.CursorPosition.X
            else:  # Clear from cursor position to end of line
                line_start = sbinfo.CursorPosition
                line_length = sbinfo.Size.X - sbinfo.CursorPosition.X
            chars_written = c_int()
            windll.kernel32.FillConsoleOutputCharacterA(
                self.hconsole, c_char(b' '), line_length, line_start,
                byref(chars_written)
            )
            windll.kernel32.FillConsoleOutputAttribute(
                self.hconsole, sbinfo.Attributes, line_length, line_start,
                byref(chars_written)
            )

        def clear_screen(self, param):
            mode = to_int(param, 0)
            sbinfo = self.screen_buffer_info()
            if mode == 1:  # Clear from begining of screen to cursor position
                clear_start = COORD(0, 0)
                clear_length = (
                    sbinfo.CursorPosition.X * sbinfo.CursorPosition.Y
                )
            elif mode == 2:  # Clear entire screen and return cursor to home
                clear_start = COORD(0, 0)
                clear_length = sbinfo.Size.X * sbinfo.Size.Y
                windll.kernel32.SetConsoleCursorPosition(
                    self.hconsole, clear_start
                )
            else:  # Clear from cursor position to end of screen
                clear_start = sbinfo.CursorPosition
                clear_length = (
                    (sbinfo.Size.X - sbinfo.CursorPosition.X) +
                    sbinfo.Size.X * (sbinfo.Size.Y - sbinfo.CursorPosition.Y)
                )
            chars_written = c_int()
            windll.kernel32.FillConsoleOutputCharacterA(
                self.hconsole, c_char(b' '), clear_length, clear_start,
                byref(chars_written)
            )
            windll.kernel32.FillConsoleOutputAttribute(
                self.hconsole, sbinfo.Attributes, clear_length, clear_start,
                byref(chars_written)
            )

        def push_cursor(self, param):
            sbinfo = self.screen_buffer_info()
            self.cursor_history.push(sbinfo.CursorPosition)

        def pop_cursor(self, param):
            if self.cursor_history:
                old_pos = self.cursor_history.pop()
                windll.kernel32.SetConsoleCursorPosition(
                    self.hconsole, old_pos)

        def set_cursor(self, param):
            x, sep, y = param.partition(';')
            x = to_int(x, 1) - 1
            y = to_int(y, 1) - 1
            sbinfo = self.screen_buffer_info()
            new_pos = COORD(
                min(max(0, x), sbinfo.Size.X),
                min(max(0, y), sbinfo.Size.Y)
            )
            windll.kernel32.SetConsoleCursorPosition(self.hconsole, new_pos)

        def set_column(self, param):
            x = to_int(param, 1) - 1
            sbinfo = self.screen_buffer_info()
            new_pos = COORD(
                min(max(0, x), sbinfo.Size.X),
                sbinfo.CursorPosition.Y
            )
            windll.kernel32.SetConsoleCursorPosition(self.hconsole, new_pos)

        def move_cursor(self, x_offset=0, y_offset=0):
            sbinfo = self.screen_buffer_info()
            new_pos = COORD(
                min(max(0, sbinfo.CursorPosition.X + x_offset), sbinfo.Size.X),
                min(max(0, sbinfo.CursorPosition.Y + y_offset), sbinfo.Size.Y)
            )
            windll.kernel32.SetConsoleCursorPosition(self.hconsole, new_pos)

        def move_up(self, param):
            self.move_cursor(y_offset=-to_int(param, 1))

        def move_down(self, param):
            self.move_cursor(y_offset=to_int(param, 1))

        def move_left(self, param):
            self.move_cursor(x_offset=-to_int(param, 1))

        def move_right(self, param):
            self.move_cursor(x_offset=to_int(param, 1))

        def next_line(self, param):
            sbinfo = self.screen_buffer_info()
            self.move_cursor(
                x_offset=-sbinfo.CursorPosition.X,
                y_offset=to_int(param, 1)
            )

        def prev_line(self, param):
            sbinfo = self.screen_buffer_info()
            self.move_cursor(
                x_offset=-sbinfo.CursorPosition.X,
                y_offset=-to_int(param, 1)
            )

        escape_to_color = {
            (0, 30): 0x0,  # black
            (0, 31): 0x4,  # red
            (0, 32): 0x2,  # green
            (0, 33): 0x4 + 0x2,  # dark yellow
            (0, 34): 0x1,  # blue
            (0, 35): 0x1 + 0x4,  # purple
            (0, 36): 0x2 + 0x4,  # cyan
            (0, 37): 0x1 + 0x2 + 0x4,  # grey
            (1, 30): 0x1 + 0x2 + 0x4,  # dark gray
            (1, 31): 0x4 + 0x8,  # red
            (1, 32): 0x2 + 0x8,  # light green
            (1, 33): 0x4 + 0x2 + 0x8,  # yellow
            (1, 34): 0x1 + 0x8,  # light blue
            (1, 35): 0x1 + 0x4 + 0x8,  # light purple
            (1, 36): 0x1 + 0x2 + 0x8,  # light cyan
            (1, 37): 0x1 + 0x2 + 0x4 + 0x8,  # white
        }

        def set_color(self, param):
            cols = param.split(';')
            attr = self.orig_sbinfo.Attributes
            for c in cols:
                c = to_int(c, 0)
                if c in range(30, 38):
                    attr = (attr & 0xf0) | (
                        self.escape_to_color.get((0, c), 0x7)
                    )
                elif c in range(40, 48):
                    attr = (attr & 0x0f) | (
                        self.escape_to_color.get((0, c), 0x7) << 8
                    )
                elif c in range(90, 98):
                    attr = (attr & 0xf0) | (
                        self.escape_to_color.get((1, c - 60), 0x7)
                    )
                elif c in range(100, 108):
                    attr = (attr & 0x0f) | (
                        self.escape_to_color.get((1, c - 60), 0x7) << 8
                    )
                elif c == 1:
                    attr |= 0x08
            windll.kernel32.SetConsoleTextAttribute(self.hconsole, attr)

        def show_cursor(self, param):
            csinfo.bVisible = 1
            windll.kernel32.SetConsoleCursorInfo(self.hconsole, byref(csinfo))

        def hide_cursor(self, param):
            csinfo.bVisible = 0
            windll.kernel32.SetConsoleCursorInfo(self.hconsole, byref(csinfo))

        ansi_command_table = {
            'A': move_up,
            'B': move_down,
            'C': move_right,
            'D': move_left,
            'E': next_line,
            'F': prev_line,
            'G': set_column,
            'H': set_cursor,
            'f': set_cursor,
            'J': clear_screen,
            'K': clear_line,
            'h': show_cursor,
            'l': hide_cursor,
            'm': set_color,
            's': push_cursor,
            'u': pop_cursor,
        }
        # Match either escape sequence or text not containing escape sequence
        ansi_tokens = re.compile(r'(?:\x1b\[([0-9?;]*)([a-zA-Z])|([^\x1b]+))')

        def write(self, text):
            try:
                wlock.acquire()
                for param, cmd, txt in self.ansi_tokens.findall(text):
                    if cmd:
                        cmd_func = self.ansi_command_table.get(cmd)
                        if cmd_func:
                            cmd_func(self, param)
                    else:
                        chars_written = c_int()
                        if isinstance(txt, _type):
                            windll.kernel32.WriteConsoleW(
                                self.hconsole, txt, len(txt),
                                byref(chars_written), None
                            )
                        else:
                            windll.kernel32.WriteConsoleA(
                                self.hconsole, txt, len(txt),
                                byref(chars_written), None
                            )
            finally:
                wlock.release()

        def flush(self):
            pass

        def isatty(self):
            return True

    sys.stderr = sys.stdout = AnsiTerm()
    os.environ['TERM'] = 'vt100'
