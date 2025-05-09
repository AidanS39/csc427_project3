# Authorship Attribution
### CSC 427 - Project 3
#### Aidan Stoner, Nicholas Merritt, Jason Perrella

## Summary

Using natural language processing concepts such as N-Gram modeling and classification, the Authorship Attribution system can compute a ranked list of authors with scores signifying its confidence in which author wrote a specific set of reviews. The system uses a 90% train and 10% test split, using the training set to learn each of the 62 authors' writing styles, with each writing style represented as a unigram model. When given a test set, the system computes a geometric mean, or score, of the test set when given to one of the authors' unigram models.

This project was developed and tested on the TCNJ HPC system.

The program has two main features, a ranking list feature and a top-k evaluation feature. These features include versions for AllTokens and Singletons. Results will always slightly differ as the training and test sets are always randomly selected.

## Requirements

The requirements for the project were derived from the hardware and software that the project was developed and tested on. Any variation of these requirements is not guaranteed to be sufficient to run this program.
1. Python 3.8.6
2. Linux-based shell
3. Significant computing power
4. imdb62.tsv (Run the setup.sh script if you do not have this file.)

## Usage

All instructions will be completed in the project root directory, which is the `csc427_project3` directory.

Locate the path of the required tsv file, imdb62.tsv. Also locate the path of the train and test directories. The program will store the training and test data into these respective directories.

From the root directory, run `python3 author_attrib.py <tsv/file/path> <train/file/path> <test/file/path>`. The file paths can be relative to the working directory, or an absolute address.
For example, `python3 author_attrib.py ./imdb62.tsv ./train ./test`. Note that I did not include a forward slash at the end of the file paths.

After a few seconds, a command-line menu should appear. Choose an option listed in the menu, or type "exit" + ENTER to exit.
