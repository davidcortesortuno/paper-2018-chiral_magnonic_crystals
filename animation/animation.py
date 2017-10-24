
import numpy as np
import os
from os import listdir
import re
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('lato_style.mplstyle')

os.environ['ETS_TOOLKIT'] = 'qt4'
from mayavi import mlab
mlab.options.offscreen = True
import scipy.interpolate


# # Load Data

mu0 = 4 * np.pi * 1e-7
Ms = 0.658e6

base_folder = '../spin_waves_fidimag/OOMMF_periodicDMI_D3e-3_a-w-ratios_Py/omfs_w50/'
static_state = '../spin_waves_fidimag/OOMMF_periodicDMI_D3e-3_a-w-ratios_Py/InitialMagnetisation_w50_ordered.omf'

def key_f(f):
    regex_res = re.search(r'(?<=Magnetization\-)[0-9]+(?=\-)', f).group(0)
    return regex_res

file_list = [_file for _file in listdir(base_folder)
             if _file.startswith('SWDynamics-Oxs_TimeDriver')]
file_list = sorted(file_list, key=key_f)


data0 = pd.read_csv(static_state, comment='#', header=None, delim_whitespace=True)
data0 = data0.as_matrix()

coordinates = data0[:, :3]

nx = len(np.unique(coordinates[:, 0]))
ny = len(np.unique(coordinates[:, 1]))

mask = coordinates[:, 1] == coordinates[:, 1][nx * int(ny * 0.5)]


def plot_i_state(i):
    data = pd.read_csv(os.path.join(base_folder, file_list[i]), comment='#',
                        header=None, delim_whitespace=True)
    data = data.as_matrix()

    data[:, 3:] = (data[:, 3:] - data0[:, 3:]) / Ms

    # mz = data[:, 5].reshape(-1, len(np.unique(data[:, 0]))) / Ms
    
    return data


# Coordinates and grid
x, y = np.unique(coordinates[:, 0]) * 1e9, np.unique(coordinates[:, 1]) * 1e9
X , Y = np.linspace(np.min(x), np.max(x), 3000), np.linspace(np.min(y), np.max(y), 200)
X, Y = np.meshgrid(X, Y)
# x, y = x.T, y.T


# Visualize the points --------------------------------------------------------
data = plot_i_state(0)
mx = scipy.interpolate.griddata((data0[:, 0] * 1e9, data0[:, 1] * 1e9),
                                data[:, 3], (X, Y), method='cubic')

f = mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(1000, 700))
f.scene.off_screen_rendering = True
surf = mlab.surf(X.T, Y.T, mx.T,
                 extent=[0, 3000, 0, 200, -100, 100],
                 colormap='RdYlBu', vmax=0.009, vmin=-0.009,
                 warp_scale=10000
                 )
ms = surf.mlab_source

# From mayavi record:
f.scene.camera.position = [2325.4326884312218, 931.86343668888458, 481.2859227706723]
f.scene.camera.focal_point = [1500.0, 100.0, 0.0]
f.scene.camera.view_angle = 30.0
f.scene.camera.view_up = [-0.27111041026308819, -0.26616607661021852, 0.92501608910813182]
f.scene.camera.clipping_range = [3.9937280454826229, 3993.7280454826227]
text = mlab.text(0.05, 0.86,
                 '{:.3f} ns'.format(0 * 1e-3), width=0.15,
                 line_width=1.,
                 color=(0, 0, 0)
                 )


def plot_mayavi_snap(i):

    data = plot_i_state(i)
    mx = scipy.interpolate.griddata((data0[:, 0] * 1e9, data0[:, 1] * 1e9),
                                    data[:, 3], (X, Y), method='cubic')
    ms.reset(x=X.T, y=Y.T, scalars=mx.T)
    text.text = '{:.3f} ns'.format(i * 1e-3)

    f.scene.save('animation/' + 'snap_{:06}.png'.format(i))

    # mlab.show()
    # mlab.clf()

for i in range(2000):
    plot_mayavi_snap(i)
