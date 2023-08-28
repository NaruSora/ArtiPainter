from krita import (
    Document,
    Krita,
    Node,
    QObject,
    Selection,
    pyqtSignal,
)

from .config import Config
from .defaults import (
    ETA_REFRESH_INTERVAL,
    EXT_CFG_NAME,
    STATE_RESET_DEFAULT,
)
from .utils import (
    get_ext_args, 
    fix_prompt,
)
from .artipainter import ArtiPainter    

class BtnStateUpdate(QObject):
    artipainter_painting_start=pyqtSignal(object)
    artipainter_painting_stop=pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.artipainter_start_function = None
        self.artipainter_stop_function = None
        self.artipainer_page=None

    def function_bind(self):
        self.artipainter_painting_start.connect(self.artipainter_start_function)
        self.artipainter_painting_stop.connect(self.artipainter_stop_function)

    def artipainter_start_call(self):
        print("start emit")
        self.artipainter_painting_start.emit(self.artipainter_page)
    
    def artipainter_stop_call(self):
        print("stop emit")
        self.artipainter_painting_stop.emit(self.artipainter_page)


class Script(QObject):
    cfg: Config
    """config singleton"""
    status: str
    """Current status (shown in status bar)"""
    app: Krita
    """Krita's Application instance (KDE Application)"""
    doc: Document
    """Currently opened document if any"""
    node: Node
    """Currently selected layer in Krita"""
    selection: Selection
    """Selection region in Krita"""
    width: int
    """Width of canvas"""
    height: int
    """Height of canvas"""
    

    status_changed = pyqtSignal(str)
    config_updated = pyqtSignal()
    progress_update = pyqtSignal(object)

    resolution_rate: float
    artipainter_update=pyqtSignal(object)
    btn_state_update:BtnStateUpdate

    def __init__(self):
        super(Script, self).__init__()
        # Persistent settings (should reload between Krita sessions)
        self.cfg = Config()
        # used for webUI scripts aka extensions not to be confused with their extensions
        self.ext_cfg = Config(name=EXT_CFG_NAME, model=None)
        self.progress_update.connect(lambda p: self.update_status_bar_eta(p))

        self.resolution_rate = 1
        self.artipainter_isrun=False
        self.btn_state_update=BtnStateUpdate()
        
    def update_resolution_rate(self,rate):
        self.resolution_rate=rate
    
    def update_params(self,*args):
        #params = dict(init_images=[args[0]],mask=args[1],mask_blur=0,inpainting_fill=0)
        params = dict(init_images=[args[0]])
        if not self.cfg("just_use_yaml", bool):
            seed = (
                int(self.cfg("img2img_seed", str))  # Qt casts int as 32-bit int
                if (not self.cfg("img2img_seed", str).strip() == "") and 
                (not self.cfg("img2img_seed", str).strip()=="-" )
                else -1
            )

            ext_name = self.cfg("img2img_script", str)
            
            ext_args = get_ext_args(self.ext_cfg, "scripts_img2img", ext_name)
            
            params.update(
                prompt=fix_prompt(self.cfg("img2img_prompt", str)),
                negative_prompt=fix_prompt(self.cfg("img2img_negative_prompt", str)),
                sampler_name=self.cfg("img2img_sampler", str),
                steps=self.cfg("img2img_steps", int),
                cfg_scale=self.cfg("img2img_cfg_scale", float),
                denoising_strength=self.cfg("img2img_denoising_strength", float),
                color_correct=self.cfg("img2img_color_correct", bool),
                script=ext_name,
                script_args=ext_args,

                seed=seed,
                
                width=str(self.width*self.resolution_rate),
                height=str(self.height*self.resolution_rate),
            )
        return params
    
    def get_config(self):
        config=dict()
        seed = (
        int(self.cfg("img2img_seed", str))  # Qt casts int as 32-bit int
        if (not self.cfg("img2img_seed", str).strip() == "") and 
        (not self.cfg("img2img_seed", str).strip()=="-" )
        else -1
        )
        config.update(
            prompt=fix_prompt(self.cfg("img2img_prompt", str)),
            negative_prompt=fix_prompt(self.cfg("img2img_negative_prompt", str)),
            sampler_name=self.cfg("img2img_sampler", str),
            steps=self.cfg("img2img_steps", int),
            cfg_scale=self.cfg("img2img_cfg_scale", float),
            denoising_strength=self.cfg("img2img_denoising_strength", float),
            color_correct=self.cfg("img2img_color_correct", bool),
            width=str(self.width*self.resolution_rate),
            height=str(self.height*self.resolution_rate),    
            seed=seed,
        )
        return config

    def restore_defaults(self, if_empty=False):
        """Restore to default config."""
        self.cfg.restore_defaults(not if_empty)
        self.ext_cfg.config.remove("")

        if not if_empty:
            self.status_changed.emit(STATE_RESET_DEFAULT)

    def action_artipainter(self):
        if self.artipainter_isrun==False:
            if self.btn_state_update.artipainter_page.artiPainterBtn_state=="start painting":
                global artipainter
                artipainter=ArtiPainter(self)
                artipainter.post_artipainter_loop()
                self.artipainter_isrun=True
                self.btn_state_update.artipainter_start_call()
            else:
                pass
        else:
            artipainter.post_artipainter_loop()
            self.artipainter_isrun=False
        

script = Script()

