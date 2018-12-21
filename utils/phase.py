import numpy as np


def get_surface_area(phase_mat):
    pass


def get_volume(phase_mat):
    """

    :param phase_mat:
    :return:
    """
    return np.count_nonzero(phase_mat == 255)
