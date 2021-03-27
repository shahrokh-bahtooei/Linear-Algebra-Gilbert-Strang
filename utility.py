from contextlib import contextmanager
import numpy as np


class Styles:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


@contextmanager
def print_style(*styles):
    print(*styles, sep='', end='')
    yield
    print(Styles.END, end='')


def draw_xyz_axes_at_center(mpl_ax):
    # Compute max_lim based on plotted data
    x_lim = abs(max(mpl_ax.get_xlim(), key=abs))
    y_lim = abs(max(mpl_ax.get_ylim(), key=abs))
    z_lim = abs(max(mpl_ax.get_zlim(), key=abs))
    max_lim = max(x_lim, y_lim, z_lim)

    # Position xyz axes to the center
    mpl_ax.set_xlim(xmin=-max_lim, xmax=max_lim)
    mpl_ax.set_ylim(ymin=-max_lim, ymax=max_lim)
    mpl_ax.set_zlim(zmin=-max_lim, zmax=max_lim)

    # Draw xyz axes
    xyz_axes_appearance = dict(color='black', alpha=.5, lw=1, arrow_length_ratio=0.1)
    labels = ['x', 'y', 'z']
    for i in range(3):
        starting_xyz = [0, 0, 0]
        starting_xyz[i] = -max_lim

        ending_xyz = [0, 0, 0]
        ending_xyz[i] = max_lim

        start_to_end_xyz = np.array(ending_xyz) - np.array(starting_xyz)
        mpl_ax.quiver(*starting_xyz, *start_to_end_xyz, **xyz_axes_appearance)

        ending_xyz_with_padding = np.array(ending_xyz) * 1.1
        mpl_ax.text(*ending_xyz_with_padding,
                    labels[i],
                    horizontalalignment='center',
                    verticalalignment='center',
                    alpha=.5)
