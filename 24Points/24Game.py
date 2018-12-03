"""
Two solutions for 24Game
"""
import itertools
import time

TargetResult = 24
CardNumber = 4
number = []     # Store numbers
Result = []     # type: string
pair = {}       # (num1, num2): []

class Solution(object):
    """
    Recursive Solution
    """
    def GameAnalysis(self, num):
        if num == 1:
            if number[0] == TargetResult:
                return True
            else:
                return False
        
        for i in range(num):
            for j in range(i + 1, num):
                a, b = number[i], number[j]
                number[j] = number[num - 1]
                str_a, str_b = Result[i], Result[j]
                Result[j] = Result[num - 1]
                # a + b (b + a)
                Result[i] = '(' + str_a + '+' + str_b + ')'
                number[i] = a + b
                if self.GameAnalysis(num - 1):
                    return True
                # a - b
                Result[i] = '(' + str_a + '-' + str_b + ')'
                number[i] = a - b
                if self.GameAnalysis(num - 1):
                    return True
                # b - a
                Result[i] = '(' + str_b + '-' + str_a + ')'
                number[i] = b - a
                if self.GameAnalysis(num - 1):
                    return True
                # a * b (b * a)
                Result[i] = '(' + str_a + '*' + str_b + ')'
                number[i] = a * b
                if self.GameAnalysis(num - 1):
                    return True
                # a / b
                if b != 0:
                    Result[i] = '(' + str_a + '/' + str_b + ')'
                    number[i] = a / b
                    if self.GameAnalysis(num - 1):
                        return True
                # b / a
                if a != 0:
                    Result[i] = '(' + str_b + '/' + str_a + ')'
                    number[i] = b / a
                    if self.GameAnalysis(num - 1):
                        return True
                
                number[i] = a
                number[j] = b
                Result[i] = str_a
                Result[j] = str_b
                
        return False

    """
    Dynamic program
    """
    def PairCalculate(self, curlist):
        # len(curlist) = 2
        result = []
        a, b = curlist[0], curlist[1]
        result.append(a + b)
        result.append(a - b)
        result.append(b - a)
        result.append(a * b)
        if b != 0:
            result.append(a / b)
        if a != 0:
            result.append(b / a)
        return result

    def Calculate(self, llist, rlist):
        #if rlist is None:
            # return llist
        result = []
        for a in llist:
            for b in rlist:
                result.append(a + b)
                result.append(a - b)
                result.append(b - a)
                result.append(a * b)
                if b != 0:
                    result.append(a / b)
                if a != 0:
                    result.append(b / a)
        return result

    def FindPair(self, curlist):
        tmp = tuple(curlist)
        if pair.__contains__(tmp):
            return pair[tmp]
        else:
            pair[tmp] = self.PairCalculate(curlist)
            return pair[tmp]

    def PartiAnalysis(self, curlist):
        if len(curlist) == 1:
            return curlist
        elif len(curlist) == 2:
            return self.FindPair(curlist)
        elif len(curlist) == 3:
            t = []
            for num in curlist:
                temp = curlist.copy()
                single = [num]
                singleRes = self.PartiAnalysis(single)
                temp.remove(num)
                pairRes = self.PartiAnalysis(temp)
                tripRes = self.Calculate(single, pairRes)
                t.extend(tripRes)
            return t

    def OptimizedAnalysis(self, numberlist):
        comb = list(itertools.permutations(numberlist))
        for c in comb:
            flist = list(i for i in c)
            temp = flist.copy()
            single = [flist[0]]
            temp.remove(flist[0])
            trip = temp
            r = self.Calculate(self.PartiAnalysis(single), self.PartiAnalysis(trip))
            if TargetResult in r:
                return True
            # temp = flist.copy()
            fpair = [flist[0], flist[1]]
            spair = [flist[2], flist[3]]
            r.extend(self.Calculate(self.PartiAnalysis(fpair), self.PartiAnalysis(spair)))
            if TargetResult in r:
                return True
            
            temp = flist.copy()
            single = [flist[-1]]
            temp.remove(flist[-1])
            trip = temp
            r.extend(self.Calculate(self.PartiAnalysis(single), self.PartiAnalysis(trip)))
            if TargetResult in r:
                return True
        return False

def main():
    # append() will be [[]]
    Result.extend(input("Input %d number:" % CardNumber).split(','))
    for n in Result:
        number.append(int(n))
    
    Game = Solution()
    # Recursive
    S_Atime = time.time()
    if Game.GameAnalysis(CardNumber):
        print("Solution A Success.")
        print("Excute time:", time.time() - S_Atime, 's')
    else:
        print("Solution A Fail.")
    # Dynamic Program
    S_Btime = time.time()
    if Game.OptimizedAnalysis(number):
        print("Solution B Success.")
        print("Excute time:", time.time() - S_Btime, 's')
        print(Result[0])
    else:
        print("Solution B Fail.")
    
if __name__ == '__main__':
    main()