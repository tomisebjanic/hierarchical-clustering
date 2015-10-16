import csv
import sys

__author__ = 'tomisebjanic'


def klaster():
    with open('eurovision-final.csv') as csvfile:
        csv_reader = csv.reader(csvfile)
        raw_data = [[row[i].strip().lower() for i in range(0, len(row))] for row in csv_reader]

    data_range = range(raw_data[0].index('albania'), raw_data[0].index('united kingdom'))
    data = [[raw_data[i][j] if i > 0 else [raw_data[i][j]] for j in data_range] for i in range(0, len(raw_data))]

    while(len(data[0])) > 1:
        min_manhattan = sys.maxsize
        column1, column2, column1_index, column2_index, min_avg_distances = None, None, None, None, []

        # Iteratively compare two columns
        for j in range(0, len(data[0]) - 1):
            for j2 in range(j+1, len(data[0])):
                distance, num_comparisons, average_distances = 0, 0, []

                # Calculate distance between columns
                for i in range(1, len(data)):
                    if data[i][j] != '' and data[i][j2] != '':
                        distance += abs(int(data[i][j]) - int(data[i][j2]))
                        average_distances.append((int(data[i][j]) + int(data[i][j2])) / 2)
                        num_comparisons += 1
                    else:
                        if data[i][j] != '':
                            average_distances.append(int(data[i][j]))
                        elif data[i][j2] != '':
                            average_distances.append(int(data[i][j2]))
                        else:
                            average_distances.append('')

                # Assign closest columns
                if 0 < num_comparisons and min_manhattan > distance/num_comparisons:
                    min_manhattan, column1, column2, column1_index, column2_index, min_avg_distances = distance/num_comparisons, data[0][j], data[0][j2], j, j2, average_distances

        # No more columns to compare
        if column1_index is None or column2_index is None:
            break

        # Merge columns
        data[0][column1_index] = [data[0][column1_index], data[0][column2_index]]
        del data[0][column2_index]

        for i in range(1, len(data)):
            data[i][column1_index] = min_avg_distances[i-1]
            del data[i][column2_index]

    return data[0][0]


def printDendrogram(T, sep=3):
    """Print dendrogram of a binary tree.  Each tree node is represented by a length-2 tuple."""

    def isPair(T):
        return type(T) == list and len(T) == 2

    def maxHeight(T):
        if isPair(T):
            h = max(maxHeight(T[0]), maxHeight(T[1]))
        else:
            h = len(str(T))
        return h + sep

    activeLevels = {}

    def traverse(T, h, isFirst):
        if isPair(T):
            traverse(T[0], h-sep, 1)
            s = [' ']*(h-sep)
            s.append('|')
        else:
            s = list(str(T))
            s.append(' ')

        while len(s) < h:
            s.append('-')

        if (isFirst >= 0):
            s.append('+')
            if isFirst:
                activeLevels[h] = 1
            else:
                del activeLevels[h]

        A = list(activeLevels)
        A.sort()
        for L in A:
            if len(s) < L:
                while len(s) < L:
                    s.append(' ')
                s.append('|')

        print (''.join(s))

        if isPair(T):
            traverse(T[1], h-sep, 0)

    traverse(T, maxHeight(T), -1)


printDendrogram(klaster())
