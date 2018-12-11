""" 2018-12-11

Set the color for all eyes.

Author: Sascha.MuellerzumHagen@baslerweb.com
"""

from hucon import Eye

eye_tl = None
eye_tr = None
eye_bl = None
eye_br = None


eye_tl = Eye(1, Eye.RGB)
eye_tr = Eye(2, Eye.RGB)
eye_bl = Eye(3, Eye.RGB)
eye_br = Eye(4, Eye.RGB)
eye_tl.set_color(255, 0, 0)
eye_tr.set_color(0, 255, 0)
eye_bl.set_color(0, 0, 255)
eye_br.set_color(255, 255, 255)
