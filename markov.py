from random import choice
import sys

file_path = sys.argv[1]

def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    one_long_source_string = open(file_path).read()
    return one_long_source_string

    

def make_chains(text_string, n_gram = 2):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    split_string = text_string.split()
    # first_source_words = tuple(split_string[0:2])

    chains = {}

    # key is a bi-gram tuple, value is a list of strings which can follow the tuple
    for index in range(len(split_string) - n_gram):

        key_list = []

        for i in range(n_gram):
            key_list.append(split_string[index + i])

            key = tuple(key_list)

        value = split_string[index + n_gram]

        chains[key] = chains.get(key, [])
        chains[key].append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    #check length of key and use that for the number of items in the tuple

    tuple_seed = choice(chains.keys())

    #Pick a tuple seed
    while tuple_seed[0][0].isupper() == False: 
        tuple_seed = choice(chains.keys())
        
    key_length = len(tuple_seed)    

    text = []
    for index in range(key_length):
            text.append(tuple_seed[index])  

    # print text

    #loop
    while text[-1][-1] not in ".!?":
        #sets value_options to the tuple seed's values
        value_options = chains.get(tuple_seed)

        #pick one of those values
        value_choice = choice(value_options)
        
        text.append(value_choice)
        print tuple_seed

############################################
        tuple_list = text[-key_length:]
        tuple_seed = tuple(tuple_list)   

    
    text_sentence = ' '.join(text)
    return text_sentence


# input_path = "gettysburg.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(file_path)

# Get a Markov chain
chains = make_chains(input_text, 2)

# Produce random text
random_text = make_text(chains)

print random_text