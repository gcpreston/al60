from typing import Hashable, Tuple

# Ideally, a Node would be defined as the name of a node in a specified graph.
# However, since Python's type hints are static, this type of definition is not
# possible. Instead, this idea is simulated by defining a Node and an Edge as
# any possible node or edge in some graph, and it is left up to each method
# to check if the Node or Edge is valid for the relevant graph.

Node = Hashable
Edge = Tuple[Node, Node]
