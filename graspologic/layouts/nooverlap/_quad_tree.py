# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import csv
import math

from ._smart_quad_node import _SmartQuadNode, find_extent


class _QuadTree:
    # used to hold objects that have x, y, and mass property
    # nodes = []

    def __init__(self, nodes, max_nodes_per_quad):
        self.nodes = nodes
        extent = find_extent(nodes)
        self.root = _SmartQuadNode(nodes, 0, extent, max_nodes_per_quad, None)

    def get_node_stats(self, max_level=10):
        stats = []
        self.root.get_stats_for_quad(max_level, stats)
        return stats

    def get_node_stats_header(self):
        return self.root._node_stats_header()


    def get_quad_leaf_density_list(self):
        density_list = self.root.get_leaf_density_list()
        return sorted(density_list, reverse=True)

    def layout_graph(self):
        return self.layout_dense_first()

    def tree_stats(self):
        results = self.root.quad_stats()
        return list(results) + [
            results[3] / len(self.nodes),
            results[4] / len(self.nodes),
            self.root.sq_ratio,
        ]

    def collect_nodes(self):
        ret_val = []
        self.root.collect_nodes(ret_val)
        return ret_val

    def get_tree_node_bounds(self):
        ret_val = []
        self.root.boxes_by_level(ret_val)
        return ret_val

    def count_overlaps(self):
        return self.root.num_overlapping()

    def count_overlaps_across_quads(self):
        return self.root.num_overlapping_across_quads(self.root.nodes)

    def layout_dense_first(self, first_color=None):
        den_list = list(self.get_quad_leaf_density_list())
        print (f"total quad nodes: {len(den_list)}")
        skipped = 0
        for cell_density, density_ratio, cell_count, qn in den_list:
            print ('cell density', cell_density, 'cir_density', density_ratio, 'cell_count', cell_count, "nodes: ", qn.number_of_nodes(), "depth: ", qn.depth, "max node size", qn.max_size)
            skipped += qn.layout_quad()
        print (f"skipped: {skipped} quad nodes")
        return self.nodes
