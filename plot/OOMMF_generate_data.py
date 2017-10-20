from __future__ import print_function
import numpy as np
# import os
from os import listdir
import re
# import gc
# import sys
import pandas as pd
import argparse

# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate data from OMF files')

parser.add_argument('--initial_state',
                    help='Path to the OMF file with the initial state',
                    default='InitialMagnetization.omf')

parser.add_argument('--omfs_path',
                    help='Path to the folder with the OMF files',
                    default='omfs/')

parser.add_argument('--out_name',
                    help='Append this name to the data_mi file name',
                    default='')

parser.add_argument('--Ms',
                    help='Saturation magnetisation value',
                    type=float, default=1.15e6)

# Parser arguments
args = parser.parse_args()

# -----------------------------------------------------------------------------

mu0 = 4 * np.pi * 1e-7
Ms = args.Ms


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

print('Processing {} files'.format(len(file_list)))

coordinates = pd.read_csv(basedir + file_list[0], comment='#',
                          header=None, delim_whitespace=True)
coordinates = coordinates.as_matrix()[:, :3]

nx = len(np.unique(coordinates[:, 0]))
ny = len(np.unique(coordinates[:, 1]))

mask = coordinates[:, 1] == coordinates[:, 1][nx * int(ny * 0.5)]
data_mx = np.zeros((len(file_list), len(mask[mask])))
data_my = np.zeros((len(file_list), len(mask[mask])))
data_mz = np.zeros((len(file_list), len(mask[mask])))

# Static data -----------------------------------------------------------------

data_mx0 = np.zeros((len(file_list), len(mask[mask])))
data_my0 = np.zeros((len(file_list), len(mask[mask])))
data_mz0 = np.zeros((len(file_list), len(mask[mask])))

m = pd.read_csv(args.initial_state, comment='#',
                header=None, delim_whitespace=True)

data_mx0 = m.as_matrix()[:, 3][mask] / Ms
data_my0 = m.as_matrix()[:, 4][mask] / Ms
data_mz0 = m.as_matrix()[:, 5][mask] / Ms

# -----------------------------------------------------------------------------

# if os.path.exists('datafile.dat'):
#     os.remove('datafile.dat')

for i, _file in enumerate(file_list):
    print(i)

    m = pd.read_csv(basedir + _file, comment='#',
                    header=None, delim_whitespace=True)
    m = m.as_matrix()
    data_mx[i] = m[:, 3][mask] / Ms - data_mx0
    data_my[i] = m[:, 4][mask] / Ms - data_my0
    data_mz[i] = m[:, 5][mask] / Ms - data_mz0

# -----------------------------------------------------------------------------

if args.out_name:
    out_name = '_' + args.out_name
else:
    out_name = ''

np.savetxt('datafile_mx{}.dat'.format(out_name), data_mx)
np.savetxt('datafile_my{}.dat'.format(out_name), data_my)
np.savetxt('datafile_mz{}.dat'.format(out_name), data_mz)
