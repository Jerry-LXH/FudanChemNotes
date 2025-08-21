import numpy as np
import matplotlib.pyplot as plt

def plot_spectrum(wl, tr, name=None, assume_unit=None, save_path=None, mode="T"):
    '''Plot spectrum.'''
    wl = np.asarray(wl, dtype=float)
    tr = np.asarray(tr, dtype=float)
    order = np.argsort(wl)
    wl, tr = wl[order], tr[order]
    if assume_unit is None:
        use_percent = (np.nanmax(tr) > 1.5)
    else:
        use_percent = (assume_unit == 'percent')

    if mode.upper() == "T":  # 透过率模式
        y = tr * (1 if use_percent else 100)
        y_label = "Transmission (%)"
    elif mode.upper() == "OD":  # 光密度模式
        frac = tr / 100 if use_percent else tr
        # 避免 log(0)，加一个小epsilon
        frac = np.clip(frac, 1e-6, 1.0)
        y = -np.log10(frac)
        y_label = "Optical Density (OD)"
    else:
        raise ValueError("mode 应为 'T' 或 'OD'")

    plt.figure()
    plt.plot(wl, y, linewidth=1.6, label=name if name else "Spectrum")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel(y_label)
    plt.title(name if name else "Filter Spectrum")
    plt.grid(True, alpha=0.3)
    if name:
        plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200)
    else:
        plt.show()

def plot_multiple_spectra(spectra, assume_unit=None, mode="T", title="Filter Comparison", save_path=None):
    """Plot multiple spectra: list[(name, wl, tr)]."""
    plt.figure()
    for name, wl, tr in spectra:
        wl = np.asarray(wl, dtype=float)
        tr = np.asarray(tr, dtype=float)
        order = np.argsort(wl)
        wl, tr = wl[order], tr[order]

        if assume_unit is None:
            use_percent = (np.nanmax(tr) > 1.5)
        else:
            use_percent = (assume_unit == 'percent')

        if mode.upper() == "T":
            y = tr * (1 if use_percent else 100)
            y_label = "Transmission (%)"
        elif mode.upper() == "OD":
            frac = tr / 100 if use_percent else tr
            frac = np.clip(frac, 1e-6, 1.0)
            y = -np.log10(frac)
            y_label = "Optical Density (OD)"
        else:
            raise ValueError("mode 应为 'T' 或 'OD'")

        plt.plot(wl, y, linewidth=1.6, label=name)

    plt.xlabel("Wavelength (nm)")
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200)
    else:
        plt.show()
