"""
Recursive Solution for 24Game
"""
TargetResult = 24
CardNumber = 4
number = []     # Store numbers
result = []     # type: string

def GameAnalysis(num):
    if num == 1:
        if number[0] == TargetResult:
            return True
        else:
            return False
    
    for i in range(num):
        for j in range(i + 1, num):
            a, b = number[i], number[j]
            number[j] = number[num - 1]
            str_a, str_b = result[i], result[j]
            result[j] = result[num - 1]
            # a + b (b + a)
            result[i] = '(' + str_a + '+' + str_b + ')'
            number[i] = a + b
            if GameAnalysis(num - 1):
                return True
            # a - b
            result[i] = '(' + str_a + '-' + str_b + ')'
            number[i] = a - b
            if GameAnalysis(num - 1):
                return True
            # b - a
            result[i] = '(' + str_b + '-' + str_a + ')'
            number[i] = b - a
            if GameAnalysis(num - 1):
                return True
            # a * b (b * a)
            result[i] = '(' + str_a + '*' + str_b + ')'
            number[i] = a * b
            if GameAnalysis(num - 1):
                return True
            # a / b
            if b != 0:
                result[i] = '(' + str_a + '/' + str_b + ')'
                number[i] = a / b
                if GameAnalysis(num - 1):
                    return True
            # b / a
            if a != 0:
                result[i] = '(' + str_b + '/' + str_a + ')'
                number[i] = b / a
                if GameAnalysis(num - 1):
                    return True
            
            number[i] = a
            number[j] = b
            result[i] = str_a
            result[j] = str_b
            
    return False

def main():
    # append will be [[]]
    result.extend(input("Input 4 number:").split())
    for n in result:
        number.append(int(n))
    
    if GameAnalysis(CardNumber):
        print("Success.")
        print(result[0])
    else:
        print("Fail.")

if __name__ == '__main__':
    main()