urwid_readline
----

Text input widget for [urwid](https://github.com/urwid/urwid) that supports
readline shortcuts.

### Installation

`pip install urwid-readline`

Example how to use the program can be found in the
[examples](https://github.com/rr-/urwid_readline/blob/master/example/)
directory.

### Features

Supported operations:

| Command                                               | Key Combination                               |
| ----------------------------------------------------- | --------------------------------------------- |
| Jump to the Beginning of line                         | <kbd>Ctrl</kbd> + <kbd>A</kbd>                |
| Jump backward one character                           | <kbd>Ctrl</kbd> + <kbd>B</kbd> / <kbd>←</kbd> |
| Jump backward one word                                | <kbd>Meta</kbd> + <kbd>B</kbd>                |
| Delete one character                                  | <kbd>Ctrl</kbd> + <kbd>D</kbd>                |
| Delete one word                                       | <kbd>Meta</kbd> + <kbd>D</kbd>                |
| Jump to the end of line                               | <kbd>Ctrl</kbd> + <kbd>E</kbd>                |
| Jump forward one character                            | <kbd>Ctrl</kbd> + <kbd>F</kbd> / <kbd>→</kbd> |
| Jump forward one word                                 | <kbd>Meta</kbd> + <kbd>F</kbd>                |
| Delete previous character                             | <kbd>Ctrl</kbd> + <kbd>H</kbd>                |
| Transpose characters                                  | <kbd>Ctrl</kbd> + <kbd>T</kbd>                |
| Kill (cut) forwards to the end of the line            | <kbd>Ctrl</kbd> + <kbd>K</kbd>                |
| Kill (cut) backwards to the start of the line         | <kbd>Ctrl</kbd> + <kbd>U</kbd>                |
| Kill (cut) forwards to the end of the current word    | <kbd>Meta</kbd> + <kbd>D</kbd>                |
| Kill (cut) backwards to the start of the current word | <kbd>Ctrl</kbd> + <kbd>W</kbd>                |
| Paste last kill                                       | <kbd>Ctrl</kbd> + <kbd>Y</kbd>                |
| Undo last action                                      | <kbd>Ctrl</kbd> + <kbd>_</kbd>                |
| Jump to previous line                                 | <kbd>Ctrl</kbd> + <kbd>P</kbd> / <kbd>↑</kbd> |
| Jump to next line                                     | <kbd>Ctrl</kbd> + <kbd>N</kbd> / <kbd>↓</kbd> |
| Clear screen                                          | <kbd>Ctrl</kbd> + <kbd>L</kbd>                |
| Autocomplete                                          | See examples                                  |
