import sys
import csv
import random

def generate_test_train_numbers(num_range: int, test_ratio: float):
    numbers = range(num_range)
    test_numbers = random.sample(numbers, (int)(num_range * test_ratio))
    test_numbers.sort()
    train_numbers = [number for number in numbers if number not in test_numbers]
    return { 
            "test"  : test_numbers, 
            "train" : train_numbers 
           }

def generate_all_author_files(numbers: dict, tsv_file_path: str, train_file_path: str, test_file_path: str):
    authors = set()
    vocab = set()
    with open(tsv_file_path, "r") as tsv_file:
        all_reviews = tsv_file.readlines() 
        current_author = all_reviews[0].split('\t')[1]
        current_reviews = list()
        for review in all_reviews:
            review = review.split('\t')
            if current_author != review[1]:
                generate_author_files(numbers, current_reviews, current_author, train_file_path, test_file_path)
                authors.add(current_author)
                current_reviews.clear()
                current_author = review[1]
            try:
                current_reviews.append(review[5])
                vocab.update(review[5].split())
            except:
                print("Error occured: text section does not exist")
                        
        generate_author_files(numbers, current_reviews, current_author, train_file_path, test_file_path)
        authors.add(current_author)
    return authors, vocab         
  
              
def generate_author_files(numbers: dict, reviews: str, author: str, train_path: str, test_path: str):
    with open(f"{train_path}/{author}.txt", "w") as train_file:
        with open(f"{test_path}/{author}.txt", "w") as test_file:
            for index, review in enumerate(reviews):
                if index in numbers["test"]:
                    test_file.write(review)
                else:
                    train_file.write(review)



def generate_all_unigrams(authors: set(), vocab: set(), train_path: str):
    unigram_counts = {author: {word: 0 for word in vocab} for author in authors}
    unigrams = {author: {word: 0 for word in vocab} for author in authors}
    vocab_length = len(vocab)
    i = 0
    for author in authors:
        with open(f"{train_path}/{author}.txt", "r") as author_file:
            reviews = author_file.readlines()
            reviews_length = 0
            for review in reviews:
                i += 1
                split_review = review.split()
                reviews_length += len(split_review)
                for word in split_review:
                    unigram_counts[author][word] += 1
            for word in unigram_counts[author]:
                unigrams[author][word] = (unigram_counts[author][word] + 1)/(reviews_length + vocab_length)
    
    print(len(unigrams))
    print(i)        
    return unigrams 

numbers = generate_test_train_numbers(1000, 0.10)
authors, vocab = generate_all_author_files(numbers, "./imdb62.tsv", "./train", "./test")
generate_all_unigrams(authors, vocab, "./train")
