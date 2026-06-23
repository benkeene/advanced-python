import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl
import matplotlib.pyplot as plt

# ── Named colors ──
# ax.plot(x, y, color='gb_red')
# ax.set_facecolor('gb_bg1')
gruvbox = {
    "gb_bg": "#282828",
    "gb_bg0_h": "#1d2021",
    "gb_bg0_s": "#32302f",
    "gb_bg1": "#3c3836",
    "gb_bg2": "#504945",
    "gb_bg3": "#665c54",
    "gb_bg4": "#7c6f64",
    "gb_fg": "#ebdbb2",
    "gb_fg0": "#fbf1c7",
    "gb_fg1": "#ebdbb2",
    "gb_fg2": "#d5c4a1",
    "gb_fg3": "#bdae93",
    "gb_fg4": "#a89984",
    "gb_red": "#cc241d",
    "gb_green": "#98971a",
    "gb_yellow": "#d79921",
    "gb_blue": "#458588",
    "gb_purple": "#b16286",
    "gb_aqua": "#689d6a",
    "gb_orange": "#d65d0e",
    "gb_red_l": "#fb4934",
    "gb_green_l": "#b8bb26",
    "gb_yellow_l": "#fabd2f",
    "gb_blue_l": "#83a598",
    "gb_purple_l": "#d3869b",
    "gb_aqua_l": "#8ec07c",
    "gb_orange_l": "#fe8019",
    "gb_gray": "#928374",
}
mcolors.get_named_colors_mapping().update(gruvbox)

# ── Colormaps ──

# ax.imshow(data, cmap='gruvbox_seq')
# ax.contourf(X, Y, Z, cmap='gruvbox_seq')
_cmaps = {
    # plt.scatter(x, y, c=values, cmap='gruvbox_seq')
    "gruvbox_seq": ["#282828", "#d65d0e", "#d79921", "#fabd2f", "#ebdbb2"],
    # ax.pcolormesh(X, Y, Z, cmap='gruvbox_heat')
    "gruvbox_heat": ["#282828", "#cc241d", "#d65d0e", "#d79921", "#fabd2f"],
    # ax.contour(X, Y, Z, cmap='gruvbox_cool')
    "gruvbox_cool": ["#282828", "#458588", "#689d6a", "#83a598", "#ebdbb2"],
    # ax.imshow(residuals, cmap='gruvbox_div', vmin=-1, vmax=1)
    "gruvbox_div": ["#458588", "#83a598", "#ebdbb2", "#fb4934", "#cc241d"],
}
for name, colors in _cmaps.items():
    cmap = LinearSegmentedColormap.from_list(name, colors)
    mpl.colormaps.register(cmap, name=name)
    # cmap='gruvbox_seq_r' for any reversed variant
    mpl.colormaps.register(cmap.reversed(), name=f"{name}_r")
