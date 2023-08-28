from krita import DockWidgetFactory, DockWidgetFactoryBase, Krita

from .defaults import (
    TAB_ARTIPAINTER,
    TAB_ARTIPAINTER_VIEWER
)
from .docker import create_docker
from .extension import ArtiPainterExtension
from .pages import (
    ArtiPainterPage,
    ArtiPainter_Viewer
)
from .script import script
from .utils import reset_docker_layout


instance = Krita.instance()
instance.addExtension(ArtiPainterExtension(instance))

instance.addDockWidgetFactory(
    DockWidgetFactory(
        TAB_ARTIPAINTER,
        DockWidgetFactoryBase.DockLeft,
        create_docker(ArtiPainterPage),
    )
)

instance.addDockWidgetFactory(
    DockWidgetFactory(
        TAB_ARTIPAINTER_VIEWER,
        DockWidgetFactoryBase.DockLeft,
        create_docker(ArtiPainter_Viewer),
    )
)

# dumb workaround to ensure its only created once
if script.cfg("first_setup", bool):
    instance.notifier().windowCreated.connect(reset_docker_layout)
    script.cfg.set("first_setup", False)
