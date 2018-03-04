from hackerschool import Eye

eye = None


HSTerm.term_exec('Set the color for the top left eye.')
eye = Eye(1)
eye.set_color(255, 0, 0)
