from krita import Extension, QMainWindow
from .script import script


class ArtiPainterExtension(Extension):
    def __init__(self, instance):
        super().__init__(instance)

        self.instance = instance
        # store original window docker config
        self.dock_opts = None

    def setup(self):
        script.config_updated.connect(lambda: self.update_global())
        self.instance.notifier().windowCreated.connect(lambda: self.update_global())


    def update_global(self):
        window = self.instance.activeWindow()
        if not window:
            return
        qwin = window.qwindow()
        if not self.dock_opts:
            self.dock_opts = qwin.dockOptions()

        # NOTE: This changes the default behaviour of Krita for all dockers!
        if script.cfg("alt_dock_behavior", bool):
            qwin.setDockOptions(
                QMainWindow.AnimatedDocks
                | QMainWindow.AllowTabbedDocks
                | QMainWindow.GroupedDragging
                | QMainWindow.AllowNestedDocks
                # | QMainWindow.VerticalTabs
            )
        else:
            qwin.setDockOptions(self.dock_opts)

    def createActions(self, window):
        artipainter_action = window.createAction(
            "artipainter", "Apply artipainter", "tools/scripts"
        )
        artipainter_action.triggered.connect(lambda: script.action_artipainter())

