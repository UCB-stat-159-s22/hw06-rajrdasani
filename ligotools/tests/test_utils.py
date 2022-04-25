import matplotlib
matplotlib.use('AGG')
## Test utils methods 
import ligotools
import numpy as np
from os.path import exists
from os import remove


import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from ligotools.readligo import loaddata
from scipy.interpolate import interp1d

from ligotools import *

def test_whiten():
	fn_H1 = "data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
	fs = 4096
	NFFT = 4*fs
	strain_H1, time_H1, chan_dict_H1 = loaddata(fn_H1, 'H1')
	Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
	psd_H1 = interp1d(freqs, Pxx_H1)
	dt = time_H1[1] - time_H1[0]
	strain_H1_whiten = whiten(strain_H1,psd_H1,dt)
	assert strain_H1_whiten.shape == strain_H1.shape


def test_write_wavfile():
	data = np.linspace(0,10,100)
	fs = 1 
	write_wavfile("audio/temp.wav", fs, data)
	assert exists("audio/temp.wav")
	remove("audio/temp.wav")

from scipy.signal import butter, filtfilt

def test_reqshift():
	fn_H1 = "data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
	fs = 4096
	NFFT = 4*fs
	strain_H1, time_H1, chan_dict_H1 = loaddata(fn_H1, 'H1')
	Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
	psd_H1 = interp1d(freqs, Pxx_H1)
	dt = time_H1[1] - time_H1[0]
	strain_H1_whiten = whiten(strain_H1,psd_H1,dt)
	fband = [43.0, 300.0]
	# We need to suppress the high frequency noise (no signal!) with some bandpassing:
	bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
	normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
	strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization

	# parameters for frequency shift
	fshift = 400.
	speedup = 1.
	fss = int(float(fs)*float(speedup))
	strain_H1_shifted = reqshift(strain_H1_whitenbp,fshift=fshift,sample_rate=fs)

def test_plot_SNR_around_event():
	# time, timemax, SNR, pcolor, det, eventname, plottype
	time = np.linspace(2,10,100)
	timemax = 2
	SNR = np.cos(time)
	pcolor = 'k'
	det = 'H1'
	eventname = "test_event"
	plottype = 'png' 
	plot_SNR_around_event(time, timemax, SNR, pcolor, det, eventname, plottype, save=False)
	assert plt.gcf().number > 0
