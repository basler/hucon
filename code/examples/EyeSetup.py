""" Set eye color of all.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
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
