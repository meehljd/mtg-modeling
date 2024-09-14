"""Add icons to plots as tick labels, plot labels, or points"""

from pathlib import Path

import matplotlib.collections
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from PIL import Image
import pandas as pd

icon_root = Path("images/mana_symbols/png")
png_files = list(icon_root.glob("*"))
label_to_icon = {f.stem: f for f in png_files}


def _load_image(path, scale=0.5):
    img = Image.open(path)
    img = img.resize((int(img.width * scale), int(img.height * scale)))
    return np.array(img)

def add_tick_symbols(orient="y", scale=0.75, x_top=False):
    """Adds icons, such as symbols, as the plot axis labels."""
    fig = plt.gcf()
    ax = plt.gca()

    y_lims = ax.get_ylim()
    x_lims = ax.get_xlim()
    fig_lims = fig.get_size_inches()

    yticks = ax.get_yticks()
    xticks = ax.get_xticks()

    if orient == "y":
        tick_labels = ax.get_yticklabels()
        tick_positions = yticks
    else:
        tick_labels = ax.get_xticklabels()
        tick_positions = xticks

    for tick, pos in zip(tick_labels, tick_positions):
        label = tick.get_text()
        icon = _load_image(label_to_icon[label], scale=scale)
        aspect_ratio = (y_lims[1] - y_lims[0]) / (x_lims[1] - x_lims[0]) * fig_lims[0] / fig_lims[1]

        if orient == "y":
            icon_height = (y_lims[1] - y_lims[0]) / len(yticks) * scale
            y = pos
            icon_width = icon_height / aspect_ratio
            x = x_lims[0] - icon_width * 1.15
            ax.imshow(
                icon,
                extent=(x, x + icon_width, y - icon_height / 2, y + icon_height / 2),
                clip_on=False,
                aspect="auto",
                zorder=50,
            )
        else:
            icon_width = (x_lims[1] - x_lims[0]) / len(xticks) * scale
            x = pos
            icon_height = icon_width * aspect_ratio
            if x_top:
                y = 1 + icon_height * 1.45
            else:
                y = y_lims[0] - icon_height * 1.15
            ax.imshow(
                icon,
                extent=(x - icon_width / 2, x + icon_width / 2, y, y + icon_height),
                clip_on=False,
                aspect="auto",
                zorder=50,
            )

    if orient == "y":
        ax.set_yticks(yticks)
        ax.set_yticklabels([])
        ax.yaxis.set_label_coords(-icon_width / (x_lims[1] - x_lims[0]) * 1.3, 0.5)
    else:
        ax.set_xticks(xticks)
        ax.set_xticklabels([])
        if x_top:
            ax.xaxis.set_label_position("top")
            ax.xaxis.tick_top()
            ax.xaxis.set_label_coords(0.5, 1 + icon_height / (y_lims[1] - y_lims[0]) * 1.3)
        else:
            ax.xaxis.set_label_coords(0.5, -icon_height / (y_lims[1] - y_lims[0]) * 1.3)

    ax.set_xlim(x_lims)
    ax.set_ylim(y_lims)


def add_heatmap_symbols(scale=0.75):
    add_tick_symbols(orient="y", scale=scale)
    add_tick_symbols(orient="x", scale=scale, x_top=True)


def add_timeseries_symbols(data, x_col, y_col, label_col, locs, scale=0.035):
    """Adds icons to the time series lines."""
    fig = plt.gcf()
    ax = plt.gca()

    y_lims = ax.get_ylim()
    x_lims = ax.get_xlim()
    fig_lims = fig.get_size_inches()

    if not isinstance(locs, list):
        locs = [locs]

    for loc in locs:
        if loc == 'first':
            loc = data[x_col].min()
        elif loc == 'last':
            loc = data[x_col].max()

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


def add_plot_symbols(data, x_col, y_col, label_col, scale=0.045):
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
