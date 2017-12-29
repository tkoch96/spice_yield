# Thomas Koch
# a script used to calculate the yield of our design, and generate figures of 
# spreads of cutoff frequency and stop-band attenuation values
# usage: python spice_parser.py
# assumes the output of the ltspice simulation ('proj1p4.txt') is in the same
# directory and in a very particular format determined by ltspice 
import numpy as np
import matplotlib.pyplot as plt
fs = []
mags =[]
i=-1
#parse the exported plot file
with open('proj1p4.txt','r') as f:

	for row in f:
		if row[0:len("Freq")] == "Freq":
			continue
		elif row[0:len("Step")] == "Step":
			i += 1
			fs.append([])
			mags.append([])
			continue
		(fs[i]).append(float(row[0:21]))
		mag_start_ind = row.find('(') + 1
		mag_end_ind = row.find('d')
		(mags[i]).append(float(row[mag_start_ind:mag_end_ind]))
mags = np.array(mags)
fs = np.array(fs)


# YIELD TEST
#test each component to see whether it passed the test

#output arrays for histograms
fs_out = []
mags_out = []


checks = np.zeros([200,1])
for i in range(fs.shape[0]):
	ind_of_cut = 0
	## CHECKING CUTOFF FREQ
	while True:
		if mags[i,ind_of_cut] >= -3:
			break
		ind_of_cut += 1
	#-3 db needs to happen after 10khz to ensure steep enough cutoff
	if fs[i,ind_of_cut-1] >= 10e3:
		#print("i: %d, freq %.4f, mag: %.4f"%(i,fs[i,ind_of_cut], mags[i,ind_of_cut]) )
		checks[i] = 1

	fs_out.append(fs[i,ind_of_cut-1])

	ind_of_cut = 0
	# CHECKING STOPBAND ATTENUATION
	while True:
		if fs[i,ind_of_cut] >= 2.5e3:
			break
		ind_of_cut += 1
	# need -35 db or less at 2.5khz
	if mags[i,ind_of_cut] <= -35:
		#print("i: %d, freq %.4f, mag: %.4f"%(i,fs[i,ind_of_cut], mags[i,ind_of_cut]) )
		checks[i] = 1 * checks[i]

	mags_out.append(mags[i,ind_of_cut])


print("Yield: ", sum(checks) * 1.0 / fs.shape[0])

fs_out = np.array(fs_out)
mags_out = np.array(mags_out)


plt.hist(fs_out)
plt.title('Histogram of Cutoff Frequencies')
plt.xlabel('Frequency (Hz)')
plt.savefig('hist_freqs.png')
plt.cla()
plt.hist(mags_out)
plt.title('Histogram of Attenuations in StopBand')
plt.xlabel('Attenuation (dB)')
plt.savefig('hist_att.png')
