# MiniSoccer launcher.
# The game itself is precompiled to minisoccer.mpy (and the grayscale library to
# thumbyGrayscale.mpy) so the Thumby doesn't have to compile 80+ KB of source at
# launch -- that avoids the on-device MemoryError.  This tiny file is all the
# Thumby menu runs.

import gc
import sys

sys.path.insert(0, "/Games/MiniSoccer")
gc.collect()

import minisoccer
minisoccer.main()
