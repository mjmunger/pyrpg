#!/usr/bin/env python3

import sys
from prpg import rpg

r = rpg.Rpg(sys.argv)
r.render_password()
