import urwid
import urwid_readline


def show_or_exit(key):
    if key in ('ctrl q', 'ctrl Q'):
        raise urwid.ExitMainLoop()
    txt.set_edit_text('unknown key: ' + repr(key))
    txt.set_edit_pos(len(txt.edit_text))


def compl(text, state):
    cmd = ('start', 'stop', 'next')
    tmp = [c for c in cmd if c and c.startswith(text)] if text else cmd
    try:
        return tmp[state]
    except IndexError:
        return None


txt = urwid_readline.ReadlineEdit()
txt.enable_autocomplete(compl)
fill = urwid.Filler(txt, 'top')
loop = urwid.MainLoop(fill, unhandled_input=show_or_exit)
loop.run()
