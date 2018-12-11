""" 2018-12-11

Set the color on the first eye.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

from hucon import Eye

eye = None


print('Set the color for the top left eye.')
eye = Eye(1, Eye.RGB)
eye.set_color(255, 0, 0)
