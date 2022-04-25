# -- To calculate the PSD of the data, choose an overlap and a window (common to all detectors)
#   that minimizes "spectral leakage" https://en.wikipedia.org/wiki/Spectral_leakage
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import h5py
import json
import matplotlib.mlab as mlab
from utils import *

def pcd_plot(fs, time, template_p, template_c, template_offset, strain_H1, strain_L1, dt, bb, ab, normalization, make_plots, strain_H1_whitenbp,eventname, plottype,tevent, strain_L1_whitenbp):

	NFFT = 4*fs
	psd_window = np.blackman(NFFT)
	# and a 50% overlap:
	NOVL = NFFT/2

	# define the complex template, common to both detectors:
	template = (template_p + template_c*1.j) 
	# We will record the time where the data match the END of the template.
	etime = time+template_offset
	# the length and sampling rate of the template MUST match that of the data.
	datafreq = np.fft.fftfreq(template.size)*fs
	df = np.abs(datafreq[1] - datafreq[0])

	# to remove effects at the beginning and end of the data stretch, window the data
	# https://en.wikipedia.org/wiki/Window_function#Tukey_window
	try:   dwindow = signal.tukey(template.size, alpha=1./8)  # Tukey window preferred, but requires recent scipy version 
	except: dwindow = signal.blackman(template.size)          # Blackman window OK if Tukey is not available

	# prepare the template fft.
	template_fft = np.fft.fft(template*dwindow) / fs

	# loop over the detectors
	dets = ['H1', 'L1']
	for det in dets:

		if det is 'L1': data = strain_L1.copy()
		else:           data = strain_H1.copy()

		# -- Calculate the PSD of the data.  Also use an overlap, and window:
		data_psd, freqs = mlab.psd(data, Fs = fs, NFFT = NFFT, window=psd_window, noverlap=NOVL)

		# Take the Fourier Transform (FFT) of the data and the template (with dwindow)
		data_fft = np.fft.fft(data*dwindow) / fs

		# -- Interpolate to get the PSD values at the needed frequencies
		power_vec = np.interp(np.abs(datafreq), freqs, data_psd)

		# -- Calculate the matched filter output in the time domain:
		# Multiply the Fourier Space template and data, and divide by the noise power in each frequency bin.
		# Taking the Inverse Fourier Transform (IFFT) of the filter output puts it back in the time domain,
		# so the result will be plotted as a function of time off-set between the template and the data:
		optimal = data_fft * template_fft.conjugate() / power_vec
		optimal_time = 2*np.fft.ifft(optimal)*fs

		# -- Normalize the matched filter output:
		# Normalize the matched filter output so that we expect a value of 1 at times of just noise.
		# Then, the peak of the matched filter output will tell us the signal-to-noise ratio (SNR) of the signal.
		sigmasq = 1*(template_fft * template_fft.conjugate() / power_vec).sum() * df
		sigma = np.sqrt(np.abs(sigmasq))
		SNR_complex = optimal_time/sigma

		# shift the SNR vector by the template length so that the peak is at the END of the template
		peaksample = int(data.size / 2)  # location of peak in the template
		SNR_complex = np.roll(SNR_complex,peaksample)
		SNR = abs(SNR_complex)

		# find the time and SNR value at maximum:
		indmax = np.argmax(SNR)
		timemax = time[indmax]
		SNRmax = SNR[indmax]

		# Calculate the "effective distance" (see FINDCHIRP paper for definition)
		# d_eff = (8. / SNRmax)*D_thresh
		d_eff = sigma / SNRmax
		# -- Calculate optimal horizon distnace
		horizon = sigma/8

		# Extract time offset and phase at peak
		phase = np.angle(SNR_complex[indmax])
		offset = (indmax-peaksample)

		# apply time offset, phase, and d_eff to template 
		template_phaseshifted = np.real(template*np.exp(1j*phase))    # phase shift the template
		template_rolled = np.roll(template_phaseshifted,offset) / d_eff  # Apply time offset and scale amplitude

		# Whiten and band-pass the template for plotting
		template_whitened = whiten(template_rolled,interp1d(freqs, data_psd),dt)  # whiten the template
		template_match = filtfilt(bb, ab, template_whitened) / normalization # Band-pass the template

		print('For detector {0}, maximum at {1:.4f} with SNR = {2:.1f}, D_eff = {3:.2f}, horizon = {4:0.1f} Mpc' 
			  .format(det,timemax,SNRmax,d_eff,horizon))

		if make_plots:

			# plotting changes for the detectors:
			if det is 'L1': 
				pcolor='g'
				strain_whitenbp = strain_L1_whitenbp
				template_L1 = template_match.copy()
			else:
				pcolor='r'
				strain_whitenbp = strain_H1_whitenbp
				template_H1 = template_match.copy()

			# -- Plot the result
			plt.figure(figsize=(10,8))
			plt.subplot(2,1,1)
			plt.plot(time-timemax, SNR, pcolor,label=det+' SNR(t)')
			#plt.ylim([0,25.])
			plt.grid('on')
			plt.ylabel('SNR')
			plt.xlabel('Time since {0:.4f}'.format(timemax))
			plt.legend(loc='upper left')
			plt.title(det+' matched filter SNR around event')

			# zoom in
			plt.subplot(2,1,2)
			plt.plot(time-timemax, SNR, pcolor,label=det+' SNR(t)')
			plt.grid('on')
			plt.ylabel('SNR')
			plt.xlim([-0.15,0.05])
			#plt.xlim([-0.3,+0.3])
			plt.grid('on')
			plt.xlabel('Time since {0:.4f}'.format(timemax))
			plt.legend(loc='upper left')
			plt.savefig('figurs/'+eventname+"_"+det+"_SNR."+plottype)

			plt.figure(figsize=(10,8))
			plt.subplot(2,1,1)
			plt.plot(time-tevent,strain_whitenbp,pcolor,label=det+' whitened h(t)')
			plt.plot(time-tevent,template_match,'k',label='Template(t)')
			plt.ylim([-10,10])
			plt.xlim([-0.15,0.05])
			plt.grid('on')
			plt.xlabel('Time since {0:.4f}'.format(timemax))
			plt.ylabel('whitened strain (units of noise stdev)')
			plt.legend(loc='upper left')
			plt.title(det+' whitened data around event')

			plt.subplot(2,1,2)
			plt.plot(time-tevent,strain_whitenbp-template_match,pcolor,label=det+' resid')
			plt.ylim([-10,10])
			plt.xlim([-0.15,0.05])
			plt.grid('on')
			plt.xlabel('Time since {0:.4f}'.format(timemax))
			plt.ylabel('whitened strain (units of noise stdev)')
			plt.legend(loc='upper left')
			plt.title(det+' Residual whitened data after subtracting template around event')
			plt.savefig('figurs/'+eventname+"_"+det+"_matchtime."+plottype)

			# -- Display PSD and template
			# must multiply by sqrt(f) to plot template fft on top of ASD:
			plt.figure(figsize=(10,6))
			template_f = np.absolute(template_fft)*np.sqrt(np.abs(datafreq)) / d_eff
			plt.loglog(datafreq, template_f, 'k', label='template(f)*sqrt(f)')
			plt.loglog(freqs, np.sqrt(data_psd),pcolor, label=det+' ASD')
			plt.xlim(20, fs/2)
			plt.ylim(1e-24, 1e-20)
			plt.grid()
			plt.xlabel('frequency (Hz)')
			plt.ylabel('strain noise ASD (strain/rtHz), template h(f)*rt(f)')
			plt.legend(loc='upper left')
			plt.title(det+' ASD and template around event')
			plt.savefig('figurs/'+eventname+"_"+det+"_matchfreq."+plottype)
            