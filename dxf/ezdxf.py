import dxfgrabber
dxf = dxfgrabber.readfile("Dessin1.dxf")
header_var_count = len(dxf.header) # dict of dxf header vars
layer_count = len(dxf.layers) # collection of layer definitions
block_definition_count = len(dxf.blocks) #  dict like collection of block definitions
entity_count = len(dxf.entities) # list like collection of entities
print(entity_count)