import mne
import matplotlib.pyplot as plt

# Load raw EEG data from EDF file
raw = mne.io.read_raw_edf('eeg_data.edf')

# Filter parameters
fs = 256  # Sampling frequency
fpass = [2, 15]  # Passband frequencies
fstop = [1, 16]  # Stopband frequencies
gpass = 0.5  # Maximum passband ripple
gstop = 40  # Minimum stopband attenuation

# Create band-pass filter
b, a = mne.filter.create_filter(raw.info['sfreq'], fpass, fstop,
                               gpass, gstop, fir_design='firwin')

# Filter raw EEG data
raw_filtered = raw.copy().filter(b, a)

# Compute upper and lower margins
upper_margin = raw_filtered.max()
lower_margin = raw_filtered.min()

# Time-scale compression factor
compression_factor = 6

# Apply time-scale compression
raw_compressed = raw_filtered.copy().resample(raw_filtered.info['sfreq']/compression_factor)

# Compute aEEG tracing
aeeg = raw_compressed.copy().apply_function(np.abs).mean()

# Plot aEEG tracing
plt.plot(aeeg.times, aeeg.data.T)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (μV)')
plt.show()
