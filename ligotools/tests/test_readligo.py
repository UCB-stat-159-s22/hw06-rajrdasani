from ligotools import readligo as rl
from ligotools import loaddata, dq_channel_to_seglist, read_hdf5
import numpy as np

def test_FileList_searchdir():
	hdf5_files = rl.FileList().searchdir('ligotools/')
	assert np.array_equal(hdf5_files, [])

def test_loadfile():
	assert len(rl.loaddata('data/H-H1_LOSC_4_V2-1126259446-32.hdf5','H1')[2]) == 13
    

def test_read_h1():
	strain_H1, time_H1, chan_dict_H1 = rl.loaddata("data/H-H1_LOSC_4_V2-1126259446-32.hdf5", 'H1')
	assert (len(strain_H1) == 131072) & (len(time_H1) == 131072) & (len(chan_dict_H1) == 13)

def test_dq_channel_to_seglist():
	c = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
	assert np.array_equal(rl.dq_channel_to_seglist(c),[slice(0, 131072, None)])



