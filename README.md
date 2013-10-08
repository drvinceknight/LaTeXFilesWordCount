A repo with a script to recursively run `latexcount` on all tex files in a target directory. The output of the script is three files:

- A scatter plot with a fitted regression line [png]
- A histogram with both code words and words represented [png]
- A csv file with 3 columns (number of code words, number of words, file name), which is to be used for further analysis

I have written 2 blog posts showing the use of this script (as it has evolved):

1.Just counting: [here](http://drvinceknight.blogspot.co.uk/2013/09/counting-words-in-all-my-latex-files.html).
2. Regression model: [here](http://drvinceknight.blogspot.co.uk/2013/10/almost-2-to-1-ratio-of-code-words-to.html).

# Usage

To run the script on a directory (which will recursively search all subdirectories):

    ./countlatexwords.py directory

To run the script on a csv file (which needs to have two column of data: number of code words, number of words):

    ./countlatexwords.py -c file.csv


# Dependencies

The script uses [matplotlib](http://matplotlib.org/) for the plotting and [scipy](http://www.scipy.org/) for the linear regression.

# License Information

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/us/) license.  You are free to:

* Share: copy, distribute, and transmit the work,
* Remix: adapt the work

Under the following conditions:

* Attribution: You must attribute the work in the manner specified by the author or licensor (but not in any way that suggests that they endorse you or your use of the work).
* Share Alike: If you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.

When attributing this work, please include me.
