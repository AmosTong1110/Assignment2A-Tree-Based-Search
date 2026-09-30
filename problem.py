"""Input data for the tree-based search algorithms."""


class Problem:
    """The graph and start/goal data for one route-finding problem."""

    def __init__(self, coordinates, edges, origin, destinations):
        self.coordinates = coordinates
        self.edges = edges
        self.origin = origin
        self.destinations = destinations


def parse_number(text):
    """Parse whole numbers as ints and other numbers as floats."""
    number = float(text)
    return int(number) if number.is_integer() else number


def load_problem(filename):
    """Read a problem file and return its parsed data."""
    sections = {"Nodes": [], "Edges": [], "Origin": [], "Destinations": []}
    current_section = None

    with open(filename, "r", encoding="utf-8-sig") as input_file:
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
        coordinates[int(node_text.strip())] = (parse_number(x_text), parse_number(y_text))

    # Store outgoing edges as (neighbour ID, cost), sorted by neighbour ID.
    edges = {}
    for line in sections["Edges"]:
        edge_text, cost_text = line.split(":", 1)
        from_text, to_text = edge_text.strip().strip("()").split(",")
        from_id = int(from_text)
        to_id = int(to_text)
        if from_id not in coordinates or to_id not in coordinates:
            missing_id = from_id if from_id not in coordinates else to_id
            raise ValueError(f"Edge refers to unknown node ID: {missing_id}")
        cost = parse_number(cost_text.strip())
        edges.setdefault(from_id, []).append((to_id, cost))

    for neighbours in edges.values():
        neighbours.sort(key=lambda edge: edge[0])

    if not sections["Origin"]:
        raise ValueError("Origin section is missing or empty")
    if not sections["Destinations"]:
        raise ValueError("Destinations section is missing or empty")

    origin = int(sections["Origin"][0])
    if origin not in coordinates:
        raise ValueError(f"Origin node ID is not in Nodes section: {origin}")

    destinations = sorted(
        int(destination.strip())
        for destination_line in sections["Destinations"]
        for destination in destination_line.split(";")
        if destination.strip()
    )
    if not destinations:
        raise ValueError("Destinations section is missing or empty")
    for destination in destinations:
        if destination not in coordinates:
            raise ValueError(
                f"Destination node ID is not in Nodes section: {destination}"
            )

    return Problem(coordinates, edges, origin, destinations)