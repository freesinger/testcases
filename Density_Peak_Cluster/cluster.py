import math
import numpy as np
import matplotlib as plt

GIVEN_DATA = './data/example_distances.dat'

class ProcessData(object):
    def data_process(self, folder):
        '''
        :folder: data file path
        :rtype: dict pair distance
        '''
        distance = dict()
        max_pt = 0
        with open(folder, 'r') as data:
            for line in data:
                i, j, dis = line.split()
                i, j, dis = int(i), int(j), float(dis)
                distance[(i, j)] = dis
                distance[(j, i)] = dis
                max_pt = max(i, j, max_pt)
            for num in range(1, max_pt + 1):
                distance[(num, num)] = 0
        return distance, max_pt

    def entropy(self, distance, maxid, factor):
        '''
        :distance: dict with pair: dist
        :factor: impact factor
        :maxid: max elem number
        :rtype: entropy H in data field
        '''
        potential = dict()
        for i in range(1, maxid + 1):
            tmp = 0
            for j in range(1, maxid + 1):
                tmp += math.exp(-pow(distance[(i, j)] / factor, 2))
            potential[i] = tmp
        z = sum(potential.values())
        H = 0
        for i in range(1, maxid + 1):
            x = potential[i] / z
            H += x * math.log(x)
        return -H

    def threshold(self, folder):
        '''
        :folder: data file path 
        :rtype: factor value makes H smallest
        '''
        dist, maxid = self.data_process(folder)
        entro = 10.0
        # 0.02139999999999999 7.203581306901208
        # 0.02149999999999999 7.203577254067677
        # 0.02159999999999999 7.203577734107922
        scape = np.arange(0.021+1e-4, 0.022, 1e-4)
        for factor in scape:
            value = self.entropy(dist, maxid, factor)
            # print(factor, value)
            if value and value < entro:
                entro, thresh = value, factor
        thresh = 3 * thresh / pow(2, 0.5)
        # print('current: ', entro, thresh)
        # current:  7.203577254067677 0.04560838738653229
        return thresh

def main():
    solution = ProcessData()
    shreshold = solution.threshold(GIVEN_DATA)
    print(shreshold)

if __name__ == '__main__':
    main()
    