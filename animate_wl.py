import tkinter as tk
from collections import Counter

import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from wl_algorithm import compare_1wl
from cubicANDring import (
    graph_a,
    graph_b,
    positions_a,
    positions_b,
)


# Run our actual 1-WL implementation.
distinguished, history = compare_1wl(graph_a, graph_b)

# Separate, exact isomorphism check.
isomorphic = nx.is_isomorphic(graph_a, graph_b)

graphs = [graph_a, graph_b]
positions = [positions_a, positions_b]
titles = ["Graph A: Cube", "Graph B: Wagner"]

# Create teaching frames from the algorithm's recorded rounds.
# Inspection frames use OLD colours; updates happen simultaneously.
frames = [("initial", 0, None)]

for round_number in range(1, len(history)):
    for node in graph_a:
        frames.append(("inspect", round_number, node))

    frames.append(("update", round_number, None))

frames.append(("result", len(history) - 1, None))


# ---------- Tkinter window ----------

root = tk.Tk()
root.title("1-WL: same colours, different graphs")
root.geometry("1100x800")

heading = tk.Label(root, font=("Arial", 16, "bold"))
heading.pack(pady=10)

figure = Figure(figsize=(10, 4.5), dpi=100)
axes = figure.subplots(1, 2)
figure.subplots_adjust(left=0.03, right=0.97, bottom=0.05, top=0.88)

canvas = FigureCanvasTkAgg(figure, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

details = tk.Label(
    root,
    font=("Consolas", 11),
    justify=tk.LEFT,
    anchor="w",
    wraplength=1000,
)
details.pack(fill=tk.X, padx=20, pady=8)

legend = tk.Label(
    root,
    text=(
        "Node fill = WL colour. "
        "Orange outline and edges = inspection highlight, not a WL colour."
    ),
    font=("Arial", 10),
)
legend.pack(pady=4)

controls = tk.Frame(root)
controls.pack(pady=10)

palette = [
    "skyblue", "lightgreen", "plum", "khaki",
    "salmon", "turquoise", "wheat", "lightpink",
]

frame_index = 0
playing = False
timer_id = None


def draw_frame():
    kind, round_number, selected = frames[frame_index]

    # Never use partially updated colours during an inspection.
    state_index = (
        round_number - 1 if kind == "inspect" else round_number
    )
    state = history[state_index]

    for index, axis in enumerate(axes):
        axis.clear()

        graph = graphs[index]
        node_order = list(graph)
        node_colours = [
            palette[state[index][node] % len(palette)]
            for node in node_order
        ]

        nx.draw_networkx(
            graph,
            pos=positions[index],
            ax=axis,
            nodelist=node_order,
            node_color=node_colours,
            node_size=800,
            edgecolors="black",
            edge_color="gray",
            width=2,
            font_size=12,
        )

        if selected is not None:
            # Highlight edges used to collect neighbour colours.
            nx.draw_networkx_edges(
                graph,
                pos=positions[index],
                ax=axis,
                edgelist=[
                    (selected, neighbour)
                    for neighbour in graph[selected]
                ],
                edge_color="darkorange",
                width=4,
            )

            # Outline the inspected vertex without changing its fill.
            x, y = positions[index][selected]
            axis.scatter(
                [x], [y],
                s=1100,
                facecolors="none",
                edgecolors="darkorange",
                linewidths=3,
                zorder=5,
            )

        counts = dict(sorted(Counter(state[index].values()).items()))
        axis.set_title(f"{titles[index]}\nColour counts: {counts}")
        axis.set_xlim(-1.3, 1.3)
        axis.set_ylim(-1.3, 1.3)
        axis.set_aspect("equal")
        axis.axis("off")

    if kind == "initial":
        heading.config(text="Round 0: every vertex starts with colour 0")
        message = "Both graphs begin with 8 vertices of the same colour."

    elif kind == "inspect":
        heading.config(
            text=f"Round {round_number}: inspect vertex {selected}"
        )

        lines = []

        for index, graph in enumerate(graphs):
            neighbours = sorted(graph[selected])
            neighbour_colours = sorted(
                state[index][node] for node in neighbours
            )
            signature = (
                state[index][selected],
                tuple(neighbour_colours),
            )

            lines.append(
                f"Graph {'AB'[index]}: neighbours {neighbours}; "
                f"signature = {signature}"
            )

        lines.append(
            "Collect signatures first. No node colours update yet."
        )
        message = "\n".join(lines)

    elif kind == "update":
        heading.config(
            text=f"Round {round_number}: apply all colour updates together"
        )
        message = (
            "Every vertex has the same signature: (0, (0, 0, 0)).\n"
            "Both graphs still have 8 vertices of colour 0.\n"
            "No colour class splits, so refinement is stable."
        )

    else:
        heading.config(text="Result: 1-WL cannot distinguish these graphs")
        message = (
            f"Distinguished by 1-WL? {distinguished}\n"
            f"Isomorphic, using a separate exact test? {isomorphic}\n"
            "A is bipartite. B has the odd cycle 1-2-3-4-5-1.\n"
            "Matching WL colours do not prove isomorphism."
        )

    details.config(text=message)
    canvas.draw_idle()


def pause():
    global playing, timer_id

    playing = False

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None


def tick():
    global frame_index, timer_id, playing

    timer_id = None

    if not playing:
        return

    if frame_index < len(frames) - 1:
        frame_index += 1
        draw_frame()

    if frame_index < len(frames) - 1:
        timer_id = root.after(1500, tick)
    else:
        playing = False


def play():
    global playing, timer_id

    if playing or frame_index == len(frames) - 1:
        return

    playing = True
    timer_id = root.after(1500, tick)


def next_step():
    global frame_index

    pause()
    frame_index = min(frame_index + 1, len(frames) - 1)
    draw_frame()


def restart():
    global frame_index

    pause()
    frame_index = 0
    draw_frame()


for text, command in [
    ("Play", play),
    ("Pause", pause),
    ("Next step", next_step),
    ("Restart", restart),
]:
    tk.Button(
        controls,
        text=text,
        command=command,
        width=12,
    ).pack(side=tk.LEFT, padx=5)


def close():
    pause()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)

draw_frame()
root.mainloop()