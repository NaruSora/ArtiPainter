from krita import QPixmap, QPushButton, QVBoxLayout, QWidget,Qt,QtWidgets,QSizePolicy
from ..script import script
from ..widgets import QLabel


class ArtiPainter_Viewer(QWidget):
    name = "artipainter Viewer"

    def __init__(self, *args, **kwargs):
        super(ArtiPainter_Viewer, self).__init__(*args, **kwargs)
        self.preview = QLabel()
        self.preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setScaledContents(False)

        layout = QVBoxLayout()
        layout.addWidget(self.preview)
        self.setLayout(layout)

    def cfg_init(self):
        pass

    def _update_image(self, Output_Img):
        try:
            pixmap=QPixmap.fromImage(Output_Img)
            scaled_pixmap = pixmap.scaled(self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview.setPixmap(scaled_pixmap)
        except:
            pass

    def cfg_connect(self):
        script.artipainter_update.connect(lambda p: self._update_image(p))