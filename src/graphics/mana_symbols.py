"""Creates mana icons for each color combination.

Using the color_palette.yaml file, draws circles using 
mana colors and characters. For multi-color combinations, 
each color is a circle sector (i.e. pizza slice).  
The circles are saved as PNG.
"""

import matplotlib.pyplot as plt
import numpy as np
import yaml

SCALE = 100

def get_circle_sector_points(rotation=45, extend=180):
    """Defines the geometric points of the circle sector."""

    # Define the partial circle points
    theta = np.linspace(0, np.deg2rad(extend), SCALE)
    x = np.cos(theta)
    y = np.sin(theta)

    # Rotate the points by 45 degrees
    t = np.deg2rad(rotation)
    x_rotated = x * np.cos(t) - y * np.sin(t)
    y_rotated = x * np.sin(t) + y * np.cos(t)

    # Center the semicircle in the 100x100 image with center at (50, 50)
    center = SCALE / 2
    x_centered = center + 0.40 * SCALE * x_rotated
    y_centered = center + 0.40 * SCALE * y_rotated

    # Add lines to form the complete shape
    if extend < 360:
        x_centered = np.concatenate(([center], x_centered, [center]))
        y_centered = np.concatenate(([center], y_centered, [center]))
    return {"x": x_centered, "y": y_centered}


def plot_circle_sector(char, fill_color, sector_lines, text_pos, fontsize):
    """Plots the circle sector, including lines, fill, and text."""
    ax.plot(
        sector_lines["x"], sector_lines["y"], color="black", linewidth=0.25, zorder=2
    )

    scale_factor = 0.98
    scaled_x = SCALE / 2 + (sector_lines["x"] - SCALE / 2) * scale_factor
    scaled_y = SCALE / 2 + (sector_lines["y"] - SCALE / 2) * scale_factor

    ax.fill(scaled_x, scaled_y, color=fill_color, zorder=1)
    ax.text(
        text_pos["x"] * SCALE / 100,
        text_pos["y"] * SCALE / 100,
        char,
        fontsize=fontsize,
        color="#130c0e",
        ha="center",
        va="center",
        fontname="monospace",
        weight="bold",
    )

def save_plot():
    """Clean up and save plot."""
    ax.set_aspect("equal")
    plt.xlim(0, SCALE)
    plt.ylim(0, SCALE)
    plt.axis("off")
    plt.savefig(
        f"images/mana_symbols/png/{name}.png",
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )
    plt.close()

# Read configs
with open("src/graphics/color_palette.yml", "r", encoding="utf-8") as file:
    color_config = yaml.safe_load(file)
color_palette = color_config["colors"]
text_configs = color_config["text_positions"]
start_angles = color_config["start_angles"]

# Draw mana symbols
for name, colors in color_config["pairs"].items():
    n_colors = len(colors)
    text_config = text_configs[n_colors]
    sector_angle = 360 / n_colors
    fig, ax = plt.subplots(figsize=(1, 1), dpi=SCALE)
    for i, color in enumerate(colors):
        rotation_angle = start_angles[n_colors] - i * sector_angle
        lines = get_circle_sector_points(rotation=rotation_angle, extend=sector_angle)

        plot_circle_sector(
            char=color,
            fill_color=color_palette[color],
            sector_lines=lines,
            text_pos=text_config["text_pos"][i],
            fontsize=text_config["size"],
        )

    save_plot()
