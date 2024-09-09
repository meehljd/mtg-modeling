"""Add icons to plots as tick labels, plot labels, or points"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
from PIL import Image
import pandas as pd

icon_root = Path("images/mana_symbols/png")
png_files = list(icon_root.glob("*"))
label_to_icon = {f.stem: f for f in png_files}

def _infer_plot_type():
    ax = plt.gca()

    if any(isinstance(child, plt.Rectangle) for child in ax.get_children() if child.get_label() != '_nolegend_'):
        return "bar"
    elif any(isinstance(child, plt.Line2D) for child in ax.get_lines()):
        return "line"
    elif any(isinstance(child, plt.PathCollection) for child in ax.collections):
        return "scatter"
    else:
        raise ValueError(f"Cannot infer plot type for {ax}")

def _load_image(path, scale=0.5):
    img = Image.open(path)
    img = img.resize((int(img.width * scale), int(img.height * scale)))
    return np.array(img)


def add_tick_symbols(data, plot_type=None, orient="y", scale=0.75):
    """Adds icons, such as mana symbols, as the plot axis labels."""
    fig = plt.gcf()
    ax = plt.gca()

    y_lims = ax.get_ylim()
    x_lims = ax.get_xlim()
    fig_lims = fig.get_size_inches()

    if plot_type is None:
        plot_type = _infer_plot_type()

    if plot_type == "bar":
        bars = ax.patches
    else:
        raise NotImplementedError(f"The plot type of {plot_type} is not yet supported.")

    for bar, label in zip(bars, data):
        icon = _load_image(label_to_icon[label], scale=1)

        aspect_ratio = (
            (y_lims[1] - y_lims[0])
            / (x_lims[1] - x_lims[0])
            * fig_lims[0]
            / fig_lims[1]
        )

        if orient == "y":
            icon_height = bar.get_height() * scale
            y = bar.get_y() + bar.get_height() / 2
            icon_width = icon_height / aspect_ratio
            x = icon_width * 1.1 + x_lims[0]
        else:
            raise NotImplementedError("can only support orient=y")
        ax.imshow(
            icon,
            extent=(x, x - icon_width, y + icon_height / 2, y - icon_height / 2),
            clip_on=False,
            aspect="auto",
            zorder=50,
        )

    ax.set_ylim(y_lims)
    ax.set_xlim(x_lims)

    yticks = ax.get_yticks()
    ax.set_yticks(yticks)
    ax.set_yticklabels([])
    ax.yaxis.set_label_coords(icon_width / (x_lims[1] - x_lims[0]) * 1.1, 0.5)


def add_timeseries_symbols(data, x_col, y_col, label_col, loc, scale=0.05):
    """Adds icons to the time series lines."""
    fig = plt.gcf()
    ax = plt.gca()

    y_lims = ax.get_ylim()
    x_lims = ax.get_xlim()
    fig_lims = fig.get_size_inches()

    mask = data[x_col] == loc
    labels = data.loc[mask].sort_values(y_col, ascending=False)

    w = (x_lims[1] - x_lims[0]) * scale
    h = (y_lims[1] - y_lims[0]) * scale * fig_lims[0] / fig_lims[1]
    for i, row in labels.iterrows():
        icon = _load_image(label_to_icon[row[label_col]])
        x = mdates.date2num(row[x_col])
        y = row[y_col] - y_lims[1] * 0.0
        ax.imshow(
            icon,
            extent=(
                x - w / 2,
                x + w / 2,
                y - h / 2,
                y + h / 2,
            ),
            aspect="auto",  # Preserve aspect ratio of the image
            zorder=5,  # Draw images above plot lines
        )

    ax.set_ylim(y_lims)
    ax.set_xlim(x_lims)


def add_plot_symbols(data, x_col, y_col, label_col, scale=0.05):
    """Adds icons to the time series lines."""
    fig = plt.gcf()
    ax = plt.gca()

    y_lims = ax.get_ylim()
    x_lims = ax.get_xlim()
    fig_lims = fig.get_size_inches()

    w = (x_lims[1] - x_lims[0]) * scale
    h = (y_lims[1] - y_lims[0]) * scale * fig_lims[0] / fig_lims[1]
    for i, row in data.iterrows():
        icon = _load_image(label_to_icon[row[label_col]])
        x = row[x_col]
        y = row[y_col]
        ax.imshow(
            icon,
            extent=(
                x - w / 2,
                x + w / 2,
                y - h / 2,
                y + h / 2,
            ),
            aspect="auto",  # Preserve aspect ratio of the image
            zorder=5,  # Draw images above plot lines
        )

    ax.set_ylim(y_lims)
    ax.set_xlim(x_lims)
