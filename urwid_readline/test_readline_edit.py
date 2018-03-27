import pytest
from urwid_readline import ReadlineEdit


def test_edit_pos_clamp():
    edit = ReadlineEdit(edit_text='asd', edit_pos=0)
    assert edit.edit_pos == 0
    edit.edit_pos = 100
    assert edit.edit_pos == 3
    edit.edit_pos = -1
    assert edit.edit_pos == 0


def test_backward_char():
    edit = ReadlineEdit(edit_text='ab', edit_pos=2)
    edit.backward_char()
    assert edit.edit_pos == 1
    edit.backward_char()
    assert edit.edit_pos == 0
    edit.backward_char()
    assert edit.edit_pos == 0


def test_forward_char():
    edit = ReadlineEdit(edit_text='ab', edit_pos=0)
    edit.forward_char()
    assert edit.edit_pos == 1
    edit.forward_char()
    assert edit.edit_pos == 2
    edit.forward_char()
    assert edit.edit_pos == 2


def test_beginnining_of_line():
    edit = ReadlineEdit(edit_text='ab', edit_pos=2)
    edit.beginning_of_line()
    assert edit.edit_pos == 0


def test_end_of_line():
    edit = ReadlineEdit(edit_text='ab', edit_pos=0)
    edit.end_of_line()
    assert edit.edit_pos == 2


@pytest.mark.parametrize('start_text, start_pos, end_pos', [
    ("'x'", 3, 1),
    ("'x'", 2, 1),
    ("'x'", 1, 0),
    ("'x'", 0, 0),
    ("'x' x", 4, 1),
    ("'x' x", 3, 1),
    ("'x' x", 2, 1),
    ("'x' x", 1, 0),
    ("'x'' x", 5, 1),
    ("'x'' x", 4, 1),
    ("'x'' x", 3, 1),
    ("'x'' x", 2, 1),
    ("'x'' x", 1, 0),
    ("'x'' x'", 6, 5),
    ("'x'' x'", 5, 1),
    ("'x'' x'", 4, 1),
    ("'x'' x'", 3, 1),
    ("'x'' x'", 2, 1),
    ("'x'' x'", 1, 0),
    ("xx'xx x", 7, 6),
    ("xx'xx x", 6, 3),
    ("xx'xx x", 3, 0),
])
def test_backward_word(start_text, start_pos, end_pos):
    edit = ReadlineEdit(edit_text=start_text, edit_pos=start_pos)
    edit.backward_word()
    assert edit.edit_pos == end_pos


@pytest.mark.parametrize('start_text, start_pos, end_pos', [
    ("'x'", 0, 1),
    ("'x'", 1, 3),
    ("'x'", 2, 3),
    ("'x'", 3, 3),
    ("'x' x", 1, 4),
    ("'x' x", 2, 4),
    ("'x' x", 3, 4),
    ("'x' x", 4, 5),
    ("'x'' x", 1, 5),
    ("'x'' x", 2, 5),
    ("'x'' x", 3, 5),
    ("'x'' x", 4, 5),
    ("'x'' x", 5, 6),
    ("'x'' x'", 1, 5),
    ("'x'' x'", 2, 5),
    ("'x'' x'", 3, 5),
    ("'x'' x'", 4, 5),
    ("'x'' x'", 5, 7),
    ("'x'' x'", 6, 7),
    ("xx'xx x", 0, 3),
    ("xx'xx x", 3, 6),
])
def test_forward_word(start_text, start_pos, end_pos):
    edit = ReadlineEdit(edit_text=start_text, edit_pos=start_pos)
    edit.forward_word()
    assert edit.edit_pos == end_pos


@pytest.mark.parametrize('start_text, start_pos, end_text, end_pos', [
    ('abc', 0, 'bc', 0),
    ('abc', 1, 'ac', 1),
    ('abc', 2, 'ab', 2),
    ('abc', 3, 'abc', 3),
])
def test_delete_char(start_text, start_pos, end_text, end_pos):
    edit = ReadlineEdit(edit_text=start_text, edit_pos=start_pos)
    edit.delete_char()
    assert edit.text == end_text
    assert edit.edit_pos == end_pos


@pytest.mark.parametrize('start_text, start_pos, end_text, end_pos', [
    ('abc', 3, 'ab', 2),
    ('abc', 2, 'ac', 1),
    ('abc', 1, 'bc', 0),
    ('abc', 0, 'abc', 0),
])
def test_backward_delete_char(start_text, start_pos, end_text, end_pos):
    edit = ReadlineEdit(edit_text=start_text, edit_pos=start_pos)
    edit.backward_delete_char()
    assert edit.text == end_text
    assert edit.edit_pos == end_pos


def test_kill_whole_line():
    edit = ReadlineEdit(edit_text='ab', edit_pos=1)
    edit.kill_whole_line()
    assert edit.edit_pos == 0
    assert edit.text == ''


def test_kill_line():
    edit = ReadlineEdit(edit_text='ab', edit_pos=1)
    edit.kill_line()
    assert edit.edit_pos == 1
    assert edit.text == 'a'


@pytest.mark.parametrize('start_text, start_pos, end_text, end_pos', [
    ("'x'", 3, "'", 1),
    ("'x'", 2, "''", 1),
    ("'x'", 1, "x'", 0),
    ("'x'", 0, "'x'", 0),
    ("'x' x", 4, "'x", 1),
    ("'x' x", 3, "' x", 1),
    ("'x' x", 2, "'' x", 1),
    ("'x' x", 1, "x' x", 0),
    ("'x'' x", 5, "'x", 1),
    ("'x'' x", 4, "' x", 1),
    ("'x'' x", 3, "'' x", 1),
    ("'x'' x", 2, "''' x", 1),
    ("'x'' x", 1, "x'' x", 0),
    ("'x'' x'", 6, "'x'' '", 5),
    ("'x'' x'", 5, "'x'", 1),
    ("'x'' x'", 4, "' x'", 1),
    ("'x'' x'", 3, "'' x'", 1),
    ("'x'' x'", 2, "''' x'", 1),
    ("'x'' x'", 1, "x'' x'", 0),
    ("xx'xx x", 7, "xx'xx ", 6),
    ("xx'xx x", 6, "xx'x", 3),
    ("xx'xx x", 3, 'xx x', 0),
])
def test_backward_kill_word(start_text, start_pos, end_text, end_pos):
    edit = ReadlineEdit(edit_text=start_text, edit_pos=start_pos)
    edit.backward_kill_word()
    assert edit.text == end_text
    assert edit.edit_pos == end_pos


@pytest.mark.parametrize('start_text, start_pos, end_text, end_pos', [
    ("'x'", 1, "'", 1),
    ("'x'", 2, "'x", 2),
    ("'x'", 3, "'x'", 3),
    ("'x' x", 1, "'x", 1),
    ("'x' x", 2, "'xx", 2),
    ("'x' x", 3, "'x'x", 3),
    ("'x' x", 4, "'x' ", 4),
    ("'x'' x", 1, "'x", 1),
    ("'x'' x", 2, "'xx", 2),
    ("'x'' x", 3, "'x'x", 3),
    ("'x'' x", 4, "'x''x", 4),
    ("'x'' x", 5, "'x'' ", 5),
    ("'x'' x'", 1, "'x'", 1),
    ("'x'' x'", 2, "'xx'", 2),
    ("'x'' x'", 3, "'x'x'", 3),
    ("'x'' x'", 4, "'x''x'", 4),
    ("'x'' x'", 5, "'x'' ", 5),
    ("'x'' x'", 6, "'x'' x", 6),
    ("xx'xx x", 0, 'xx x', 0),
    ("xx'xx x", 3, "xx'x", 3),
])
def test_kill_word(start_text, start_pos, end_text, end_pos):
    edit = ReadlineEdit(edit_text=start_text, edit_pos=start_pos)
    edit.kill_word()
    assert edit.text == end_text
    assert edit.edit_pos == end_pos


@pytest.mark.parametrize('start_text, start_pos, end_text, end_pos', [
    ('a', 0, 'a', 1),
    ('a', 1, 'a', 1),
    ('abc', 0, 'bac', 2),
    ('abc', 1, 'bac', 2),
    ('abc', 2, 'acb', 3),
    ('abc', 3, 'acb', 3),
])
def test_transpose(start_text, start_pos, end_text, end_pos):
    edit = ReadlineEdit(edit_text=start_text, edit_pos=start_pos)
    edit.transpose_chars()
    assert edit.text == end_text
    assert edit.edit_pos == end_pos


@pytest.mark.parametrize('start_text, start_pos, source, positions', [
    (
        '',
        0,
        ['start', 'stop', 'next'],
        [
            ('start', 5),
            ('stop', 4),
            ('next', 4),
            ('', 0),
            ('start', 5),
        ]
    ),

    (
        'non-matching',
        12,
        ['start', 'stop', 'next'],
        [
            ('non-matching', 12),
            ('non-matching', 12),
        ]
    ),

    (
        's',
        1,
        ['start', 'stop', 'next'],
        [
            ('start', 5),
            ('stop', 4),
            ('s', 1),
        ]
    ),

    (
        'trailing',
        0,
        ['start', 'stop', 'next'],
        [
            ('starttrailing', 5),
            ('stoptrailing', 4),
            ('nexttrailing', 4),
            ('trailing', 0),
        ]
    ),

    (
        'trailing trailing',
        0,
        ['start', 'stop', 'next'],
        [
            ('starttrailing trailing', 5),
            ('stoptrailing trailing', 4),
            ('nexttrailing trailing', 4),
            ('trailing trailing', 0),
        ]
    ),

    (
        'strailing trailing',
        1,
        ['start', 'stop', 'next'],
        [
            ('starttrailing trailing', 5),
            ('stoptrailing trailing', 4),
            ('strailing trailing', 1),
        ]
    ),

    (
        'preceding s',
        11,
        ['start', 'stop', 'next'],
        [
            ('preceding start', 15),
            ('preceding stop', 14),
            ('preceding s', 11),
        ]
    ),
])
def test_enable_autocomplete(start_text, start_pos, source, positions):
    def compl(text, state):
        tmp = (
            [c for c in source if c and c.startswith(text)]
            if text
            else source)
        try:
            return tmp[state]
        except IndexError:
            return None

    edit = ReadlineEdit(edit_text=start_text, edit_pos=start_pos)
    edit.enable_autocomplete(compl)
    for position in positions:
        expected_text, expected_pos = position
        edit.keypress(None, 'tab')
        assert edit.edit_text == expected_text
        assert edit.edit_pos == expected_pos


def test_enable_autocomplete_clear_state():
    source = ['start', 'stop', 'next']

    def compl(text, state):
        tmp = (
            [c for c in source if c and c.startswith(text)]
            if text
            else source)
        try:
            return tmp[state]
        except IndexError:
            return None

    edit = ReadlineEdit(edit_text='s', edit_pos=1)
    edit.enable_autocomplete(compl)
    edit.keypress(None, 'tab')
    assert edit.edit_text == 'start'
    assert edit.edit_pos == 5
    edit.keypress(None, 'home')
    edit.keypress(None, 'right')
    assert edit.edit_pos == 1
    edit.keypress(None, 'tab')
    assert edit.edit_text == 'starttart'
    assert edit.edit_pos == 5
