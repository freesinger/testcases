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
                i, j, dis = line.strip().split()
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

    def threshold(self, dist, max_id):
        '''
        :rtype: factor value makes H smallest
        '''
        entro = 10.0
        # 0.02139999999999999 7.203581306901208
        # 0.02149999999999999 7.203577254067677
        # 0.02159999999999999 7.203577734107922
        scape = np.arange(0.021+1e-4, 0.022, 1e-4)
        for factor in scape:
            value = self.entropy(dist, max_id, factor)
            # print(factor, value)
            if value and value < entro:
                entro, thresh = value, factor
        thresh = 3 * thresh / pow(2, 0.5)
        # print('current: ', entro, thresh)
        # current:  7.203577254067677 0.04560838738653229
        return thresh
    
    def CutOff(self, distance, max_id, threshold):
        '''
        :rtype: list with Cut-off kernel values by desc
        '''
        cut_off = dict()
        for i in range(1, max_id + 1):
            tmp = 0
            for j in range(1, max_id + 1):
                gap = distance[(i, j)] - threshold
                tmp += 0 if gap >= 0 else 1
            cut_off[i] = tmp
        sorted_cutoff = sorted(cut_off.items(), key=lambda k:k[1], reverse=True)
        return sorted_cutoff
            
    def Guasse(self, distance, max_id, threshold):
        '''
        :rtype: dict with Gaussian kernel values by desc
        '''
        guasse = dict()
        for i in range(1, max_id + 1):
            tmp = 0
            for j in range(1, max_id + 1):
                tmp += math.exp(-pow((distance[(i, j)] / threshold), 2))
            guasse[i] = tmp
        sorted_guasse = sorted(guasse.items(), key=lambda k:k[1], reverse=True)
        return sorted_guasse

    def min_distance(self, distance, srt_dens, maxid):
        '''
        :srt_dens: desc sorted list with density values
        :rtype: min distance dict
        '''
        min_distance = dict()
        h_dens = srt_dens[0][0]
        max_dist = -1
        for i in range(1, maxid + 1):
            max_dist = max(distance[(h_dens, i)], max_dist)
        min_distance[h_dens] = max_dist
        
        for j in range(1, len(srt_dens)):
            min_dist = 1
            for k in srt_dens[0:j]:
                current_dist = distance[(srt_dens[j][0], k[0])]
                min_dist = min(current_dist, min_dist)
            min_distance[srt_dens[j][0]] = min_dist
        return min_distance

    def make_pair(self, srt_dens, min_dist, maxid):
        '''
        :rtype: dict with {point: [desity, min dist]}
        '''
        # convert list to dict
        pair_dict = dict()
        dens_dict = dict()
        for elem in srt_dens:
            dens_dict[elem[0]] = elem[1]
        if len(dens_dict) == maxid:
            for key in dens_dict.keys():
                pair_dict[key] = [dens_dict[key], min_dist[key]]
        else:
            return print('missing %d value', maxid - dens_dict)
        return pair_dict
            

def main():
    solution = ProcessData()
    dist, maxid = solution.data_process(GIVEN_DATA)
    threshold = solution.threshold(dist, maxid)
    cutoff = solution.CutOff(dist, maxid, threshold)
    min_dist = solution.min_distance(dist, cutoff, maxid)
    pair_info = solution.make_pair(cutoff, min_dist, maxid)
    print(pair_info)
    # gauss = solution.Guasse(dist, maxid, threshold)


if __name__ == '__main__':
    main()
    