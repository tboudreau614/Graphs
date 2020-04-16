"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Vertex:
	def __init__(self, vid):
		self.vid = vid

	def __hash__(self):
		return hash(self.vid)

	def __eq__(self, value):
		return hash(self) == hash(value)


class Graph:

	"""Represent a graph as a dictionary of vertices mapping labels to edges."""
	def __init__(self):
		self.vertices = {}

	def add_vertex(self, vertex_id):

	    self.vertices[vertex_id] = set()

	def add_edge(self, v1, v2):

		v1 = Vertex(v1)
		v2 = Vertex(v2)
		self.vertices[v1].add(v2)

	def get_neighbors(self, vertex_id):

		vertex = Vertex(vertex_id)
		return {v.vid for v in self.vertices[vertex]}

	def bft(self, starting_vertex):

		visited = set()
		current_vertices = {Vertex(starting_vertex)}
		new_vertices = set()
		while current_vertices:
			for vertex in current_vertices:
				new_vertices.update(self.vertices[vertex])
				visited.add(vertex)
				print(vertex.vid)
			current_vertices = new_vertices - visited
			new_vertices = set()

	def dft(self, starting_vertex):

		visited = set()
		to_visit = Stack()
		to_visit.push(Vertex(starting_vertex))
		while to_visit.size():
			current_vertex = to_visit.pop()
			if current_vertex in visited:
				continue
			visited.add(current_vertex)
			print(current_vertex.vid)
			for vertex in self.vertices[current_vertex]:
				to_visit.push(vertex)

	def dft_recursive(self, starting_vertex, visited=None):

		if not isinstance(starting_vertex, Vertex):
			starting_vertex = Vertex(starting_vertex)
		if visited is None:
			visited = set()
		visited.add(starting_vertex)
		print(starting_vertex.vid)
		for vertex in self.vertices[starting_vertex] - visited:
			self.dft_recursive(vertex, visited=visited)

	def bfs(self, starting_vertex, destination_vertex):

		if not isinstance(starting_vertex, Vertex):
			starting_vertex = Vertex(starting_vertex)
		if not isinstance(destination_vertex, Vertex):
			destination_vertex = Vertex(destination_vertex)

		visited = set()
		to_visit = Queue()
		to_visit.enqueue([starting_vertex])
		while to_visit.size():
			current_path = to_visit.dequeue()
			if current_path[-1] == destination_vertex:
				return [v.vid for v in current_path]
			elif current_path[-1] in visited:
				continue
			else:
				visited.add(current_path[-1])
				for vertex in self.vertices[current_path[-1]]:
					to_visit.enqueue(current_path + [vertex])

	def dfs(self, starting_vertex, destination_vertex):

		if not isinstance(starting_vertex, Vertex):
			starting_vertex = Vertex(starting_vertex)
		if not isinstance(destination_vertex, Vertex):
			destination_vertex = Vertex(destination_vertex)

		visited = set()
		to_visit = Stack()
		to_visit.push([starting_vertex])
		while to_visit.size():
			current_path = to_visit.pop()
			if current_path[-1] == destination_vertex:
				return [v.vid for v in current_path]
			elif current_path[-1] in visited:
				continue
			else:
				visited.add(current_path[-1])
				for vertex in self.vertices[current_path[-1]]:
					to_visit.push(current_path + [vertex])

	def dfs_recursive(self, starting_vertex, destination_vertex):
		return [
			v.vid for v in
			self._dfs_recursive_v(starting_vertex, destination_vertex)
		]

	def _dfs_recursive_v(self, starting_vertex, destination_vertex, visited=None):

		if visited is None:
			visited = set()
		if not isinstance(starting_vertex, Vertex):
			starting_vertex = Vertex(starting_vertex)
		if not isinstance(destination_vertex, Vertex):
			destination_vertex = Vertex(destination_vertex)

		path = [starting_vertex]
		visited.add(starting_vertex)
		for vertex in self.vertices[starting_vertex]:
			if vertex == destination_vertex:
				return path + [destination_vertex]
			elif vertex in visited:
				continue
			else:
				new_path = self._dfs_recursive_v(vertex, destination_vertex, visited=visited)
				if new_path is not None:
					return path + new_path
		return None

	def _vertices_ids(self):
		return {key.vid: {v.vid for v in val} for key, val in self.vertices.items()}


if __name__ == '__main__':
	graph = Graph()  # Instantiate your graph
	# https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
	graph.add_vertex(1)
	graph.add_vertex(2)
	graph.add_vertex(3)
	graph.add_vertex(4)
	graph.add_vertex(5)
	graph.add_vertex(6)
	graph.add_vertex(7)
	graph.add_edge(5, 3)
	graph.add_edge(6, 3)
	graph.add_edge(7, 1)
	graph.add_edge(4, 7)
	graph.add_edge(1, 2)
	graph.add_edge(7, 6)
	graph.add_edge(2, 4)
	graph.add_edge(3, 5)
	graph.add_edge(2, 3)
	graph.add_edge(4, 6)

	'''
	Should print:
		{1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
	'''
	print(graph._vertices_ids())

	'''
	Valid BFT paths:
		1, 2, 3, 4, 5, 6, 7
		1, 2, 3, 4, 5, 7, 6
		1, 2, 3, 4, 6, 7, 5
		1, 2, 3, 4, 6, 5, 7
		1, 2, 3, 4, 7, 6, 5
		1, 2, 3, 4, 7, 5, 6
		1, 2, 4, 3, 5, 6, 7
		1, 2, 4, 3, 5, 7, 6
		1, 2, 4, 3, 6, 7, 5
		1, 2, 4, 3, 6, 5, 7
		1, 2, 4, 3, 7, 6, 5
		1, 2, 4, 3, 7, 5, 6
	'''
	graph.bft(1)

	'''
	Valid DFT paths:
		1, 2, 3, 5, 4, 6, 7
		1, 2, 3, 5, 4, 7, 6
		1, 2, 4, 7, 6, 3, 5
		1, 2, 4, 6, 3, 5, 7
	'''
	graph.dft(1)
	graph.dft_recursive(1)

	'''
	Valid BFS path:
		[1, 2, 4, 6]
	'''
	print(graph.bfs(1, 6))

	'''
	Valid DFS paths:
		[1, 2, 4, 6]
		[1, 2, 4, 7, 6]
	'''
	print(graph.dfs(1, 6))
	print(graph.dfs_recursive(1, 6))