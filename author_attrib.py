import sys
import math
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
    
    # open reviews file
    with open(tsv_file_path, "r") as tsv_file:
        
        # read all reviews
        all_reviews = tsv_file.readlines() 

        # intitialize the current author as the author of the first review
        current_author = all_reviews[0].split('\t')[1]
        current_reviews = list()
        
        # iterate through all reviews
        for review in all_reviews:
            
            # split review by tab so it can get the author of the current review and the text content of the review
            review = review.split('\t')

            # if author of current review is not current_author
            if current_author != review[1]:
                generate_author_files(numbers, current_reviews, current_author, train_file_path, test_file_path)
                authors.add(current_author)
                current_reviews.clear()
                current_author = review[1]
            # if author of current review is current_author
            try:
                current_reviews.append(review[5])
                vocab.update(review[5].split())
            except:
                raise Exception("Error: text section does not exist")
                        
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
    
    # intitalize a unigrams and unigram counts dictionary
    unigram_counts = {author: {word: 0 for word in vocab} for author in authors}
    unigrams = {author: {word: 0 for word in vocab} for author in authors}
    
    # find length of vocab
    vocab_length = len(vocab)
    
    
    # iterate through each author's training set of reviews
    for author in authors:
        with open(f"{train_path}/{author}.txt", "r") as train_file:
            
            # read all reviews in training set
            reviews = train_file.readlines()
            reviews_length = sum(len(review.split()) for review in reviews)

            # iterate through every word in every review
            for review in reviews:
                review = review.split()
                for word in review:
                    unigram_counts[author][word] += 1
            # calculate the unigram probability for every word in unigram counts dictionary
            for word in unigram_counts[author]:
                unigrams[author][word] = (unigram_counts[author][word] + 1)/(reviews_length + vocab_length)



#        if author is list(authors)[0]:
#            print(unigram_counts[author])
#            print(author)    
#    print(len(unigrams))
    return unigrams 



def compute_alltokens(unigrams: dict(), test_path: str, author: str):
    geo_mean = 0
    word_count = 0
    
    # iterate through every word in every review, add log of unigram probability to geo_mean
    with open(f"{test_path}/{author}.txt", "r") as test_file:
        reviews = test_file.readlines() 
        for review in reviews:
            review = review.split()
            for word in review:
                word_count += 1
                geo_mean += math.log(unigrams[word], 2)
    
    # compute the alltokens geometric mean
    geo_mean = 2**(geo_mean * (1 / word_count))
    
    return geo_mean

def compute_singletons(unigrams: dict(), test_path: str, author: str):
    geo_mean = 0
    word_counts = dict()
    singletons = set()
    
    # iterate through every word in every review, keep track of every word count in word_counts
    with open(f"{test_path}/{author}.txt", "r") as test_file:
        reviews = test_file.readlines() 
        for review in reviews:
            review = review.split()
            for word in review:
                if word not in word_counts:
                    word_counts[word] = 1
                else:
                    word_counts[word] += 1
    
    # find all words that occur only once, add them to singletons list
    for word in word_counts:
        if word_counts[word] == 1:
            singletons.add(word)
        elif word_counts[word] < 1:
            raise Exception("Error: word was listed in word counts that never occured")
    
    # calculate the singletons geometric mean
    for word in singletons:
        geo_mean += math.log(unigrams[word], 2)
    geo_mean = geo_mean / len(singletons)
    geo_mean = 2**geo_mean
   
    return geo_mean

def print_ranked_list_alltokens(unigrams: dict(), authors: set(), target_author: str, test_path: str):
    ranked_list = list()
    
    geo_means = dict()
    for author in authors:
        geo_means[author] = compute_alltokens(unigrams[author], test_path, target_author)
    
    ranked_list = sorted(geo_means.items(), key=lambda x: x[1], reverse=True)
    print("RANK AUTHOR    GEO. MEAN")
    for rank, item in enumerate(ranked_list):
        print(f"{(rank + 1):<5}{item[0]:<10}{item[1]:<15}")

def print_ranked_list_singletons(unigrams: dict(), authors: set(), target_author: str, test_path: str):
    ranked_list = list()
    
    geo_means = dict()
    for author in authors:
        geo_means[author] = compute_singletons(unigrams[author], test_path, target_author)
    
    ranked_list = sorted(geo_means.items(), key=lambda x: x[1], reverse=True)
    print("RANK AUTHOR    GEO. MEAN")
    for rank, item in enumerate(ranked_list):
        print(f"{(rank + 1):<5}{item[0]:<10}{item[1]:<15}")

def evaluate_alltokens(unigrams: dict(), authors: set(), test_path: str, k: int):
    correct_count = 0    

    for target_author in authors:
        geo_means = dict()
        ranked_list = list()
        for author in authors:
            geo_means[author] = compute_singletons(unigrams[author], test_path, target_author)
        
        ranked_list = sorted(geo_means.items(), key=lambda x: x[1], reverse=True)
        top_k = [ranking[0] for ranking in ranked_list[0:k]]
        if target_author in top_k:
            correct_count += 1
    
    print(f"{correct_count}/62")

def evaluate_singletons(unigrams: dict(), authors: set(), test_path: str, k: int):
    correct_count = 0    

    for target_author in authors:
        geo_means = dict()
        ranked_list = list()
        for author in authors:
            geo_means[author] = compute_singletons(unigrams[author], test_path, target_author)
        
        ranked_list = sorted(geo_means.items(), key=lambda x: x[1], reverse=True)
        top_k = [ranking[0] for ranking in ranked_list[0:k]]
        if target_author in top_k:
            correct_count += 1
    
    print(f"{correct_count}/62")



# Main Function & Menu

if (len(sys.argv) > 4):
    print("Error: missing arguments. Format: python3 author_attrib.py imdb62.tsv <train path> <test path>")
    sys.exit()

tsv_path = sys.argv[1]
train_path = sys.argv[2]
test_path = sys.argv[3]

print("Generating random numbers...")
numbers = generate_test_train_numbers(1000, 0.10)

print("Generating training and test files for each author...")
authors, vocab = generate_all_author_files(numbers, tsv_path, train_path, test_path)

print("Generating unigram models for each author...")
unigrams = generate_all_unigrams(authors, vocab, train_path)

option = "0"
while (option != "exit"):
    print("OPTIONS:")
    print("[1]\tAllTokens Rankings")
    print("[2]\tSingletons Rankings")
    print("[3]\tAllTokens Top k Evaluation")
    print("[4]\tSingletons Top k Evaluation")
    print("[exit]\tExit")
    option = input("Please select an option: ")

    if option == "1":
        author = input("Author ID: ")
        if author in authors:
            print_ranked_list_alltokens(unigrams, authors, author, test_path)
        else:
            print("Invalid author.")
    elif option == "2":
        author = input("Author ID: ")
        if author in authors:
            print_ranked_list_singletons(unigrams, authors, author, test_path)
        else:
            print("Invalid author.")
    elif option == "3":
        try:
            k = int(input("Please input a top k: "))
            print("Evaluating top k...")
            evaluate_alltokens(unigrams, authors, test_path, k)
        except ValueError:
            print("Invalid k.")
    elif option == "4":
        try:
            k = int(input("Please input a top k: "))
            print("Evaluating top k...")
            evaluate_singletons(unigrams, authors, test_path, k)
        except ValueError:
            print("Invalid k.")
    elif option == "exit":
        sys.exit()
    else:
        print("Invalid option.")
    input("Press Enter to continue...")
