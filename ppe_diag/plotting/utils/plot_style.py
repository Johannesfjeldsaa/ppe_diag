# This script provides a set of functions to set the default plotting style for diagrams
# in the PPE diagnostics.

# -------------------------- #
# --- Table of Functions --- #
# -------------------------- #

# set_plt_plot_style: Sets the default plotting style for matplotlib figures.

# ----------------------- #
# --- library imports --- #
# ----------------------- #

import cartopy
import cmocean
import seaborn as sns
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

def set_matplotlib_style():
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'figure.figsize': (8, 6),
        'axes.spines.top': False,
        'axes.spines.right': False,
    })

def set_seaborn_style(context='notebook', style='whitegrid'):
    sns.set_theme(context=context, style=style, font_scale=1.2)

def get_colormap(variable_name):
    # Map variable names to appropriate cmocean colormaps
    mapping = {
        'heatmap': cmocean.tools.crop_by_percent(cmocean.cm.tarn, 30, which='both', N=None),
    }
    if variable_name in mapping:
        return mapping[variable_name]
    elif variable_name in cmocean.cm.__dict__:
        return cmocean.cm.__dict__[variable_name]
    else:
        raise ValueError(f"No colormap defined for variable '{variable_name}'. Please define a mapping in mapping).")

def set_cartopy_defaults(
    ax,
    projection=ccrs.PlateCarree(),
    coastlines=True,
    borders=True,
    gridlines=True,
    gridlines_kwargs=None,
    central_longitude=0,
    extent=None
    ):
    if coastlines:
        ax.coastlines()
    if borders:
        ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    if gridlines:
        if gridlines_kwargs is None:
            gridlines_kwargs = {}
        ax.gridlines(crs=projection, draw_labels=True, **gridlines_kwargs)
    if extent:
        ax.set_extent(extent, crs=projection)
    if central_longitude != 0:
        ax.set_global(central_longitude=central_longitude)

def xarray_plot_style(**kwargs):
    # Default kwargs for xr.DataArray.plot()
    defaults = {'cmap': cmocean.cm.matter, 'robust': True, 'add_colorbar': True}
    defaults.update(kwargs)
    return defaults

# Style mapping for common statistics measures and reference/observation cases
STATISTIC_STYLES = {
    "mean":      {"color": "#000000", "linestyle": "-",  "linewidth": 2, "label": "Mean"},
    "median":    {"color": "#2ca02c", "linestyle": "--", "linewidth": 2, "label": "Median"},
    "min":       {"color": "#000000", "linestyle": ":",  "linewidth": 1, "label": "Min"},
    "max":       {"color": "#000000", "linestyle": ":",  "linewidth": 1, "label": "Max"},
    "std":       {"color": "#335fff", "linestyle": "-.", "linewidth": 2, "label": "Std dev"},
    "stdrange": {"color": "#33abff", "linestyle": "--", "linewidth": 2, "label": "Std range"},
    "percentile_10": {"color": "#8c564b", "linestyle": ":", "linewidth": 1, "label": "10th Percentile"},
    "percentile_90": {"color": "#e377c2", "linestyle": ":", "linewidth": 1, "label": "90th Percentile"},
    "iqr":       {"color": "#883838FF", "linestyle": "--", "linewidth": 2, "label": "IQR"},
    "observations": {
        "color": "#727272", "linestyle": "-", "linewidth": 3, "marker": "o", "label": "Observations"
    },
    "observationsrange": {
        "color": "#929292", "linestyle": "--", "linewidth": 2, "marker": "o", "label": "Obs. Range"
    },
    "reference_case": {
        "color": "#ff0000", "linestyle": "--", "linewidth": 2, "marker": "^", "label": "Reference Case"
    },
    "reference_case_historical": {
        "color": "#c21616", "linestyle": "-.", "linewidth": 2, "marker": "s", "label": "Reference Case (Hist.)"
    },
}

def get_ensemble_colors(n_members, cmap_name="tab20"):
    """
    Returns a list of colors for ensemble members using a specified colormap.
    """
    cmap = plt.get_cmap(cmap_name)
    return [cmap(i / n_members) for i in range(n_members)]

def get_member_color(member_idx, n_members, cmap_name="tab20"):
    """
    Returns the color for a specific ensemble member index.
    """
    colors = get_ensemble_colors(n_members, cmap_name)
    return colors[member_idx]

def reset_styles():
    plt.rcdefaults()
    sns.reset_defaults()