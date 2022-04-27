
import ligotools

from ligotools import readligo as rl
from ligotools import loaddata, dq_channel_to_seglist, read_hdf5
import numpy as np

def FileList_searchdir_test():
	hdf5_files = rl.FileList().searchdir('ligotools/')
	assert np.array_equal(hdf5_files, [])

def loadfile_test():
	assert len(rl.loaddata('data/H-H1_LOSC_4_V2-1126259446-32.hdf5','H1')[2]) == 13
    

def read_h1_test():
	strain_H1, time_H1, chan_dict_H1 = rl.loaddata("data/H-H1_LOSC_4_V2-1126259446-32.hdf5", 'H1')
	assert (len(strain_H1) == 131072) & (len(time_H1) == 131072) & (len(chan_dict_H1) == 13)

def dq_channel_to_seglist_test():
	c = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
	assert np.array_equal(rl.dq_channel_to_seglist(c),[slice(0, 131072, None)])



