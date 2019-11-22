""" Set eye color of first.

    Copyright (C) 2019 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

from hucon import Eye

eye = None


print('Set the color for the top left eye.')
eye = Eye(1, Eye.RGB)
eye.set_color(255, 0, 0)
