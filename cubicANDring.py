import math

import matplotlib.pyplot as plt
import networkx as nx


def create_graphs():
    """Create the cube graph A and Wagner graph B."""

    graph_a = nx.Graph()
    graph_b = nx.Graph()

    graph_a.add_nodes_from(range(1, 9))
    graph_b.add_nodes_from(range(1, 9))

    # Graph A: two squares joined at corresponding corners.
    graph_a.add_edges_from([
        # Outer square
        (1, 2), (2, 3), (3, 4), (4, 1),

        # Inner square
        (5, 6), (6, 7), (7, 8), (8, 5),

        # Connections between the squares
        (1, 5), (2, 6), (3, 7), (4, 8),
    ])

    # Graph B: an eight-vertex ring with opposite vertices joined.
    graph_b.add_edges_from([
        # Ring
        (1, 2), (2, 3), (3, 4), (4, 5),
        (5, 6), (6, 7), (7, 8), (8, 1),

        # Connections across the ring
        (1, 5), (2, 6), (3, 7), (4, 8),
    ])

    return graph_a, graph_b


def create_positions():
    """Choose fixed drawing positions for both graphs."""

    # Each vertex maps to an (x, y) coordinate.
    positions_a = {
        1: (-1, 1),
        2: (1, 1),
        3: (1, -1),
        4: (-1, -1),
        5: (-0.4, 0.4),
        6: (0.4, 0.4),
        7: (0.4, -0.4),
        8: (-0.4, -0.4),
    }

    # Place vertices equally around a circle, starting at the top.
    positions_b = {}

    for index, node in enumerate(range(1, 9)):
        angle = math.pi / 2 - index * (2 * math.pi / 8)

        positions_b[node] = (
            math.cos(angle),
            math.sin(angle),
        )

    return positions_a, positions_b


def show_graphs(graph_a, graph_b, positions_a, positions_b):
    """Draw both graphs with the same initial node colour."""

    figure, axes = plt.subplots(1, 2, figsize=(11, 6))

    panels = [
        (graph_a, positions_a, "Graph A: Cube", axes[0]),
        (graph_b, positions_b, "Graph B: Wagner", axes[1]),
    ]

    for graph, positions, title, axis in panels:
        nx.draw_networkx(
            graph,
            pos=positions,
            ax=axis,
            with_labels=True,
            node_color="skyblue",
            node_size=850,
            edge_color="gray",
            width=2,
            font_size=13,
            font_weight="bold",
            edgecolors="black",
        )

        axis.set_title(title)
        axis.set_aspect("equal")
        axis.set_xlim(-1.3, 1.3)
        axis.set_ylim(-1.3, 1.3)
        axis.axis("off")

    figure.suptitle(
        "Both graphs: 8 vertices, 12 edges, 3 neighbours per vertex",
        fontsize=14,
    )

    figure.text(
        0.5,
        0.04,
        "Edge crossings are not vertices unless a labelled circle is shown.",
        ha="center",
        fontsize=10,
    )

    figure.tight_layout(rect=(0, 0.08, 1, 0.93))
    plt.show()


# These objects can be imported by our animation file later.
graph_a, graph_b = create_graphs()
positions_a, positions_b = create_positions()


if __name__ == "__main__":
    # This performs an actual isomorphism test, separate from 1-WL.
    print("Are the graphs isomorphic?",
          nx.is_isomorphic(graph_a, graph_b))

    show_graphs(graph_a, graph_b, positions_a, positions_b)