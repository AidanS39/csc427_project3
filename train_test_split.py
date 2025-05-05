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

def generate_test_train_files(numbers: dict, tsv_file_path: str, train_file_path: str, test_file_path: str):
    with open(tsv_file_path, "r") as tsv_file:
        current_author = '33913'
        reviews = list()
        i = 0
        for line in tsv_file:
            line = line.split('\t')
            if current_author != line[1]:
                generate_author_files(numbers, reviews, current_author, train_file_path, test_file_path)
                reviews.clear()
                current_author = line[1]
            try:
                reviews.append(line[5])
            except:
                print("Error occured: text section does not exist")
                        
        generate_author_files(numbers, reviews, current_author, train_file_path, test_file_path)
                
                
def generate_author_files(numbers: dict, reviews: str, author: str, train_file_path: str, test_file_path: str):
    with open(f"{train_file_path}/{author}.txt", "w") as train_file:
        with open(f"{test_file_path}/{author}.txt", "w") as test_file:
            for index, review in enumerate(reviews):
                if index in numbers["test"]:
                    test_file.write(review)
                else:
                    train_file.write(review)
                    
            

numbers = generate_test_train_numbers(1000, 0.10)
generate_test_train_files(numbers, "./imdb62.tsv", "./train", "./test")
