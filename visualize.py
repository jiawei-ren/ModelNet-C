import os
import h5py
import mathutils
import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cmx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
with open(os.path.join(DATA_DIR, 'modelnet40_ply_hdf5_2048', 'shape_names.txt')) as f:
    CLASS_NAME = f.read().splitlines()


def read_pcd(corruption_type, level):
    """ read XYZ point cloud from filename PLY file """
    if corruption_type == 'clean':
        f = h5py.File(os.path.join(DATA_DIR, 'modelnet_c', corruption_type + '.h5'))
    else:
        f = h5py.File(os.path.join(DATA_DIR, 'modelnet_c', corruption_type + '_{}.h5'.format(level)))
    data = f['data'][:].astype('float32')
    label = f['label'][:].astype('int64')
    f.close()
    return data, label


def pyplot_draw_point_cloud(points, corruption, fig, i):
    rot1 = mathutils.Euler([-math.pi / 2, 0, 0]).to_matrix().to_3x3()
    rot2 = mathutils.Euler([0, 0, math.pi]).to_matrix().to_3x3()
    points = np.dot(points, rot1)
    points = np.dot(points, rot2)
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    colorsMap = 'winter'
    cs = y
    cm = plt.get_cmap(colorsMap)
    cNorm = matplotlib.colors.Normalize(vmin=-1, vmax=1)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    ax = fig.add_subplot(7, 6, i + 1, projection='3d')
    ax.scatter(x, y, z, c=scalarMap.to_rgba(cs))
    scalarMap.set_array(cs)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    plt.axis('off')
    plt.title(corruption, fontsize=30)
    plt.tight_layout()


def visualize(sel_idx, class_to_vis):
    print('Visualizing #{} object in class {}'.format(sel_idx, class_to_vis))
    fig = plt.figure(figsize=(35, 40))
    corruptions = [
        'scale',
        'rotate',
        'jitter',
        'dropout_global',
        'dropout_local',
        'add_global',
        'add_local',
    ]
    titles = [
        'Scale',
        'Rotate',
        'Jitter',
        'Drop Global',
        'Drop Local',
        'Add Global',
        'Add Local',
    ]
    for level in range(6):
        for i, corruption_type in enumerate(corruptions):
            if level == 0:
                data, label = read_pcd('clean', level - 1)
            else:
                data, label = read_pcd(corruption_type, level - 1)
            cnt = 0
            for idx, (pcd, cls) in enumerate(zip(data, label)):
                if CLASS_NAME[cls[0]] == class_to_vis:
                    if cnt == sel_idx:
                        if level == 0:
                            pyplot_draw_point_cloud(pcd, 'Clean', fig, 6 * i + level)
                        else:
                            pyplot_draw_point_cloud(pcd, titles[i] + ' {}'.format(level), fig,
                                                    6 * i + level)
                    cnt += 1
    plt.show()


if __name__ == "__main__":
    visualize(sel_idx=78, class_to_vis='chair')
