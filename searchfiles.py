#!/usr/bin/env python
import fnmatch
import os
import subprocess
import argparse
import csv
import pickle
from matplotlib import pyplot as plt
from scipy import stats

parser = argparse.ArgumentParser(description="A simple script to find word counts of all tex files in all subdirectories of a target directory.")
parser.add_argument("target", help="the directory or csv file you would like to search/use")
parser.add_argument("-c", "--csv", help="statistical analysis on a csv file", action="store_true")
args = parser.parse_args()

if args.csv:
    # If -c tag passed read data from csv file in correct format
    print "Reading data from csv file: %s" % args.target
    f = open(args.target, 'r')
    csvrdr = csv.reader(f)
    x = []
    y = []
    for row in csvrdr:
        x.append(int(row[0]))
        y.append(int(row[1]))
    f.close()

else:
    # Else search through all subdirectories (recursively)
    directory = args.target
    matches = []
    for root, dirnames, filenames in os.walk(directory):
      for filename in fnmatch.filter(filenames, '*.tex'):
            matches.append(os.path.join(root, filename))

    wordcounts = {}
    codewordcounts = {}
    fails = {}
    for f in matches:
        #Quote the filename.
        g = '"%s"'%f
        print "-" * 30
        print f
        process = subprocess.Popen(['texcount', '-1', g],stdout=subprocess.PIPE)
        out, err = process.communicate()
        try:
            wordcounts[f] = eval(out.split()[0])
            print "\t has %s words." % wordcounts[f]
        except:
            print "\t Couldn't count with texcount..."
            fails[f] = err
        process = subprocess.Popen(['wc', '-w', f],stdout=subprocess.PIPE)
        out, err = process.communicate()
        try:
            codewordcounts[f] = eval(out.split()[0])
            print "\t has %s code words." % codewordcounts[f]
        except:
            print "\t Couldn't count with wc..."
            fails[f] = err

    # Convert data to correct type

    x = [codewordcounts[e] for e in wordcounts]
    y = [wordcounts[e] for e in wordcounts]

    # Write data to csv including file name

    data = zip(x, y, [e for e in wordcounts])
    f = open('wordsvcodewords.csv', 'w')
    wrtr = csv.writer(f)
    for row in data:
        wrtr.writerow(row)
    f.close()



# Fit linear regression model

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

# Plot scatter plot and fitted line

plt.figure()
plt.scatter(x, y, color='black')
plt.plot(x, [slope * i + intercept for i in x], lw=2, label='y=%0.2f*x + %0.2f  (p=%0.2f)' % (slope, intercept, p_value))
plt.xlabel("Code words")
plt.ylabel("Words")
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
plt.legend()
plt.savefig('wordsvcodewords.png')


# Draw histogram

plt.figure()
plt.hist(x, bins=20,  color='b', label='Code words (N=%s, mean=%s)' %(len(x), sum(x)/len(x)) )
plt.hist(y, bins=20,  color='r', alpha=0.5, label='Words (N=%s, mean=%s)' %(len(y), sum(y)/len(y)) )
plt.ylabel("Frequency")
plt.legend()
plt.savefig('counthistogram.png')
