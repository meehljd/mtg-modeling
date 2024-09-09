"""Supplemental annotations for plots, such as labels or lines."""

from sys import implementation
import pandas as pd
from pytest import yield_fixture
from tqdm.notebook import tqdm
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import to_rgba, to_hex
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import time
import polars as pl
from datetime import datetime, timedelta
from PIL import Image
from typing import Optional, Union, Dict, List
from matplotlib.legend import Legend


def set_axis_labels_and_show(
    suptitle: Optional[str] = None,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    legend: Union[bool, Legend] = False,
    legend_title: Optional[str] = None,
    legend_labels: Optional[Dict[str, str]] = None,
    tight: bool = True,
    show: bool = True,
    rot_x: bool = False,
    reverse_y: bool = False,
):
    """Sets the title and axis labels and shows the plot."""

    fig = plt.gcf()
    ax = plt.gca()

    if suptitle is not None:
        plt.suptitle(title)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if legend:
        if legend_labels is not None:
            if isinstance(legend, Legend):
                for text in legend.get_texts():
                    text.set_text(legend_labels.get(text.get_text(), text.get_text()))
            else:
                raise ValueError(
                    "'legend' needs to be a boolean or a matplotlib.legend.Legend type"
                )
        if isinstance(legend, bool):
            plt.legend(title=legend_title)
    if rot_x:
        plt.xticks(rotation=90)
    if reverse_y:
        plt.gca().invert_yaxis()
    if tight:
        plt.tight_layout()
    if show:
        plt.show()


def _format_axis_labels(formatter, axis):
    ax = plt.gca()

    if axis == "x":
        ax.xaxis.set_major_formatter(formatter)
    elif axis == "y":
        ax.yaxis.set_major_formatter(formatter)
    elif axis == "xy":
        ax.xaxis.set_major_formatter(formatter)
        ax.yaxis.set_major_formatter(formatter)
    else:
        raise ValueError(f"axis {axis} is not supported.")


def _get_percent_precision(axis='x'):
    ax = plt.gca()
    if axis=='x':
        lims = ax.get_xlim()
    elif axis=='y':
        lims = ax.get_ylim()
    elif axis=='xy':
        lims = ax.get_xlim()

    span = max(lims) - min(lims)
    if span < 0.01:
        return 2
    elif span < 0.1:
        return 1
    else:
        return 0

def set_labels_to_percent(axis="x", precision=None):
    """Sets the axis labels to percent format"""

    precision = _get_percent_precision(axis)
    formatter = FuncFormatter(lambda x, _: f"{x:.{precision}%}")
    _format_axis_labels(formatter, axis)


def set_labels_to_commas(axis="x", precision=0):
    """Sets the axis labels to percent format"""
    formatter = FuncFormatter(lambda x, _: f"{x:,.{precision}f}")
    _format_axis_labels(formatter, axis)

def set_labels_to_ints(axis="x"):
    """Converts floating point axis tick labels to integers."""
    ticks = plt.gca().get_xticks()
    ticks = list(set(map(int, ticks)))

    plt.xticks(
        ticks=ticks,
        labels=[str(x) for x in ticks],
    )

def annotate_bars(padding_ratio=1.05):
    """Annotate the bars in a bar plot with the height of the bar."""
    fig = plt.gcf()
    ax = plt.gca()

    for container in ax.containers:

        # Format labels
        labels = []
        for height in container.datavalues:
            if height < 0.0001:
                labels.append(f"{height:.4%}")
            elif height < 0.001:
                labels.append(f"{height:.3%}")
            elif height < 0.01:
                labels.append(f"{height:.2%}")
            elif height < 0.1:
                labels.append(f"{height:.1%}")
            else:
                labels.append(f"{height:.1%}")

        # Write the labels
        ax.bar_label(
            container,
            labels=labels,
            label_type="edge",
            fontsize=10,
            padding=1,
            # fontstyle="italic",
            alpha=0.75,
        )

    # Pad the x-axis limits
    ax.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1] * padding_ratio)


def plot_vert_line(x, label=None, use_arrow=False, offset=0, y_pos=0.83):
    """Plots a vertical line with optional annotation."""
    fig = plt.gcf()
    ax = plt.gca()

    if isinstance(x, datetime):
        x = mdates.date2num(x)

    args = dict(
        color="gray",
        linestyle="--",
        linewidth=2,
        alpha=0.5,
    )

    # Plot the line
    plt.axvline(x, **args)

    # Annotation settings
    text_args = dict(
        ha="center",
        va="center",
        color="gray",
        alpha=0.5,
        fontweight="normal",
        rotation=90,
        fontsize=8,
    )

    y = ax.get_ylim()[0] * y_pos

    x_lims = ax.get_xlim()
    offset = (x_lims[1] - x_lims[0]) * offset

    # Add the label
    if label is not None:
        if use_arrow:
            plt.annotate(
                label,
                xy=(
                    x,
                    y,
                ),
                xytext=(
                    x,
                    y + offset,
                ),
                arrowprops=dict(arrowstyle="-", lw=1.0, color="grey"),
                **text_args,
            )
        else:
            plt.text(
                x + offset,
                y,
                label,
                **text_args,
            )
