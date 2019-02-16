import urwid

import urwid_readline


def unhandled_input(txt, key):
    if key in ("ctrl q", "ctrl Q"):
        raise urwid.ExitMainLoop()
    txt.set_edit_text("unknown key: " + repr(key))
    txt.set_edit_pos(len(txt.edit_text))


def compl(text, state):
    cmd = ("start", "stop", "next")
    tmp = [c for c in cmd if c and c.startswith(text)] if text else cmd
    try:
        return tmp[state]
    except IndexError:
        return None


def main():
    txt = urwid_readline.ReadlineEdit(multiline=True)
    txt.enable_autocomplete(compl)
    fill = urwid.Filler(txt, "top")
    loop = urwid.MainLoop(
        fill, unhandled_input=lambda key: unhandled_input(txt, key)
    )
    loop.run()


if __name__ == "__main__":
    main()
