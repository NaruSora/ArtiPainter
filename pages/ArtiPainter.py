from krita import QPushButton,pyqtSignal
from ..script import script
from ..widgets import TipsLayout
from .img_base import SDImgPageBase

class ArtiPainterPage(SDImgPageBase):
    name = "ArtiPainter"
    artiPainterBtn = QPushButton("start painting")
    artiPainterBtn_state="start painting"

    def __init__(self, *args, **kwargs):
        super(ArtiPainterPage, self).__init__(cfg_prefix="img2img", *args, **kwargs)
        self.tips = TipsLayout(
            ["call webUI api"]
        )
        self.layout.addLayout(self.denoising_strength_layout)
        self.layout.addWidget(self.artiPainterBtn)
        self.layout.addLayout(self.tips)
        self.layout.addStretch()

    def painting_start(self):
            self.artiPainterBtn_state="stop painting"
            self.artiPainterBtn.setText("stop painting")
    def painting_stop(self):
            self.artiPainterBtn_state="start painting"
            self.artiPainterBtn.setText("start painting")

    def cfg_init(self):
        super(ArtiPainterPage, self).cfg_init()
        self.tips.setVisible(not script.cfg("minimize_ui", bool))

    def cfg_connect(self):
        super(ArtiPainterPage, self).cfg_connect()
        self.artiPainterBtn.released.connect(lambda: script.action_artipainter())