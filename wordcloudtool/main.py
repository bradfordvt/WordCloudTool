#!/usr/bin/env python
"""
Start up the Word Cloud Parser tool
"""
import sys
import optparse
from wordcloudtool.WordCloudApplication import WordCloudApplication


default_guis = {
    'qt5': 'wordcloudtool.Qt5GUIFactory.Qt5GUIFactory',
    'tk': 'wordcloudtool.TkGUIFactory.TkGUIFactory',
}


def main(args=None):
    gui=None
    try:
        from PyQt5 import QtCore
        gui="qt5"
    except:
        try:
            import tkinter
            gui="Tk"
        except:
            raise AssertionError('No graphical package is detected!')

    if args is None:
        args = sys.argv[1:]
    #from pkg_resources import get_distribution
    #version = get_distribution('wordcloudtool').version
    #parser = optparse.OptionParser(usage=__doc__.strip(), version=version)
    parser = optparse.OptionParser(usage=__doc__.strip())
    parser.add_option(
        "--gui", help="GUI platform to use to display the tool: {0}.".format(
            ", ".join(sorted(default_guis.keys()))))
    opts, args = parser.parse_args(args)

    if opts.gui:
        module = default_guis.get(opts.gui, opts.gui)
        if '.' not in module:
            parser.error("The gui factory is not a full python path")
        module, name = module.rsplit('.', 1)
        imp = __import__(module, {}, [], [name])
        gui_factory = getattr(imp, name)
    elif gui is not None:
        module = default_guis.get(gui, gui)
        if '.' not in module:
            parser.error("The gui factory is not a full python path")
        module, name = module.rsplit('.', 1)
        imp = __import__(module, {}, [], [name])
        gui_factory = getattr(imp, name)
    else:
        gui_factory = None

    app = WordCloudApplication()
    app.make_gui(gui_factory=gui_factory)


if __name__ == "__main__":
    main()