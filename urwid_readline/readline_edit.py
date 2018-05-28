import re
import string
import urwid


def _is_valid_key(char):
    return (
        urwid.util.is_wide_char(char, 0)
        or (len(char) == 1 and ord(char) >= 32)
    )


class AutocompleteState:
    def __init__(self, prefix, infix, suffix):
        self.prefix = prefix
        self.infix = infix
        self.suffix = suffix
        self.num = 0


class ReadlineEdit(urwid.Edit):
    ignore_focus = False

    def __init__(
            self,
            *args,
            word_chars=string.ascii_letters + string.digits + '_',
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._word_regex1 = re.compile(
            '([%s]+)' % '|'.join(re.escape(ch) for ch in word_chars)
        )
        self._word_regex2 = re.compile(
            '([^%s]+)' % '|'.join(re.escape(ch) for ch in word_chars)
        )
        self._autocomplete_state = None
        self._autocomplete_func = None
        self._autocomplete_delims = ' \t\n;'
        self.size = (30,)  # SET MAXCOL DEFAULT VALUE

    def keypress(self, _size, key):
        self.size = _size
        if key == 'tab' and self._autocomplete_func:
            self._complete()
            return None
        else:
            self._autocomplete_state = None

        keymap = {
            'ctrl f':         self.forward_char,
            'ctrl b':         self.backward_char,
            'up':             self.previous_line,
            'ctrl p':         self.previous_line,
            'ctrl n':         self.next_line,
            'down':           self.next_line,
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
            'ctrl u':         self.backward_kill_line,
            'ctrl k':         self.forward_kill_line,
            'meta d':         self.kill_word,
            'ctrl w':         self.backward_kill_word,
            'meta backspace': self.backward_kill_word,
            'ctrl t':         self.transpose_chars,
            'enter':          self.insert_new_line,
            'ctrl l':         self.clear_screen,
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
            + self._edit_text[self._edit_pos:]
        )
        self.set_edit_pos(self._edit_pos + 1)

    def clear_screen(self):
        self.set_edit_pos(0)
        self.set_edit_text('')

    def previous_line(self):
        x, y = self.get_cursor_coords(self.size)
        self.move_cursor_to_coords(self.size, x, max(0, y - 1))

    def next_line(self):
        x, y = self.get_cursor_coords(self.size)
        self.move_cursor_to_coords(self.size, x, y + 1)

    def backward_char(self):
        if self._edit_pos > 0:
            self.set_edit_pos(self._edit_pos - 1)

    def forward_char(self):
        if self._edit_pos < len(self._edit_text):
            self.set_edit_pos(self._edit_pos + 1)

    def backward_word(self):
        for match in self._word_regex1.finditer(
                self._edit_text[0:self._edit_pos][::-1]
        ):
            self.set_edit_pos(self._edit_pos - match.end(1))
            return
        self.set_edit_pos(0)

    def forward_word(self):
        for match in self._word_regex2.finditer(
                self._edit_text[self._edit_pos:]
        ):
            self.set_edit_pos(self._edit_pos + match.end(1))
            return
        self.set_edit_pos(len(self._edit_text))

    def delete_char(self):
        if self._edit_pos < len(self._edit_text):
            self.set_edit_text(
                self._edit_text[0:self._edit_pos]
                + self._edit_text[self._edit_pos+1:]
            )

    def backward_delete_char(self):
        if self._edit_pos > 0:
            self.set_edit_pos(self._edit_pos - 1)
            self.set_edit_text(
                self._edit_text[0:self._edit_pos]
                + self._edit_text[self._edit_pos+1:]
            )

    def backward_kill_line(self):
        for pos in reversed(range(0, self.edit_pos)):
            if self.edit_text[pos] == '\n':
                self.set_edit_text(
                    self._edit_text[:pos + 1]
                    + self._edit_text[self.edit_pos:]
                )
                self.edit_pos = pos + 1
                return
        self.set_edit_text(self._edit_text[self.edit_pos:])
        self.edit_pos = 0

    def forward_kill_line(self):
        for pos in range(self.edit_pos, len(self.edit_text)):
            if self.edit_text[pos] == '\n':
                self.set_edit_text(
                    self._edit_text[:self.edit_pos]
                    + self._edit_text[pos:]
                )
                return
        self.set_edit_text(self._edit_text[:self.edit_pos])

    def kill_whole_line(self):
        self.backward_kill_line()
        self.forward_kill_line()

    def backward_kill_word(self):
        pos = self._edit_pos
        self.backward_word()
        self.set_edit_text(
            self._edit_text[0:self._edit_pos]
            + self._edit_text[pos:]
        )

    def kill_word(self):
        pos = self._edit_pos
        self.forward_word()
        self.set_edit_text(
            self._edit_text[0:pos]
            + self._edit_text[self._edit_pos:]
        )
        self.set_edit_pos(pos)

    def beginning_of_line(self):
        x, y = self.get_cursor_coords(self.size)
        if x == 0 and y > 0:
            y -= 1
        self.move_cursor_to_coords(self.size, 0, y)

    def end_of_line(self):
        text_length = len(self.edit_text)
        # Move one character forward if at the end of a line.
        if self.edit_pos < text_length and \
                self.edit_text[self.edit_pos] == '\n':
            self.forward_char()
        # Set the position of cursor at the next '\n'.
        for pos in range(self.edit_pos, text_length + 1):
            if pos == text_length:
                self.set_edit_pos(pos)
                return
            elif self.edit_text[pos] == '\n':
                self.set_edit_pos(pos)
                return

    def transpose_chars(self):
        x, y = self.get_cursor_coords(self.size)
        x = max(2, x + 1)
        self.move_cursor_to_coords(self.size, x, y)
        x, y = self.get_cursor_coords(self.size)
        if x == 1:
            # Don't transpose in case of single character
            return
        self.set_edit_text(
            self._edit_text[0:self._edit_pos - 2]
            + self._edit_text[self._edit_pos - 1]
            + self._edit_text[self._edit_pos - 2]
            + self._edit_text[self._edit_pos:]
        )

    def insert_new_line(self):
        if self.multiline:
            self.insert_text('\n')

    def enable_autocomplete(self, func):
        self._autocomplete_func = func
        self._autocomplete_state = None

    def set_completer_delims(self, delimiters):
        self._autocomplete_delims = delimiters

    def _complete(self):
        if self._autocomplete_state:
            self._autocomplete_state.num += 1
        else:
            text_before_caret = self.edit_text[0:self.edit_pos]
            text_after_caret = self.edit_text[self.edit_pos:]

            group = re.escape(self._autocomplete_delims)
            match = re.match(
                '^(?P<prefix>.*[' + group + '])(?P<infix>.*?)$',
                text_before_caret
            )
            if match:
                prefix = match.group('prefix')
                infix = match.group('infix')
            else:
                prefix = ''
                infix = text_before_caret
            suffix = text_after_caret

            self._autocomplete_state = AutocompleteState(prefix, infix, suffix)

        state = self._autocomplete_state

        match = self._autocomplete_func(state.infix, state.num)
        if not match:
            match = state.infix
            self._autocomplete_state = None

        self.edit_text = state.prefix + match + state.suffix
        self.edit_pos = len(state.prefix) + len(match)
