urwid_readline
----

Text input widget for [urwid](https://github.com/urwid/urwid) that supports
readline shortcuts.

### Installation

`pip install urwid-readline`

Example how to use the program can be found in the
[examples](https://github.com/rr-/urwid_readline/blob/master/examples/)
directory.

### Features

Supported operations (names consistent with bash):

- `forward-char`
- `backward-char`
- `forward-word`
- `backward-word`
- `delete-char`
- `backward-delete-char`
- `kill-word`
- `backward-kill-word`
- `beginning-of-line`
- `end-of-line`
- `kill-line`
- `kill-whole-line`
- `transpose-chars`
- autocomplete

Notable unsupported operations (let me know if you need these):

- word transposing
- clipboard
- history, undo
