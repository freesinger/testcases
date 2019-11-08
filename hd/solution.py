import os
import sys
import zipfile
from copy import deepcopy

# Global dics
IPs = {}
num_part_date = {}
record_date = {}
record_condition = {}
trial_mappings = {}


""" Unzip file function for scalability """
def unzip(file="results.zip"):
    folder = os.listdir()
    try:
        if file not in folder:
            print("Results zip file not exists")
            sys.exit()
        elif "results" not in folder:
            with zipfile.ZipFile(file, "r") as res_zip:
                res_zip.extractall("results")
                print("Extracting to results folder...")
            print("Extract done")
        else:
            pass
    except IOError:
        print("IOError occured, exiting...")
        sys.exit()

""" Handling task 1 """
def task1(folder=None):
    header = ['Condition', 'Name', 'Gender', 'Age', 'Proportion of hits', 'Proportion of nearmisses',
              ' Proportion of fullmisses', 'meanHapp of hit', 'meanWill of hit', 'meanHapp of nearmisses',
              'meanWill of nearmisses', 'meanHapp of fullmisses', 'meanWill of fullmisses', 'maxHapp', 'trialnumber',
              'minHapp', 'trialnumber\n']
    with open("task1.csv", 'w') as dest_file:
        dest_file.write(','.join(header))

    # results_folder = os.path.join(os.path.dirname(__file__), "results", "results")
    # results_folder = os.path.join(os.getcwd(), "results", "results")
    # print(results_folder)
    # print(len(os.listdir(results_folder)))
    file_number = 0
    for file in os.listdir(folder):
        file_number += 1
        with open(os.path.join(folder, file), "r") as f, open("task1.csv", 'a') as t1:
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
            notSameIP = True
            for line in f.readlines():
                line_number += 1
                if line_number == 1:
                    line = line.strip('\n')
                    condition = line.strip()
                    record_condition[file_number] = condition
                elif line_number == 4:
                    infor = line.split(',')
                    Name = infor[0]

                    # parsing age and gender
                    Age = infor[1]
                    Gender = infor[2]
                    if 'female' in Gender.lower():
                        Gender = "2"
                    else:
                        Gender = "1"
                elif line_number == 2:
                    _, raw_date = line.strip().split(':')
                    raw_date = raw_date.strip()
                    date = '-'.join([raw_date[0:2], raw_date[2:4], raw_date[4:8]])
                    if date not in record_date:
                        record_date[date] = [file_number]
                    else:
                        record_date[date].append(file_number)
                    if date not in num_part_date:
                        num_part_date[date] = 1
                    else:
                        num_part_date[date] += 1
                elif line_number == 3:
                    _, IP = line.strip('\n').split(':')
                    if IP not in IPs:
                        IPs[IP] = 1
                    else:
                        notSameIP = False
                        
                # parsing Proportion of Hits, Near misses, and Full Misses over the total number of trials
                elif line_number != 3:
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
                else:
                    continue

            trial_mappings[file_number] = trials
            if notSameIP:
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


                aList = [condition, Name, Gender, Age, hit_proportion, near_proportion, full_proportion, meanHapp_hit,
                         meanWill_hit, meanHapp_near, meanWill_near, meanHapp_full, meanWill_full, maxHappiness,
                         trialmax_number, minHappiness, trialmin_number]

                bList = ','.join(aList)
                t1.write(bList + '\n')

""" Handling task 2 """
def task2():
    avg_trials = deepcopy(record_date)

    for seq in record_date.values():
        for i in range(len(seq)):
            seq[i] = record_condition[seq[i]]

    for k, v in record_date.items():
        mapping = {"skill": 0, "mixed": 0, "luck": 0}
        for ele in v:
            mapping[ele] += 1
        record_date[k] = mapping
    print(record_date)


    for k, v in avg_trials.items():
        avg_trials[k] = round(sum(map(lambda x: trial_mappings[x], v)) / len(v), 2)


    print(avg_trials)

    with open("task2.csv", 'w') as t2:
        header = ['Date', 'Number of participants', 'Skill', 'Luck', 'Mixed', 'avg_trials\n']
        t2.write(','.join(header))
        for date in num_part_date.keys():
            record = [date, str(num_part_date[date]), str(record_date[date]['skill']), str(record_date[date]['luck']),
                      str(record_date[date]['mixed']), str(avg_trials[date])]
            t2.write(','.join(record))
            t2.write('\n')


if __name__ == "__main__":
    unzip(file="results.zip")
    task1(folder=os.path.join(os.getcwd(), "results", "results"))
    task2()
