from collections import Counter


def compare_1wl(graph_a, graph_b):
    """Compare two simple, undirected graphs with no initial labels.

    Returns:
        distinguished: True means the graphs are not isomorphic.
        history: Node colours for both graphs at each round.
    """

    graphs = [graph_a, graph_b]

    # Initially, every vertex has colour 0.
    colours = [
        {node: 0 for node in graph}
        for graph in graphs
    ]

    history = [
        [node_colours.copy() for node_colours in colours]
    ]

    while True:
        # Compare how many vertices have each colour.
        counts_a = Counter(colours[0].values())
        counts_b = Counter(colours[1].values())

        if counts_a != counts_b:
            return True, history

        old_colour_count = len(
            set(colours[0].values()) | set(colours[1].values())
        )

        # Shared by BOTH graphs:
        # the same signature must receive the same colour.
        signature_to_colour = {}
        next_colours = []

        for graph, current_colours in zip(graphs, colours):
            updated = {}

            for node in graph:
                # Sorting ignores neighbour order but keeps duplicates.
                neighbour_colours = tuple(sorted(
                    current_colours[neighbour]
                    for neighbour in graph[node]
                ))

                signature = (
                    current_colours[node],
                    neighbour_colours,
                )

                if signature not in signature_to_colour:
                    signature_to_colour[signature] = len(
                        signature_to_colour
                    )

                updated[node] = signature_to_colour[signature]

            next_colours.append(updated)

        # Apply updates simultaneously after processing both graphs.
        colours = next_colours
        history.append([
            node_colours.copy() for node_colours in colours
        ])

        # Check whether this round distinguishes the graphs.
        if Counter(colours[0].values()) != Counter(colours[1].values()):
            return True, history

        # Old colours are part of each signature, so classes cannot merge.
        # No increase in colour classes means refinement is stable.
        if len(signature_to_colour) == old_colour_count:
            return False, history


# Graph A: cube graph
graph_a = {
    1: [2, 4, 5],
    2: [1, 3, 6],
    3: [2, 4, 7],
    4: [1, 3, 8],
    5: [1, 6, 8],
    6: [2, 5, 7],
    7: [3, 6, 8],
    8: [4, 5, 7],
}

# Graph B: Wagner graph
graph_b = {
    1: [2, 8, 5],
    2: [1, 3, 6],
    3: [2, 4, 7],
    4: [3, 5, 8],
    5: [4, 6, 1],
    6: [5, 7, 2],
    7: [6, 8, 3],
    8: [7, 1, 4],
}


if __name__ == "__main__":
    distinguished, history = compare_1wl(graph_a, graph_b)

    for round_number, (colours_a, colours_b) in enumerate(history):
        print(f"\nRound {round_number}")
        print("Graph A:", colours_a)
        print("Graph B:", colours_b)

    if distinguished:
        print("\n1-WL distinguishes the graphs: not isomorphic.")
    else:
        print("\n1-WL cannot distinguish the graphs.")
        print("This does NOT prove that they are isomorphic.")