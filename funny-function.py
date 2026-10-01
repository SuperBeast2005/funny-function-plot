import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# 1. Gitter (Grid) für den Bereich definieren
x = np.linspace(-4, 4, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)

# 2. Figur initialisieren (schwarzer Hintergrund)
fig, ax = plt.subplots(figsize=(12, 12), facecolor="black")
fig.patch.set_facecolor("black")

# Gesamtfenster und Zeichenfläche komplett schwarz machen
plt.rcParams["figure.facecolor"] = "black"
plt.rcParams["axes.facecolor"] = "black"
plt.rcParams["savefig.facecolor"] = "black"

# Vollbildmodus für das Fenster aktivieren
manager = plt.get_current_fig_manager()
try:
    manager.full_screen_toggle()
except AttributeError:
  try:
    manager.window.state("zoomed")
  except AttributeError:
    pass

try:
    manager.window.setBackgroundColor("black")
except AttributeError:
    pass

# Implizite Gleichung im Voraus berechnen (ohne Rotation)
term1 = (
    2.8
    * X**2
    * (
        X**2 * (2.5 * X**2 + Y**2 - 2)
        + 1.2 * Y**2 * (Y * (3 * Y - 0.75) - 6.0311)
        + 3.09
    )
)
term2 = 0.98 * Y**2 * ((Y**2 - 3.01) * Y**2 + 3) - 1.005
Z = term1 + term2

total_frames = 90


# 3. Animationsfunktion (erscheint von oben nach unten aus dem Nichts)
def animate(i):
  ax.clear()

  # Hintergrund schwarz und alle Achsen/Rahmen/Beschriftungen komplett ausschalten
  ax.set_facecolor("black")
  ax.axis("off")

  # Vergrößerte Limits, damit die Kanten nicht abgeschnitten werden
  ax.set_xlim(-1.2, 1.2)
  ax.set_ylim(-1.8, 1.8)
  ax.set_aspect("equal", adjustable="box")

  # Berechne die aktuelle Y-Schwelle (startet oben bei 1.4 und wandert nach unten zu -1.4)
  progress = i / (total_frames - 1)
  cutoff_y = 1.4 - progress * 2.8

  # Alles um 180° drehen
  X_rot = -X
  Y_rot = -Y

  # Maskiere alles unterhalb der aktuellen Linie, sodass es von oben nach unten eingeblendet wird
  Z_masked = np.where(Y_rot < cutoff_y, np.nan, Z)

  # Zeichne die Nulllinie im Hautton (#FFD1A4)
  cs = ax.contour(X_rot, Y_rot, Z_masked, levels=[0], colors="#FFD1A4", linewidths=6)
  return cs


# 4. Animation starten (90 Frames)
ani = animation.FuncAnimation(
    fig, animate, frames=total_frames, interval=25, blit=False, repeat=False
)

plt.show()