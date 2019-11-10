import os

# open the file
path = os.path.join(os.getcwd(), "results","results")
dir_list = os.listdir(path)

# read the file
header = ['Condition', 'Name', 'Gender', 'Age', 'Proportion of hits', 'Proportion of nearmisses',
          ' Proportion of fullmisses', 'meanHapp of hit', 'meanWill of hit', 'meanHapp of nearmisses',
          'meanWill of nearmisses', 'meanHapp of fullmisses', 'meanWill of fullmisses', 'maxHapp', 'trialnumber',
          'minHapp', 'trialnumber']
Header = ','.join(header)

newFile = open('newFile.csv', 'w')
newFile.write(Header + '\n')

seen_ip_addresses = []
allFileInfo = []
date_dict = {}

for file_name in dir_list:
    writable = True
    file = open(os.path.join(path, file_name), 'r')
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
    file_information = []

    for line in file:
        line_number += 1
        if line_number == 1:
            line = line.strip(' \n')
            condition = line
            file_information.append(condition)
        elif line_number == 2:
            raw_date = line.strip('Date: ')
            date = '-'.join([raw_date[0:2], raw_date[2:4], raw_date[4:8]])
            file_information.append(date)
            # print(date)
            if date not in date_dict:
                date_dict[date] = 1
            else:
                date_dict[date] += 1
            # print(date_dict)
        elif line_number == 3:
            # print(line)
            tmp = line.strip().split(':')
            # print(tmp)
            if tmp[1] in seen_ip_addresses:
                writable = False
            else:
                seen_ip_addresses.append(tmp[1])
            # print(seen_ip_addresses)
        elif line_number == 4:
            infor = line.split(',')
            # print(line)
            Name = infor[0]
            # parsing age and gender
            Age = infor[1]
            Gender = infor[2]
            if 'female' in Gender.lower():
                Gender = "2"
            else:
                Gender = "1"
            # parsing Proportion of Hits, Near misses, and Full Misses over the total number of trials
        else:
            line = line.strip('\n')
            values = line.split(',')
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
    file_information.append(trials)
    allFileInfo.append(file_information)
    # print(file_information)

# caculation of proportion
    hit_proportion = str(hits / trials)
    full_proportion = str(full_misses / trials)
    near_proportion = str(near_misses / trials)
# caculation of mean
    meanHapp_hit = str(happiness_hit / hits)
    meanWill_hit = str(willingness_hit / hits)
    meanHapp_full = str(happiness_full / full_misses)
    meanWill_full = str(willingness_full / full_misses)
    meanHapp_near = str(happiness_near / near_misses)
    meanWill_near = str(willingness_near / near_misses)
# finding max and min happiness
    maxHappiness = str(max(mList))
    trialmax_number = str(mList.index(int(maxHappiness)))
    minHappiness = str(min(mList))
    trialmin_number = str(mList.index(int(minHappiness)))

    aList = [condition, Name, Gender, Age, hit_proportion, near_proportion, full_proportion, meanHapp_hit, meanWill_hit,
             meanHapp_near, meanWill_near, meanHapp_full, meanWill_full, maxHappiness, trialmax_number, minHappiness,
             trialmin_number]
    bList = ','.join(aList)

    file.close()

    if writable:
        newFile.write(bList)
        newFile.write('\n')
print(allFileInfo)
newFile.close()

print("-****************-")
print("-*****Task3******-")
print("-****************-")

date_skill = {}
date_luck = {}
date_mixed = {}
date_avg_trials = {}

for date in date_dict.keys():
    date_skill[date] = 0
    date_luck[date] = 0
    date_mixed[date] = 0
    date_avg_trials[date] = 0

# print(date_luck)
for date in date_dict.keys():
    for record in allFileInfo:
        if date == record[1]:
            if record[0] == 'skill':
                if date not in date_skill:
                    date_skill[date] = 1
                else:
                    date_skill[date] += 1
            elif record[0] == 'luck':
                if date not in date_luck:
                    date_luck[date] = 1
                else:
                    date_luck[date] += 1
            else:
                if date not in date_mixed:
                    date_mixed[date] = 1
                else:
                    date_mixed[date] += 1
            date_avg_trials[date] += record[2]

for date in date_dict.keys():
    date_avg_trials[date] = '%.2f' %(date_avg_trials[date] / date_dict[date])
# print(date_avg_trials)
# print(date_luck)

newFile2 = open("newFile2.csv", 'w')
header = ['Date', 'Number of participants', 'Skill', 'Luck', 'Mixed', 'avg_trials\n']
newFile2.write(','.join(header))
for date in date_dict.keys():
    record = [date, str(date_dict[date]), str(date_skill[date]), str(date_luck[date]), str(date_mixed[date]), str(date_avg_trials[date])]
    newFile2.write(','.join(record)+'\n')

















