import csv
from itertools import combinations
import sys


__author__ = 'tomisebjanic'


class HierarchicalClustering:

    def __init__(self, file, linkage, distance):
        with open(file, encoding="latin1", errors='ignore') as csvfile:
            csv_reader = csv.reader(csvfile)
            raw_data = [[row[i].strip().lower() for i in range(0, len(row))] for row in csv_reader]
        data_range = range(raw_data[0].index('albania'), raw_data[0].index('united kingdom') + 1)

        self.data = [[float(raw_data[i][j]) if raw_data[i][j] != '' else '' for j in data_range] for i in range(1, len(raw_data))]
        self.clusters = [[raw_data[0][j]] for j in data_range]
        self.linkage = linkage
        self.distance_method = distance
        self.data = [list(i) for i in zip(*self.data)]  # transpose data matrix
        self.print_separator = 7
        self.active_levels = {}

    def euclidean_distance(self, row1, row2):
        distance = [(x-y)**2 for x, y in zip(self.data[row1], self.data[row2]) if x != '' and y != '']
        return sum(distance)**0.5 / len(distance) if len(distance) != 0 else None

    def manhattan_distance(self, row1, row2):
        distance = [abs(x-y) for x, y in zip(self.data[row1], self.data[row2]) if x != '' and y != '']
        return sum(distance) / len(distance) if len(distance) != 0 else None

    def cluster_distances(self, cl1, cl2):
        return self.single_linkage(cl1, cl2) if self.linkage == 'min' else self.complete_linkage(cl1, cl2) if self.linkage == 'max' else self.average_linkage(cl1, cl2)

    def single_linkage(self, row1, row2):
        return [min(self.data[row1][j], self.data[row2][j]) if self.data[row1][j] != '' and self.data[row2][j] != '' else self.data[row1][j] if self.data[row1][j] != '' else self.data[row2][j] if self.data[row2][j] != '' else '' for j in range(len(self.data[row1]))]

    def complete_linkage(self, row1, row2):
        return [max(self.data[row1][j], self.data[row2][j]) if self.data[row1][j] != '' and self.data[row2][j] != '' else self.data[row1][j] if self.data[row1][j] != '' else self.data[row2][j] if self.data[row2][j] != '' else '' for j in range(len(self.data[row1]))]

    def average_linkage(self, row1, row2):
        return [(self.data[row1][j] + self.data[row2][j])/2 if self.data[row1][j] != '' and self.data[row2][j] != '' else self.data[row1][j] if self.data[row1][j] != '' else self.data[row2][j] if self.data[row2][j] != '' else '' for j in range(len(self.data[row1]))]

    def do_clustering(self):
        while len(self.clusters) > 1:
            cluster1, cluster2, min_distance = None, None, sys.maxsize  # get two closest clusters
            for c in combinations(range(len(self.clusters)-1), 2):
                curr_dist = self.euclidean_distance(c[0], c[1]) if self.distance_method == 'euc' else self.manhattan_distance(c[0], c[1])
                if curr_dist is not None and curr_dist < min_distance:
                    cluster1, cluster2, min_distance = c[0], c[1], curr_dist

            if cluster1 is None and cluster2 is None:   # there is only one cluster remaining --> stop the loop
                break

            # print("merged\t", self.clusters[cluster1], self.clusters[cluster2])
            new_dist = self.cluster_distances(cluster1, cluster2)   # calculate new distance
            self.clusters.append([self.clusters[cluster1], self.clusters[cluster2]])    # append new cluster and delete old ones
            self.data.append(new_dist)
            if cluster1 < cluster2:
                del self.clusters[cluster1]
                del self.clusters[cluster2-1]
                del self.data[cluster1]
                del self.data[cluster2-1]
            else:
                del self.clusters[cluster2]
                del self.clusters[cluster1-1]
                del self.data[cluster2]
                del self.data[cluster1-1]

        return self.clusters

    def max_height(self, tree):
        return max(self.max_height(tree[0]), self.max_height(tree[1])) + self.print_separator if len(tree) == 2 else self.print_separator + len(str(tree))

    def print_dendrogram(self, tree, height):
        if len(tree) <= 1:
            print(''.join(list(str(tree[0]).upper()) + [' '] + ['-']*(height-len(tree[0])-1) + ['+']))
        else:
            self.print_dendrogram(tree[0], height-self.print_separator)
            print(''.join([' ']*(height-self.print_separator) + ['|'] + ['-']*(height-(height-self.print_separator+1)) +['+']))
            self.print_dendrogram(tree[1], height-self.print_separator)

    def main(self):
        clusters = self.do_clustering()
        self.print_dendrogram(clusters, self.max_height(self.clusters))

""" Uncomment one of the following constructors """
# hc = HierarchicalClustering('eurovision-final.csv', 'min', 'euc')
# hc = HierarchicalClustering('eurovision-final.csv', 'min', 'man')
# hc = HierarchicalClustering('eurovision-final.csv', 'avg', 'euc')
# hc = HierarchicalClustering('eurovision-final.csv', 'avg', 'man')
# hc = HierarchicalClustering('eurovision-final.csv', 'max', 'euc')
hc = HierarchicalClustering('eurovision-final.csv', 'max', 'man')
hc.main()
