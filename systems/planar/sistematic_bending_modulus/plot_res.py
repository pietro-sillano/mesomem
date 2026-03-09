# Import numpy at the beginning of the file
import numpy as np
from typing import Tuple, Optional
import matplotlib.pyplot as plt
import argparse

def plot_autocorr_selected(qcenters: np.ndarray, acorr_binned: np.ndarray,acorr_std, lags: np.ndarray, show_bins: int = 10) -> None:
    """
    Plot a few representative binned autocorrelation curves.

    Parameters
    ----------
    qcenters : np.ndarray
        Array (n_bins,) of q bin centers.
    acorr_binned : np.ndarray
        Array (n_bins, n_lags) of autocorrelations.
    lags : np.ndarray
        Integer lag array.
    dt_seconds : float
        Time between frames in seconds; used to convert lag->time.
    show_bins : int
        Number of bins to plot (evenly sampled across q range).
    """
    n_bins = len(qcenters)
    chosen = np.linspace(0, n_bins - 1, min(show_bins, n_bins), dtype=int)

    t = lags

    plt.figure(figsize=(8, 5))
    for ib in chosen:
        curve = acorr_binned[ib]
        if np.all(np.isnan(curve)):
            continue
        # plt.plot(t, curve, label=f'q={qcenters[ib]:.3g} (bin {ib})')
        plt.errorbar(t, curve, yerr=acorr_std[ib], fmt='o-', capsize=5, capthick=1.5, alpha=0.5,label=f'q={qcenters[ib]:.3g} (bin {ib})')

    plt.xlabel('Time lag (s)')
    plt.ylabel('Normalized autocorrelation')
    plt.title('Autocorrelation vs time lag for selected q-bins')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("autocorr",dpi=300)
    plt.show()
    plt.close()
    
def bin_by_q(qvals: np.ndarray, acorr: np.ndarray, n_bins: int = 20, qmin: Optional[float] = None, qmax: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Bin modes by their |q| magnitude and average autocorrelations within each bin.

    Parameters
    ----------
    qvals : np.ndarray
        1D array of |q| for each mode (length n_modes).
    acorr : np.ndarray
        2D array (n_modes, n_lags) of autocorrelations.
    n_bins : int
        Number of q bins.
    qmin, qmax : floats or None
        Minimum and maximum q for binning. Defaults to full range.

    Returns
    -------
    q_bin_centers : np.ndarray
        Center q-value for each bin (length n_bins).
    acorr_binned : np.ndarray
        Averaged autocorrelation per bin (n_bins, n_lags).
    counts : np.ndarray
        Number of modes in each bin.
    """
    if qmin is None:
        qmin = qvals.min()
    if qmax is None:
        qmax = qvals.max()

    # Exclude zero-mode if present (k=0) to avoid trivial behavior in bins
    mask_nonzero = qvals > 0.0
    q_nonzero = qvals[mask_nonzero]
    acorr_nonzero = acorr[mask_nonzero]

    bins = np.linspace(qmin, qmax, n_bins + 1)
    bin_indices = np.digitize(q_nonzero, bins) - 1

    acorr_binned = np.zeros((n_bins, acorr.shape[1]), dtype=np.float64)
    acorr_std = np.zeros((n_bins, acorr.shape[1]), dtype=np.float64)
    counts = np.zeros(n_bins, dtype=int)

    for ibin in range(n_bins):
        sel = bin_indices == ibin
        counts[ibin] = sel.sum()
        if counts[ibin] > 0:
            acorr_binned[ibin] = acorr_nonzero[sel].mean(axis=0)
            acorr_std[ibin] = acorr_nonzero[sel].std(axis=0)
        else:
            acorr_binned[ibin] = np.nan
            acorr_std[ibin] = np.nan

    # Bin centers
    q_bin_centers = 0.5 * (bins[:-1] + bins[1:])

    return q_bin_centers, acorr_binned, acorr_std, counts   
    
            


# Load each file separately
parser = argparse.ArgumentParser()
parser.add_argument('--base_dir', type=str, default="/martini/pietro/new_potential_v2/planar/fluctuation_pipeline/test_acorr/")
args = parser.parse_args()
folder = args.base_dir


acorr = np.load(folder+"autocorr_results/acorr.npy")
kx = np.load(folder+"autocorr_results/kx.npy")
ky = np.load(folder+"autocorr_results/ky.npy")
lags = np.load(folder+"autocorr_results/lags.npy")
qvals = np.load(folder+"autocorr_results/qvals.npy")

# print(f"acorr: {acorr.shape}")
# print(f"kx: {kx.shape}")
# print(f"ky: {ky.shape}")
# print(f"lags: {lags.shape}")
# print(f"qvals: {qvals.shape}")


# === Bin by q and average to reduce noise ===
n_bins = 24
# q_centers, acorr_binned, acorr_std, counts = bin_by_q(qvals, acorr, n_bins=n_bins,qmin=0.0,qmax=2.0)

    
# === Plot a few representative binned autocorrelation curves ===
# plot_autocorr_selected(q_centers, acorr,acorr_std, lags, show_bins=3)


# === Plot single modes ===
# Exclude zero-mode if present (k=0) to avoid trivial behavior in bins
mask_nonzero = qvals > 0.0
qvals = qvals[mask_nonzero]
acorr = acorr[mask_nonzero]

# sort qvals and reorder corresponding arrays the same way
order = np.argsort(qvals)
qvals = qvals[order]
acorr = acorr[order]
# also reorder kx/ky if you want to keep mode vectors aligned
kx = kx[order]
ky = ky[order]

n_mode_plot = 5

q_unique = np.unique(qvals)

for idx,q in enumerate(q_unique):
    if idx < n_mode_plot:
        # print(q)
        mask = (qvals==q)
        # print(kx[mask],ky[mask])
        print(f"Mode n:{idx} averaged over {len(acorr[mask,:])} amplitudes")
        acorr_mean = np.mean(acorr[mask,:],axis=0)
        acorr_std = np.std(acorr[mask,:],axis=0)
        
        # Plots the line for every point, but error bars every 10 points
        plt.errorbar(
            lags, 
            acorr_mean, 
            yerr=acorr_std, 
            label=f'q: {q:.4f}', 
            alpha=0.7,      # Increased alpha for the line
            errorevery=20,  # Only show error bars every 10th lag
            capsize=2       # Adds little 'caps' to the bars for better visibility
        )

mid_time = int(len(lags) * 0.5)
plt.vlines(lags[mid_time],np.min(acorr[:n_mode_plot,:]),np.max(acorr[:n_mode_plot,:]),'k','--',label='T/2')
plt.xlabel('Time lag (frame)')
plt.ylabel('Normalized autocorrelation')
plt.ylim(-2.0,2.0)
plt.title('Autocorrelation vs time lag for single mode')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(folder+"autocorr_single_modes.png",dpi=300)
plt.show()