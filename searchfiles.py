#!/usr/bin/env python
import fnmatch
import os
import subprocess
import argparse
import matplotlib.pyplot as plt
import pickle

parser = argparse.ArgumentParser(description="A simple script to find word counts of all tex files in all subdirectories of a target directory.")
parser.add_argument("directory", help="the directory you would like to search")
args = parser.parse_args()
directory = args.directory

matches = []
for root, dirnames, filenames in os.walk(directory):
  for filename in fnmatch.filter(filenames, '*.tex'):
        matches.append(os.path.join(root, filename))

wordcounts = {}
fails = {}
for f in matches:
    print "-" * 30
    print f
    process = subprocess.Popen(['texcount', '-1', f],stdout=subprocess.PIPE)
    out, err = process.communicate()
    try:
        wordcounts[f] = eval(out.split()[0])
        print "\t has %s words." % wordcounts[f]
    except:
        print "\t Couldn't count..."
        fails[f] = err

pickle.dump(wordcounts, open('latexwordcountin%s.pickle' % directory.replace("/", "-"), "w"))

data = [wordcounts[e] for e in wordcounts]

plt.figure()
plt.hist(data, bins=20)
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.title("Distribution of words counts in all my LaTeX documents\n ($N=%s$,mean=$%s$, max=$%s$)" % (len(data), sum(data)/len(data), max(data)))
plt.savefig('latexwordcountin%s.svg' % directory.replace("/", "-"))
