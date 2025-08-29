import csv
import numpy as np
from scipy.interpolate import interp1d

def read_filter_csv(file_path, wavelength_col=0, transmission_col=1, skip_header=True):
    """Read from csv file the specturm into 2 np arrays."""
    wavelengths, transmissions = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader, None)  # 跳过第一行表头
        for row in reader:
            try:
                wl = float(row[wavelength_col])
                tr = float(row[transmission_col])
                wavelengths.append(wl)
                transmissions.append(tr)
            except ValueError:
                continue  # 遇到空行/非数字行则跳过
    return np.array(wavelengths), np.array(transmissions)

def read_filter_txt(file_path, wavelength_col=0, transmission_col=1, skip_header=True):
    """Read from csv file the specturm into 2 np arrays.
       Transmission values will be multiplied by 100.
    """
    wavelengths, transmissions = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        if skip_header:
            next(reader, None)  
        for row in reader:
            try:
                wl = float(row[wavelength_col])
                tr = float(row[transmission_col]) * 100.0  
                wavelengths.append(wl)
                transmissions.append(tr)
            except ValueError:
                continue  
    return np.array(wavelengths), np.array(transmissions)


def resample_spectrum(wavelengths, transmissions, wl_min=300, wl_max=900, step=0.5, kind="linear"):
    """Interpolate linearly so that wavelength form is the same. Default range is 300-900@0.5nm/step."""
    if wl_min is None:
        wl_min = np.min(wavelengths)
    if wl_max is None:
        wl_max = np.max(wavelengths)
    new_wavelengths = np.arange(wl_min, wl_max + step, step)
    f_interp = interp1d(wavelengths, transmissions, kind=kind, bounds_error=False, fill_value="extrapolate")
    new_transmissions = f_interp(new_wavelengths)
    new_transmissions = np.clip(new_transmissions, 0, 100)
    return new_wavelengths, new_transmissions