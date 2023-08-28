from krita import Krita,Qt,QObject,QThread, Qt,QImage, QColor,Selection
from .utils import img_to_ba, img_to_b64, b64_to_img
from .layermanager import get_artipainter_layer,get_artipainter_layerGroup

import os
import sys
plugin_dir = os.path.dirname(os.path.abspath(__file__))
requests_dir = os.path.join(plugin_dir, 'requests')
sys.path.append(requests_dir)
import requests
import hashlib

class artipainter_Loop(QObject):
    selection: Selection
    def __init__(self,script):
        self.script=script
        self.API_URL=self.script.cfg("base_url",str)
        self.if_loop=False
        self.application=Krita.instance()            
        self.currentDoc = self.application.activeDocument()
        self.currentLayer = self.currentDoc.activeNode()

        self.input_layerGroup=get_artipainter_layerGroup(self.currentDoc,"↓ InPut","new layer")
        #self.mask_layerGroup=get_artipainter_layerGroup(self.currentDoc,"Mask_LayerGroup","Mask_layer")
        self.artipainter_OutPut_layer=get_artipainter_layer(self.currentDoc,"↑ OutPut")        

        self.script.x = 0
        self.script.y = 0
        self.script.width = self.currentDoc.width()
        self.script.height = self.currentDoc.height()
        self.script.selection = None

        self.previous_checksum = None
        self.previous_confighash = None

        self.selection = self.currentDoc.selection()
        if self.selection is not None:
            self.selection_height = self.selection.height()
            self.selection_width = self.selection.width()
            self.selection_x = self.selection.x()
            self.selection_y = self.selection.y() 

        super(artipainter_Loop,self).__init__()

    def get_checksum(self, img):
        # Get the raw data from the QImage and compute its SHA-256 hash
        img_data = img.bits()
        img_data.setsize(img.byteCount())
        return hashlib.sha256(img_data).hexdigest()

    def calculate_dict_hash(self,data):
        data_str = str(data).encode('utf-8')
        return hashlib.sha256(data_str).hexdigest()    

    def get_inputLayer_Qimage(self):
        layer_group_data=self.input_layerGroup.projectionPixelData(self.script.x,self.script.y,self.script.width,self.script.height)
        img=QImage(
            layer_group_data,
            self.script.width,
            self.script.height,
            QImage.Format_RGBA8888,
        ).rgbSwapped()
        return img
    
    def get_selection_Qimage(self):
        layer_group_data=self.input_layerGroup.projectionPixelData(self.selection_x,self.selection_y,self.selection_width,self.selection_height)
        img=QImage(
            layer_group_data,
            self.selection_width,
            self.selection_height,
            QImage.Format_RGBA8888,
        ).rgbSwapped()
        return img
        
    def get_maskLayer_Qimage(self):
        mask_data=self.mask_layerGroup.projectionPixelData(self.script.x,self.script.y,self.script.width,self.script.height)
        mask=QImage(
            mask_data,
            self.script.width,
            self.script.height,
            QImage.Format_RGBA8888,
        ).rgbSwapped()
        return mask
    
    def call_api(self, src_ba):
        url = self.API_URL
        payload = self.script.update_params(src_ba)
        if payload["prompt"] == None:
            payload["prompt"]="0"
        response = requests.post(url=f"{url}/sdapi/v1/img2img", json=payload)
        return response.json()
    
    def call_api_on_selection(self, src_ba):
        url = self.API_URL
        payload = self.script.update_params(src_ba)
        payload['width']=self.selection_width
        payload['height']=self.selection_height
        if payload["prompt"] == None:
            payload["prompt"]="0"
        response = requests.post(url=f"{url}/sdapi/v1/img2img", json=payload)
        return response.json()
        
    def maskalpha2Qimgae(self,mask):
        mask_rgba = QImage(self.script.width,self.script.height, QImage.Format_RGBA8888)
        for y in range(self.script.height):
            for x in range(self.script.width):
                #not sure why there's an error when the mask receives a value of 0, so I added a condition here. 
                # If it's 0, I set it to 1. However, this approach causes the mask values to be out of the 0-255 range
                gray_value =max(1,255-mask.pixelColor(x,y).alpha())
                color = QColor(gray_value, gray_value, gray_value)
                mask_rgba.setPixelColor(x, y, color)
        return mask_rgba
       
    def apply_artipainter(self):
        img=self.get_inputLayer_Qimage()

        current_checksum = self.get_checksum(img)
        cfg=self.script.get_config()
        current_confighash =self.calculate_dict_hash(cfg)
        if current_checksum == self.previous_checksum and current_confighash == self.previous_confighash:
            # The image hasn't changed since the last iteration, so we can skip processing it
            return
        self.previous_checksum = current_checksum
        self.previous_confighash = current_confighash

        src_ba=img_to_b64(img)

        #mask=self.get_maskLayer_Qimage()
        #mask_rgba=self.maskalpha2Qimgae(mask)
        #src_mask_ba=img_to_b64(mask_rgba)
         
        r=self.call_api(src_ba)
        img=b64_to_img(r["images"][0].split(",",1)[0])
        img=img.scaled(self.script.width,self.script.height,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.script.artipainter_update.emit(img)
        output_ba = img_to_ba(img)
        self.artipainter_OutPut_layer.setPixelData(output_ba,0,0,self.script.width,self.script.height) 
        self.currentDoc.refreshProjection()

    def apply_artipainter_on_selection(self):
        img=self.get_selection_Qimage()

        current_checksum = self.get_checksum(img)
        cfg=self.script.get_config()
        current_confighash =self.calculate_dict_hash(cfg)
        if current_checksum == self.previous_checksum and current_confighash == self.previous_confighash:
            return
        self.previous_checksum = current_checksum
        self.previous_confighash = current_confighash

        src_ba=img_to_b64(img)
        r=self.call_api_on_selection(src_ba)
        img=b64_to_img(r["images"][0].split(",",1)[0])
        #Sometimes the returned image is inconsistent with the size and input parameters？？why？？？
        self.script.artipainter_update.emit(img)
        img=img.scaled(self.selection_width,self.selection_height,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        output_ba = img_to_ba(img)
        self.artipainter_OutPut_layer.setPixelData(output_ba,self.selection_x,self.selection_y,self.selection_width,self.selection_height) 
        self.currentDoc.refreshProjection()
    
    def apply_artipainter_loop(self):
        if self.selection is None:
            while self.if_loop:
                    self.apply_artipainter()
            self.script.btn_state_update.artipainter_stop_call()
        else :
            while self.if_loop:
                    self.apply_artipainter_on_selection()
            self.script.btn_state_update.artipainter_stop_call()
                   

class ArtiPainter():
    def __init__(self, script):
        self.script = script
        self.artipainter_loop_thread = QThread()
        self.artipainter_loop = artipainter_Loop(self.script)
        self.artipainter_loop.moveToThread(self.artipainter_loop_thread)
        self.artipainter_loop_thread.started.connect(self.artipainter_loop.apply_artipainter_loop)
        
    def post_artipainter_loop(self):
        self.artipainter_loop.if_loop=not self.artipainter_loop.if_loop
        if self.artipainter_loop.if_loop:
            self.artipainter_loop_thread.start()

        else:
            self.artipainter_loop.if_loop = False
            self.artipainter_loop_thread.quit()     