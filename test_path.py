import copy
from itertools import chain
from numpy import Inf
import json


class Graph:
    def __init__(self, matrix):
        self.node_coordinates = self._get_node_coordinates(matrix)
        self.graph = self._get_graph(matrix)

    def _get_node_coordinates(self, matrix):
        '''
        Функция возвращает координаты для каждой клетки
        :param matrix: карта территории со стоимостью прохождения клетки
        :return: координаты всех клеток (x, y)
        '''
        number_of_cells = len(matrix) * len(matrix[0])
        cell_coordinates = [(j, i) for i in range(len(matrix)) for j in range(len(matrix[0]))]
        cell_coordinates = {x: y for x, y in zip(range(number_of_cells), cell_coordinates)}
        return cell_coordinates

    def _is_neighbour(self, coord: dict, key1: int, key2: int):
        '''
        Вычисляем по координатам соседние клетки, в которые
        можем ходить.
        :param coord: координаты всех клеток
        :param key1: клетка на которой находимся
        :param key2: предполагаемый сосед
        :return: True - можем ходить в клетку, False - не можем
        '''
        condition_1 = ((coord[key1][0] + 1 == coord[key2][0] and
                        coord[key1][1] == coord[key2][1]) or (
                               coord[key1][1] + 1 == coord[key2][1] and
                               coord[key1][0] == coord[key2][0]))
        condition_2 = ((coord[key1][0] - 1 == coord[key2][0] and
                        coord[key1][1] == coord[key2][1]) or (
                               coord[key1][1] - 1 == coord[key2][1] and
                               coord[key1][0] == coord[key2][0]))
        condition_3 = True if key2 != 0 else False
        if (condition_1 or condition_2) and condition_3:
            return True
        else:
            return False

    @staticmethod
    def _add_edge_weight(graph, board: list):
        '''
        Добавляем стоимость перехода к каждой вершине
        в граф
        :param graph:
        :param board:
        :return:
        '''
        some = list(chain.from_iterable(board))
        for vertex, neighbours in graph.items():
            for idx in range(len(neighbours)):
                graph[vertex][idx] = (graph[vertex][idx], some[graph[vertex][idx]])
        return graph

    def _get_graph(self, matrix):
        graph = {}
        for key, value in self.node_coordinates.items():
            graph[key] = None
            connected_vertices = list()
            for key_2 in self.node_coordinates:
                if key != key_2:
                    if self._is_neighbour(self.node_coordinates, key, key_2):
                        connected_vertices.append(key_2)
            graph[key] = connected_vertices
        graph = self._add_edge_weight(graph, matrix)
        return graph


def algorithm_dijkstra(graph, root: int = 0):
    n = len(graph)
    dist = [Inf for _ in range(n)]
    dist[root] = 0
    visited = [False for _ in range(n)]
    best_way = {}

    for _ in range(n):
        u = -1
        for i in range(n):
            if not visited[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if dist[u] == Inf:
            break
        visited[u] = True
        for v, l in graph[u]:
            if dist[u] + l < dist[v]:
                dist[v] = dist[u] + l
                if best_way.get(u):
                    prev_way = copy.deepcopy(best_way[u])
                    prev_way.append(v)
                    best_way[v] = prev_way
                else:
                    best_way[v] = [u, v]
    return dist, best_way


def target_cell_number(graph: Graph, target_cell: tuple) -> int:
    value = None
    for coordinate in graph.node_coordinates:
        if graph.node_coordinates[coordinate] == target_cell:
            value = coordinate
    return value


def print_result(graph: Graph, cell: int, best_dists: list, best_ways: dict) -> None:
    path = [graph.node_coordinates[i] for i in best_ways[cell]]
    print(f'Путь: {path}')
    cost = best_dists[cell]
    print(f'Стоимость: {cost}')
    picture = [['o' for j in range(len(i))] for i in board]
    for i in path:
        picture[i[1]][i[0]] = 'x'
    print(*picture, sep='\n')


if __name__ == '__main__':
    with open('input.json', 'r') as read_file:
        data = json.load(read_file)
        board = data.get('board')
        target = tuple(data.get('target'))

    g = Graph(board)
    target_cell = target_cell_number(g, target)
    best_dist, best_way = algorithm_dijkstra(g.graph)
    print_result(g, target_cell, best_dist, best_way)
