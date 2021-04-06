from contextlib import contextmanager
import numpy as np
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


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


class Arrow3D(FancyArrowPatch):
    """
    Ref: https://stackoverflow.com/a/22867877/4526384
    """

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


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
    axes = ['x', 'y', 'z']
    for axis in axes:
        start_pt = {a: -max_lim if a == axis else 0 for a in axes}
        end_pt = {a: max_lim if a == axis else 0 for a in axes}

        # Draw axis
        xs = [start_pt['x'], end_pt['x']]
        ys = [start_pt['y'], end_pt['y']]
        zs = [start_pt['z'], end_pt['z']]

        a = Arrow3D(xs, ys, zs, mutation_scale=20, arrowstyle='-|>', lw=1, color='black', alpha=1)
        mpl_ax.add_artist(a)

        # Add label
        end_xyz_with_padding = np.array([end_pt['x'], end_pt['y'], end_pt['z']]) * 1.1

        mpl_ax.text(*end_xyz_with_padding,
                    axis,
                    horizontalalignment='center',
                    verticalalignment='center',
                    color='black',
                    alpha=1)
