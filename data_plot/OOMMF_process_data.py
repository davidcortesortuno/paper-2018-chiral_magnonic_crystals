from __future__ import print_function

# import spectrum
import numpy as np
import os
from os import listdir
import re
import argparse

# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Process data from OMF files')

parser.add_argument('--omfs_path',
                    help='Path to the folder with the OMF files',
                    default='omfs/')

parser.add_argument('--m_i',
                    help='Magnetisation component: x, y or z',
                    default='x')

parser.add_argument('--out_name',
                    help='Name of the data_mi file name (from the generate '
                    ' data file)',
                    default='')

parser.add_argument('--vminf',
                    help='Factor to scale the minimum value of the spectra',
                    default=1., type=float)

parser.add_argument('--vmaxf',
                    help='Factor to scale the maximum value of the spectra',
                    default=1., type=float)

parser.add_argument('--time_step',
                    help='Simulation time step size',
                    default=0.5e-12, type=float)

parser.add_argument('--window',
                    help='Window function for the Fourier spectra. Options: '
                    'blackman, hanning, hamming, bartlett',
                    default='hanning'
                    )

parser.add_argument('--xlim',
                    help='Optional limits for the x axis',
                    nargs=2, type=float)

parser.add_argument('--ylim',
                    help='Optional limits for the y axis',
                    nargs=2, type=float)

parser.add_argument('--colormap', help='Colormap', default='bone_r')

parser.add_argument('--scale', help='Spectra scale: log10, power2',
                    default='log10')

parser.add_argument('--get_data', help='Specify a file name to save the data',
                    )

parser.add_argument('--plot_file_name',
                    help='Name of the output file. Default value is the '
                    'out_name argument',
                    )

parser.add_argument('--plot_file_format',
                    help='Extension of the output plot. Default: pdf',
                    default='pdf'
                    )

# Parser arguments
args = parser.parse_args()

# -----------------------------------------------------------------------------

if args.out_name:
    out_name = '_' + args.out_name
else:
    out_name = ''

# -----------------------------------------------------------------------------


def key_f(f):
    regex_res = re.search(r'(?<=Magnetization\-)[0-9]+(?=\-)', f).group(0)
    return regex_res

basedir = args.omfs_path
if not basedir.endswith('/'):
    basedir += '/'

file_list = [_file for _file in listdir(basedir)
             if _file.startswith('SWDynamics-Oxs_TimeDriver')]
file_list = sorted(file_list,
                   key=key_f)


mu0 = 4 * np.pi * 1e-7

data = np.loadtxt('datafile_m' + args.m_i + out_name + '.dat')
# Time steps according to the steps in data file
n_time_steps = len(data)

coordinates = np.loadtxt(basedir + file_list[0])[:, :3]
nx = len(np.unique(coordinates[:, 0]))
ny = len(np.unique(coordinates[:, 1]))

times = np.arange(n_time_steps) * args.time_step
x = coordinates[:, 0][:nx] / 1e-9

# Apply windows to get a better Fourier spectrum
# We can use: blackman, hanning, hamming, kaiser(ny, 5.5), bartlett
window = args.window
window_f = getattr(np, window)

times_filter, x_filter = (window_f(len(times)),
                          window_f(len(x))
                          )
# times_filter, x_filter = (spectrum.window_lanczos(len(times)),
#                           spectrum.window_lanczos(len(x))
#                           )

w1, w2 = np.meshgrid(x_filter, times_filter)
window = w1 * w2
data = data * window

# for i in np.arange(data.shape[0]):
#     data[i] = data[i] * x_filter
#
# for i in np.arange(data.shape[1]):
#     data[:, i] = data[:, i] * times_filter

fft_data = abs(np.fft.fftshift(np.fft.fft2(data)))

# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt
plt.style.use(os.path.join(os.path.dirname(__file__),
                           'lato_style.mplstyle')
              )


freqs = np.fft.fftfreq(len(times),
                       d=(times[1] - times[0])) / (1e9)
freqs = np.fft.fftshift(freqs)

k = np.fft.fftfreq(len(x),
                   d=(x[1] - x[0]))
k = np.fft.fftshift(k) * 2 * np.pi

# k = 2 * np.pi / (x - np.mean(x))

f = plt.figure()
ax = f.add_subplot(111)

if args.scale == 'log10':
    fft_data = np.log10(fft_data ** 2)
elif args.scale == 'power2':
    fft_data = fft_data ** 2

if args.get_data:
    np.savetxt(args.get_data, fft_data)

# Modify colorbar to get good plots
cbmax = fft_data.max() / args.vmaxf
cbmin = fft_data.min() / args.vminf
print('Spectra limits: ', cbmin, cbmax)

p = ax.imshow(fft_data,
              vmin=cbmin, vmax=cbmax,
              # cmap='viridis',
              cmap=args.colormap,
              extent=[k[0], k[-1],
                      freqs[0], freqs[-1]],
              aspect='auto',
              interpolation='none'
              )
plt.colorbar(p)

if args.xlim:
    plt.xlim([args.xlim[0], args.xlim[1]])
else:
    plt.xlim([-0.07, 0.07])

if args.ylim:
    plt.ylim([args.ylim[0], args.ylim[1]])

plt.xlabel(r'$k$  [ rad/nm ]')
plt.ylabel(r'$f$  [ GHz ]')

xs = [0, -np.pi / 50, np.pi / 50, -np.pi / 100, np.pi / 100]

if not args.plot_file_name:
    args.plot_file_name = 'spectra' + out_name

plt.savefig(args.plot_file_name + '.' + args.plot_file_format,
            bbox_inches='tight')
# plt.savefig('spectra.jpg')
