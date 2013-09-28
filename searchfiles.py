#!/usr/bin/env python
import fnmatch
import os
import subprocess
import argparse
import matplotlib.pyplot as plt
import pickle

def trim(t, p=0.01):
    """Trims the largest and smallest elements of t.

    Args:
    t: sequence of numbers
    p: fraction of values to trim off each end

    Returns:
    sequence of values
    """
    t.sort()
    n = int(p * len(t))
    t = t[n:-n]
    return t

parser = argparse.ArgumentParser(description="A simple script to find word counts of all tex files in all subdirectories of a target directory.")
parser.add_argument("directory", help="the directory you would like to search")
parser.add_argument("-t", "--trim", help="trim data percentage", default=0)
args = parser.parse_args()
directory = args.directory
p = float(args.trim)

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


try:
    data = [wordcounts[e] for e in wordcounts]
    data = trim(data, p)

    plt.figure()
    plt.hist(data, bins=20)
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Distribution of words counts in all my LaTeX documents\n ($N=%s$,mean=$%s$, max=$%s$)" % (len(data), sum(data)/len(data), max(data)))
    plt.savefig('latexwordcountin%s.svg' % directory.replace("/", "-"))
except:
    print "Graph not produced, perhaps you don't have matplotlib installed..."
