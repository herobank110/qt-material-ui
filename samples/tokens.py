# Color in hue, chroma, tone form
from materialyoucolor.hct import Hct
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors

# There are 9 different variants of scheme.
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from materialyoucolor.scheme.scheme_content import SchemeContent
# Others you can import: SchemeExpressive, SchemeFruitSalad, SchemeMonochrome, SchemeRainbow, SchemeVibrant, SchemeNeutral, SchemeFidelity and SchemeContent

# SchemeTonalSpot is android default
scheme = SchemeTonalSpot( # choose any scheme here
    Hct.from_int(0xff4181EE), # source color in hct form
    False, # dark mode
    0.0, # contrast
)

for color in vars(MaterialDynamicColors).keys():
    color_name = getattr(MaterialDynamicColors, color)
    if hasattr(color_name, "get_hct"): # is a color
        color_hct_value = color_name.get_hct(scheme)
        color_str = "#" + "".join("%02x" %x for x in color_hct_value.to_rgba())
        if color_str.endswith("ff"):
            color_str = color_str[:-2]
        print(f"{color:30}{color_str}")
        # print(color, color_name.get_hct(scheme).to_rgba()) # print name of color and value in rgba format

# background [14, 20, 21, 255]
# onBackground [222, 227, 229, 255]
# surface [14, 20, 21, 255]
# surfaceDim [14, 20, 21, 255]
# ...