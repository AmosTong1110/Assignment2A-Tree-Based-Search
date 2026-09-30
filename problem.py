"""Input data for the tree-based search algorithms."""


class Problem:
    """The graph and start/goal data for one route-finding problem."""

    def __init__(self, coordinates, edges, origin, destinations):
        self.coordinates = coordinates
        self.edges = edges
        self.origin = origin
        self.destinations = destinations


def load_problem(filename):
    """Read a problem file and return its parsed data."""
    sections = {"Nodes": [], "Edges": [], "Origin": [], "Destinations": []}
    current_section = None

    with open(filename, "r", encoding="utf-8") as input_file:
        for raw_line in input_file:
            line = raw_line.strip()
            if not line:
                continue

            if line in ("Nodes:", "Edges:", "Origin:", "Destinations:"):
                current_section = line[:-1]
            elif current_section is not None:
                sections[current_section].append(line)

    # Store each node ID with its (x, y) coordinates.
    coordinates = {}
    for line in sections["Nodes"]:
        node_text, coordinate_text = line.split(":", 1)
        x_text, y_text = coordinate_text.strip().strip("()").split(",")
        coordinates[int(node_text.strip())] = (int(x_text), int(y_text))

    # Store outgoing edges as (neighbour ID, cost), sorted by neighbour ID.
    edges = {}
    for line in sections["Edges"]:
        edge_text, cost_text = line.split(":", 1)
        from_text, to_text = edge_text.strip().strip("()").split(",")
        from_id = int(from_text)
        to_id = int(to_text)
        cost = int(cost_text.strip())
        edges.setdefault(from_id, []).append((to_id, cost))

    for neighbours in edges.values():
        neighbours.sort(key=lambda edge: edge[0])

    origin = int(sections["Origin"][0])
    destinations = sorted(
        int(destination.strip())
        for destination in sections["Destinations"][0].split(";")
        if destination.strip()
    )

    return Problem(coordinates, edges, origin, destinations)