def get_layer(krita_doc,name):
    if krita_doc is None:
        return None
    root=krita_doc.rootNode()
    for node in root.childNodes():
        if node.name() == name:
            return node
    
    new_layer=krita_doc.createNode(name, "paintlayer")
    root.addChildNode(new_layer,None)
    return new_layer

def get_artipainter_layer(krita_doc,name):
    if krita_doc is None:
        return None
    root=krita_doc.rootNode()
    for node in root.childNodes():
        if node.name() == name:
            return node
    
    new_layer=krita_doc.createNode(name, "paintlayer")
    root.addChildNode(new_layer,None)
    return new_layer
    
def get_artipainter_layerGroup(*args):
    if len(args) == 2:
        krita_doc = args[0]
        name = args[1]
        if krita_doc is None:
            return None
        root=krita_doc.rootNode()
        for node in root.childNodes():
            if node.type()=="grouplayer" and node.name() == name:
                return node    
        new_layer_group=krita_doc.createNode(name, "grouplayer")
        root.addChildNode(new_layer_group,None)
        return new_layer_group
    elif len(args) == 3:
        krita_doc = args[0]
        name = args[1]
        child_name = args[2]
        root=krita_doc.rootNode()
        for node in root.childNodes():
            if node.type()=="grouplayer" and node.name() == name:
                return node    
        new_layer_group=krita_doc.createNode(name, "grouplayer")
        root.addChildNode(new_layer_group,None)
        new_layer=krita_doc.createNode(child_name, "paintlayer")
        new_layer_group.addChildNode(new_layer,None)
        return new_layer_group
    
def get_artipainter_mask(krita_doc,paintlayer,name):
    if krita_doc is None:
        return None
    for node in paintlayer.childNodes():
        if node.name() == name and node.type() == "transparencymask":
            return node
    # new_mask=krita_doc.createNode(name, "transparencymask")
    # paintlayer.addChildNode(new_mask,None)
    # return new_mask
    return None