from krita import QPlainTextEdit, QSizePolicy, QVBoxLayout,QSplitter,Qt,QWidget
from ..config import Config


class QPromptEdit(QPlainTextEdit):
    def __init__(self, placeholder="Enter prompt...", *args, **kwargs):
        super(QPromptEdit, self).__init__(*args, **kwargs)
        self.setPlaceholderText(placeholder)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



class QPromptLayout(QVBoxLayout):
    prompt_label: str = "Prompt:"
    neg_prompt_label: str = "Negative prompt:"

    def __init__(
        self, cfg: Config, prompt_cfg: str, neg_prompt_cfg: str, *args, **kwargs
    ):
        """Layout for prompt and negative prompt.

        Args:
            cfg (Config): Config to connect to.
            prompt_cfg (str): Config key to read/write prompt to.
            neg_prompt_cfg (str): Config key to read/write negative prompt to.
        """
        super(QPromptLayout, self).__init__(*args, **kwargs)
        # Used to connect to config stored in script
        self.cfg = cfg
        self.prompt_cfg = prompt_cfg
        self.neg_prompt_cfg = neg_prompt_cfg

        self.qedit_prompt = QPromptEdit(placeholder=self.prompt_label)
        self.qedit_neg_prompt = QPromptEdit(placeholder=self.neg_prompt_label)
        
        self.qedit_prompt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.qedit_neg_prompt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.addWidget(self.qedit_prompt,stretch=3)
        self.addWidget(self.qedit_neg_prompt,stretch=1)        

    def cfg_init(self):
        # NOTE: update timer -> cfg_init, setText seems to reset cursor position so we prevent it
        prompt = self.cfg(self.prompt_cfg, str)
        neg_prompt = self.cfg(self.neg_prompt_cfg, str)
        if self.qedit_prompt.toPlainText() != prompt:
            self.qedit_prompt.setPlainText(prompt)
        if self.qedit_neg_prompt.toPlainText() != neg_prompt:
            self.qedit_neg_prompt.setPlainText(neg_prompt)

    def cfg_connect(self):
        self.qedit_prompt.textChanged.connect(
            lambda: self.cfg.set(self.prompt_cfg, self.qedit_prompt.toPlainText())
        )
        self.qedit_neg_prompt.textChanged.connect(
            lambda: self.cfg.set(
                self.neg_prompt_cfg, self.qedit_neg_prompt.toPlainText()
            )
        )
