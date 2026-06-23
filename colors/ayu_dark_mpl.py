import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl
import matplotlib.pyplot as plt

# ── Named colors ──
# ax.plot(x, y, color='ayu_red')
# ax.set_facecolor('ayu_bg1')
ayu_dark = {
    "ayu_bg": "#0b0e14",
    "ayu_bg0_h": "#0a0e14",
    "ayu_bg0_s": "#11151c",
    "ayu_bg1": "#1f2430",
    "ayu_bg2": "#272d38",
    "ayu_bg3": "#3d4751",
    "ayu_bg4": "#565b66",
    "ayu_fg": "#bfbdb6",
    "ayu_fg0": "#fafafa",
    "ayu_fg1": "#bfbdb6",
    "ayu_fg2": "#b3b1aa",
    "ayu_fg3": "#acb6bf",
    "ayu_fg4": "#565b66",
    "ayu_red": "#d95757",
    "ayu_green": "#aad94c",
    "ayu_yellow": "#e6b673",
    "ayu_blue": "#39bae6",
    "ayu_purple": "#d2a6ff",
    "ayu_aqua": "#95e6cb",
    "ayu_orange": "#ff8f40",
    "ayu_red_l": "#f07178",
    "ayu_green_l": "#c2d94c",
    "ayu_yellow_l": "#ffb454",
    "ayu_blue_l": "#59c2ff",
    "ayu_purple_l": "#a37acc",
    "ayu_aqua_l": "#5ccfe6",
    "ayu_orange_l": "#f29668",
    "ayu_gray": "#626a73",
}
mcolors.get_named_colors_mapping().update(ayu_dark)

# ── Colormaps ──

# ax.imshow(data, cmap='ayu_seq')
# ax.contourf(X, Y, Z, cmap='ayu_seq')
_cmaps = {
    # plt.scatter(x, y, c=values, cmap='ayu_seq')
    "ayu_seq": ["#0b0e14", "#ff8f40", "#ffb454", "#e6b673", "#bfbdb6"],
    # ax.pcolormesh(X, Y, Z, cmap='ayu_heat')
    "ayu_heat": ["#0b0e14", "#d95757", "#ff8f40", "#ffb454", "#e6b673"],
    # ax.contour(X, Y, Z, cmap='ayu_cool')
    "ayu_cool": ["#0b0e14", "#39bae6", "#95e6cb", "#59c2ff", "#bfbdb6"],
    # ax.imshow(residuals, cmap='ayu_div', vmin=-1, vmax=1)
    "ayu_div": ["#39bae6", "#59c2ff", "#bfbdb6", "#f07178", "#d95757"],
}
for name, colors in _cmaps.items():
    cmap = LinearSegmentedColormap.from_list(name, colors)
    mpl.colormaps.register(cmap, name=name)
    # cmap='ayu_seq_r' for any reversed variant
    mpl.colormaps.register(cmap.reversed(), name=f"{name}_r")
