import os
import glob
import h5py
import numpy as np
from corrupt_utils import corrupt_scale, corrupt_jitter, corrupt_rotate, corrupt_dropout_global, corrupt_dropout_local, \
    corrupt_add_global, corrupt_add_local

NUM_POINTS = 1024
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data')

np.random.seed(0)

corruptions = {
    'clean': None,
    'scale': corrupt_scale,
    'jitter': corrupt_jitter,
    'rotate': corrupt_rotate,
    'dropout_global': corrupt_dropout_global,
    'dropout_local': corrupt_dropout_local,
    'add_global': corrupt_add_global,
    'add_local': corrupt_add_local,
}


subset_list = [0, 2, 5, 6, 8, 10, 10, 17, 18, 20, 26, 10, 30, 32, 33, 37]

def load_data(partition):
    h5_name = "/PATH/TO/oo3d_pcd_1024.hdf5"
    f = h5py.File(h5_name)
    data = f['data']
    data = [pc_normalize(pcd) for pcd in data]
    data = np.array(data).astype('float32')
    label = f['label']
    label = [subset_list[i] for i in label]
    label = np.array(label).astype('int64')
    label = label[:, None]
    f.close()
    return data, label


def pc_normalize(pc):
    centroid = np.mean(pc, axis=0)
    pc = pc - centroid
    m = np.max(np.sqrt(np.sum(pc ** 2, axis=1)))
    pc = pc / m
    return pc


def save_data(all_data, all_label, corruption_type, level):
    if not os.path.exists(os.path.join(DATA_DIR, 'oo3d_c')):
        os.makedirs(os.path.join(DATA_DIR, 'oo3d_c'))
    if corruption_type == 'clean':
        h5_name = os.path.join(DATA_DIR, 'oo3d_c', '{}.h5'.format(corruption_type))
    else:
        h5_name = os.path.join(DATA_DIR, 'oo3d_c', '{}_{}.h5'.format(corruption_type, level))
    f = h5py.File(h5_name, 'w')
    f.create_dataset('data', data=all_data)
    f.create_dataset('label', data=all_label)
    f.close()
    print("{} finished".format(h5_name))


def corrupt_data(all_data, type, level):
    if type == 'clean':
        return all_data
    corrupted_data = []
    for pcd in all_data:
        corrupted_pcd = corruptions[type](pcd, level)
        corrupted_data.append(corrupted_pcd)
    corrupted_data = np.stack(corrupted_data, axis=0)
    return corrupted_data


def main():
    all_data, all_label = load_data('test')
    for corruption_type in corruptions:
        for level in range(5):
            corrupted_data = corrupt_data(all_data, corruption_type, level)
            save_data(corrupted_data, all_label, corruption_type, level)
            if corruption_type == 'clean':
                break


if __name__ == '__main__':
    main()
