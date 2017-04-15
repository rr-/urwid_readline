import re
import string
import unicodedata
import urwid


def _clamp(number, min_value, max_value):
    return max(min_value, min(max_value, number))


def _is_valid_key(ch):
    return urwid.util.is_wide_char(ch, 0) or (len(ch) == 1 and ord(ch) >= 32)


class ReadlineEdit(urwid.Edit):
    ignore_focus = False

    def __init__(
            self,
            *args,
            word_chars=string.ascii_letters + string.digits + '_',
            **kwargs):
        super().__init__(*args, **kwargs)
        self._word_regex1 = re.compile(
            '([%s]+)' % '|'.join(re.escape(ch) for ch in word_chars))
        self._word_regex2 = re.compile(
            '([^%s]+)' % '|'.join(re.escape(ch) for ch in word_chars))

    def set_edit_pos(self, pos):
        super().set_edit_pos(_clamp(pos, 0, len(self._edit_text)))

    def set_edit_text(self, edit_text):
        super().set_edit_text(edit_text)
        self.set_edit_pos(_clamp(self._edit_pos, 0, len(edit_text)))

    def keypress(self, _size, key):
        keymap = {
            'ctrl f':         self.forward_char,
            'ctrl b':         self.backward_char,
            'right':          self.forward_char,
            'left':           self.backward_char,
            'ctrl a':         self.beginning_of_line,
            'ctrl e':         self.end_of_line,
            'home':           self.beginning_of_line,
            'end':            self.end_of_line,
            'meta f':         self.forward_word,
            'meta b':         self.backward_word,
            'shift right':    self.forward_word,
            'shift left':     self.backward_word,

            'ctrl d':         self.delete_char,
            'ctrl h':         self.backward_delete_char,
            'delete':         self.delete_char,
            'backspace':      self.backward_delete_char,
            'ctrl u':         self.kill_whole_line,
            'ctrl k':         self.kill_line,
            'meta d':         self.kill_word,
            'ctrl w':         self.backward_kill_word,
            'meta backspace': self.backward_kill_word,
            'ctrl t':         self.transpose_chars,
        }
        if key in keymap:
            keymap[key]()
            self._invalidate()
            return None
        elif _is_valid_key(key):
            self._insert_char_at_cusor(key)
            self._invalidate()
            return None
        return key

    def _insert_char_at_cusor(self, key):
        self.set_edit_text(
            self._edit_text[0:self._edit_pos]
            + key
            + self._edit_text[self._edit_pos:])
        self.set_edit_pos(self._edit_pos + 1)

    def backward_char(self):
        if self._edit_pos > 0:
            self.set_edit_pos(self._edit_pos - 1)

    def forward_char(self):
        if self._edit_pos < len(self._edit_text):
            self.set_edit_pos(self._edit_pos + 1)

    def backward_word(self):
        for match in self._word_regex1.finditer(
                self._edit_text[0:self._edit_pos][::-1]):
            self.set_edit_pos(self._edit_pos - match.end(1))
            return
        self.set_edit_pos(0)

    def forward_word(self):
        for match in self._word_regex2.finditer(
                self._edit_text[self._edit_pos:]):
            self.set_edit_pos(self._edit_pos + match.end(1))
            return
        self.set_edit_pos(len(self._edit_text))

    def delete_char(self):
        if self._edit_pos < len(self._edit_text):
            self.set_edit_text(
                self._edit_text[0:self._edit_pos]
                + self._edit_text[self._edit_pos+1:])

    def backward_delete_char(self):
        if self._edit_pos > 0:
            self.set_edit_pos(self._edit_pos - 1)
            self.set_edit_text(
                self._edit_text[0:self._edit_pos]
                + self._edit_text[self._edit_pos+1:])

    def kill_whole_line(self):
        self.set_edit_text('')
        self.set_edit_pos(0)

    def kill_line(self):
        self.set_edit_text(self._edit_text[0:self._edit_pos])

    def backward_kill_word(self):
        pos = self._edit_pos
        self.backward_word()
        self.set_edit_text(
            self._edit_text[0:self._edit_pos] + self._edit_text[pos:])

    def kill_word(self):
        pos = self._edit_pos
        self.forward_word()
        self.set_edit_text(
            self._edit_text[0:pos] + self._edit_text[self._edit_pos:])
        self.set_edit_pos(pos)

    def beginning_of_line(self):
        self.set_edit_pos(0)

    def end_of_line(self):
        self.set_edit_pos(len(self._edit_text))

    def transpose_chars(self):
        self.set_edit_pos(max(2, self._edit_pos + 1))
        if len(self._edit_text) >= 2:
            self.set_edit_text(
                self._edit_text[0:self._edit_pos - 2]
                + self._edit_text[self._edit_pos - 1]
                + self._edit_text[self._edit_pos - 2]
                + self._edit_text[self._edit_pos:])
