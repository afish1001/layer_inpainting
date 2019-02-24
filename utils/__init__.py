import os
import utils.inpaint as inpaint

__all__ = ['inpaint', 'mat', 'phase']

from . import phase
from . import mat
from . import inpaint
from . import image


def get_filename(path):
    return os.path.basename(path).split('.')[0]
