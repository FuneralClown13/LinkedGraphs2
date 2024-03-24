from itertools import count


class Vertex:
    vertex_id = count(0)

    def __init__(self):
        self._id = next(self.vertex_id)
        self._links = []

    @property
    def links(self):
        return self._links

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return self._id == other._id


class Link:
    def __init__(self, v1: Vertex, v2: Vertex, dist=1):
        self._v1 = v1
        self._v2 = v2
        self.dist = dist

    def __eq__(self, vertex):
        if isinstance(vertex, Link):
            vertex = (vertex._v1, vertex._v2)
        return self._v1 in vertex and self._v2 in vertex


class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v):
        """добавление новой вершины v в список _vertex (если она там отсутствует)"""
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link: Link):
        """добавление новой связи link в список _links (если объект link с указанными вершинами в списке отсутствует)"""
        if link not in self._links:
            self._links.append(link)
            self.add_vertex(link._v1)
            self.add_vertex(link._v2)
            link._v1.links.append(link)
            link._v2.links.append(link)


    def create_graph(self):
        graph = {}
        for v in self._vertex:
            neighbors = []
            for link in v.links:
                if v == link._v1:
                    neighbors.append((link._v2, link))
                if v == link._v2:
                    neighbors.append((link._v1, link))
            graph[v] = {p: link for p, link in neighbors}
        return graph

    def get_routs(self, start, fin, graph):
        inf = float('inf')
        is_visited = set()
        distance = {v: graph[start][v].dist if v in graph[start].keys() else inf for v in self._vertex}
        routs = {v: start if v in graph[start].keys() else None for v in self._vertex}

        queue = [*graph[start].keys()]
        while queue:
            node = queue.pop(0)
            if node is fin:
                break
            if node in is_visited:
                continue
            is_visited.add(node)
            dist = distance[node]
            neighbors = graph[node]
            for n in neighbors.keys():
                new_dist = dist + neighbors[n].dist
                if distance[n] > new_dist:
                    distance[n] = new_dist
                    routs[n] = node
                queue.append(n)
        return routs

    @staticmethod
    def get_path(start, fin, routs):
        path = [fin]
        while path[-1] != start:
            path.append(routs[path[-1]])
        return path[::-1]

    def get_links(self, path):
        pathes = list(zip(path, path[1::]))
        return list(filter(lambda l: l in pathes, self._links))

    def find_path(self, start: Vertex, fin: Vertex):
        """поиск кратчайшего маршрута из вершины start_v в вершину stop_v."""
        graph = self.create_graph()
        routs = self.get_routs(start, fin, graph)
        path_by_vertex = self.get_path(start, fin, routs)
        path_by_links = self.get_links(path_by_vertex)

        return path_by_vertex, path_by_links



