import string
import re
import urwid


_FIND_WORD_RE1 = re.compile(r'([a-zA-Z0-9_]+)')
_FIND_WORD_RE2 = re.compile(r'([^a-zA-Z0-9_]+)')


def _clamp(number, min_value, max_value):
    return max(min_value, min(max_value, number))


class ReadlineEdit(urwid.Text):
    signals = ['change']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._edit_pos = 0

    @property
    def edit_pos(self):
        return self._edit_pos

    @edit_pos.setter
    def edit_pos(self, pos):
        self._edit_pos = _clamp(pos, 0, len(self.text))
        self._invalidate()

    @property
    def text(self):
        return self.get_text()[0]

    @text.setter
    def text(self, text):
        self.set_text(text)
        self.edit_pos = _clamp(self.edit_pos, 0, len(text))
        urwid.signals.emit_signal(self, 'change', self, text)

    def render(self, size, focus=False):
        (maxcol,) = size
        canv = urwid.Text.render(self, (maxcol,))
        if focus:
            canv = urwid.CompositeCanvas(canv)
            canv.cursor = (min(self._edit_pos, maxcol - 1), 0)
        return canv

    def selectable(self):
        return True

    def keypress(self, _size, key):
        keymap = {
            'ctrl f':         self._forward_char,
            'ctrl b':         self._backward_char,
            'right':          self._forward_char,
            'left':           self._backward_char,
            'ctrl a':         self._beginning_of_line,
            'ctrl e':         self._end_of_line,
            'home':           self._beginning_of_line,
            'end':            self._end_of_line,
            'meta f':         self._forward_word,
            'meta b':         self._backward_word,
            'shift right':    self._forward_word,
            'shift left':     self._backward_word,

            'ctrl d':         self._delete_char,
            'ctrl h':         self._backward_delete_char,
            'delete':         self._delete_char,
            'backspace':      self._backward_delete_char,
            'ctrl u':         self._kill_whole_line,
            'ctrl k':         self._kill_line,
            'meta d':         self._kill_word,
            'ctrl w':         self._backward_kill_word,
            'meta backspace': self._backward_kill_word,
        }
        if key in keymap:
            keymap[key]()
            return None
        elif key in string.printable:
            self._insert_char_at_cusor(key)
            return None
        return key

    def _insert_char_at_cusor(self, key):
        self.text = (
            self.text[0:self.edit_pos] + key + self.text[self.edit_pos:])
        self.edit_pos += 1

    def _backward_char(self):
        if self.edit_pos > 0:
            self.edit_pos -= 1

    def _forward_char(self):
        if self.edit_pos < len(self.text):
            self.edit_pos += 1

    def _backward_word(self):
        iterator = _FIND_WORD_RE1.finditer(self.text[0:self.edit_pos][::-1])
        for match in iterator:
            self.edit_pos -= match.end(1)
            return
        self.edit_pos = 0

    def _forward_word(self):
        iterator = _FIND_WORD_RE2.finditer(self.text[self.edit_pos:])
        for match in iterator:
            self.edit_pos += match.end(1)
            return
        self.edit_pos = len(self.text)

    def _delete_char(self):
        if self.edit_pos < len(self.text):
            self.text = (
                self.text[0:self.edit_pos] + self.text[self.edit_pos+1:])

    def _backward_delete_char(self):
        if self.edit_pos > 0:
            self.text = (
                self.text[0:self.edit_pos-1] + self.text[self.edit_pos:])
            self.edit_pos -= 1

    def _kill_whole_line(self):
        self.text = ''
        self.edit_pos = 0

    def _kill_line(self):
        self.text = self.text[0:self.edit_pos]

    def _backward_kill_word(self):
        pos = self.edit_pos
        self._backward_word()
        self.text = self.text[0:self.edit_pos] + self.text[pos:]

    def _kill_word(self):
        pos = self.edit_pos
        self._forward_word()
        self.text = self.text[0:pos] + self.text[self.edit_pos:]
        self.edit_pos = pos

    def _beginning_of_line(self):
        self.edit_pos = 0

    def _end_of_line(self):
        self.edit_pos = len(self.text)
