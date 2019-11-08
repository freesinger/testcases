import os

# open the file
path = "/Users/shanewang/Desktop/Codes/AAAI-procedding/hd/results/results/"
dir_list = os.listdir(path)
# # print(dir_list)


header = ['Condition', 'Name', 'Gender', 'Age', 'Proportion of hits', 'Proportion of nearmisses',
        ' Proportion of fullmisses', 'meanHapp of hit', 'meanWill of hit', 'meanHapp of nearmisses',
        'meanWill of nearmisses', 'meanHapp of fullmisses', 'meanWill of fullmisses', 'maxHapp', 'trialnumber',
        'minHapp', 'trialnumber']
Header = ','.join(header)
newFile = open('newFile.csv', 'w')
newFile.write(Header + '\n')
# read the file

date_dict = {}

seen_addresses = []
allFiles = []

for file_name in dir_list:
    writeble = True
    file = open(path + file_name, 'r')
    line_number = 0
    # iterate through one participant file
    trials = 0  # items for Proportion of Hits, Near misses, and Full Misses over the total number of trials
    hits = 0
    near_misses = 0
    full_misses = 0

    happiness_hit = 0  # items for mean happiness and mean willingness
    happiness_full = 0
    happiness_near = 0
    willingness_hit = 0
    willingness_full = 0
    willingness_near = 0

    mList = []
    bList = []
    fileInfo = []

    for line in file:
        line_number += 1
        if line_number == 1:
            line = line.strip(' \n')
            # print(line)
            condition = line
            fileInfo.append(condition)
        elif line_number == 2:
            tmp = line.strip().split(':')
            raw_date = tmp[1].strip()
            date = '-'.join([raw_date[0:2], raw_date[2:4], raw_date[4:8]])
            fileInfo.append(date)
            if date not in date_dict:
                date_dict[date] = 1
            else:
                date_dict[date] += 1
            # print(date_dict)
            # print(fileInfo)
        elif line_number == 3:
            tmp = line.strip().split(':')
            if tmp[1] in seen_addresses:
                writeble = False
            else:
                seen_addresses.append(tmp[1])
        elif line_number == 4:
            infor = line.split(',')
            # # print(line)
            Name = infor[0]
            # print(Name)
            # parsing age and gender
            Age = infor[1]
            # print(Age)
            Gender = infor[2]
            # print(Gender)
            Gender = Gender.replace('F', 'f')
            Gender = Gender.replace('A', 'a')
            Gender = Gender.replace('M', 'm')
            Gender = Gender.replace('E', 'e')
            Gender = Gender.replace('L', 'l')
            # print(Gender)
            if 'female' in Gender:
                Gender = "2"
            else:
                Gender = "1"
            # print(Gender)
            
            # parsing Proportion of Hits, Near misses, and Full Misses over the total number of trials

        else:
            line = line.strip('\n')
            values = line.split(',')
            # print(values)
            if values[0] != 'trial':
                continue
            if 'trial' in values:
                trials = trials + 1
            if 'hit' in values:
                hits = hits + 1
            if 'fullMiss' in values:
                full_misses = full_misses + 1
            if 'nearMiss' in values:
                near_misses = near_misses + 1
            # parsing Mean happiness and mean willingness
            if values[4] == "hit":
                happiness_hit = happiness_hit + int(values[7])
                willingness_hit = willingness_hit + int(values[8])
            if values[4] == "fullMiss":
                happiness_full = happiness_full + int(values[7])
                willingness_full = willingness_full + int(values[8])
            if values[4] == "nearMiss":
                happiness_near = happiness_near + int(values[7])
                willingness_near = willingness_near + int(values[8])
            # parsing the maximum and the minimum reported happiness levels and the trial in which they occurred
            mList.append(int(values[7]))
    fileInfo.append(trials)
    allFiles.append(fileInfo)
# caculation of proportion
    hit_proportion = str(hits / trials)
    # print(hit_proportion)
    full_proportion = str(full_misses / trials)
    # print(full_proportion)
    near_proportion = str(near_misses / trials)
    # print(near_proportion)
# caculation of mean
    meanHapp_hit = str(happiness_hit / hits)
    # print(meanHapp_hit)
    meanWill_hit = str(willingness_hit / hits)
    # print(meanWill_hit)
    meanHapp_full = str(happiness_full / full_misses)
    # print(meanHapp_full)
    meanWill_full = str(willingness_full / full_misses)
    # print(meanWill_full)
    meanHapp_near = str(happiness_near / near_misses)
    # print(meanHapp_near)
    meanWill_near = str(willingness_near / near_misses)
    # print(meanWill_near)
# finding max and min happiness
    # print(mList)
    maxHappiness = str(max(mList))
    # print(maxHappiness)
    trialmax_number = str(mList.index(int(maxHappiness)))
    # print(trialmax_number)
    minHappiness = str(min(mList))
    # print(minHappiness)
    trialmin_number = str(mList.index(int(minHappiness)))
    # print(trialmin_number)

    aList = [condition, Name, Gender, Age, hit_proportion, near_proportion, full_proportion, meanHapp_hit, meanWill_hit, meanHapp_near, meanWill_near, meanHapp_full, meanWill_full, maxHappiness, trialmax_number, minHappiness, trialmin_number]
    # print(aList)
    bList = ','.join(aList)
    # print(bList)
    # print(Header)
    file.close() 

#for row in aList:
    if writeble:
        newFile.write(bList)
        newFile.write('\n')
print(allFiles)
newFile.close()



# print(' ')
# print('Question 2')
# print(' ')




















