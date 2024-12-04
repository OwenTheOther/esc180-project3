'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math


def split_string(L, S):
    ret = [""]
    split_num = 0
    for i in L:
        if i in S:
            split_num += 1
            ret.append("")
        else:
            ret[split_num] = ret[split_num] + i

    deleted = 0
    for i in range(len(ret)):
        if ret[i-deleted] == "":
            ret.pop(i-deleted)
            deleted += 1
    return ret


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot = 0
    for word, count1 in vec1.items():
        if word in vec2:
            dot += count1 * vec2[word]
    return dot/(norm(vec1) * norm(vec2))
    


def build_semantic_descriptors(sentences):
    descriptors = {}
    for words in sentences:
        to_ignore = []
        for word in words:
            if word.lower() not in to_ignore:
                if word.lower() not in descriptors:
                    descriptors[word.lower()] = {}
                other_ignore = []
                for otherword in words:
                    if otherword.lower() not in other_ignore:    
                        if otherword.lower() not in descriptors[word.lower()]:
                            descriptors[word.lower()][otherword.lower()] = 1
                        else:
                            descriptors[word.lower()][otherword.lower()] += 1
                        other_ignore.append(otherword.lower())
                    
                descriptors[word.lower()][word.lower()] -= 1
                if descriptors[word.lower()][word.lower()] == 0:
                    del descriptors[word.lower()][word.lower()]
        to_ignore.append(word.lower())
    return descriptors

def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for filename in filenames:
        f = open(filename, "r", encoding="latin1").read()
        lines = split_string(f, [".",".", "!", "?"])
        for line in lines:
            to_add = split_string(line, [" ", ",", "-", "--", ":", ";", "\n"])
            if to_add != []:
                sentences.append(to_add)
    return build_semantic_descriptors(sentences)
        



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    similarities = {}
    
    if word.lower() not in semantic_descriptors:
        return None

    for choice in choices:
        if choice.lower() in semantic_descriptors:
            sim = similarity_fn(semantic_descriptors[word.lower()], semantic_descriptors[choice.lower()])
            if sim == 0:
                similarities[choice.lower()] = -1
            else:
                similarities[choice.lower()] = sim
    max_sim = -2
    max_choice = None        
    for choice, val in similarities.items():
        if val > max_sim:
            max_sim = val
            max_choice = choice
    return choice


    


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    testfile = open(filename, "r", encoding="latin1").read()
    total_tests = 0
    tests_passed = 0
    for line in testfile.splitlines():
        test = line.split()
        test_word = test[0]
        answer = test[1]
        options = test[2:]
        max_similarity = -1
        max_option = options[0]
        for option in options:
            sim = similarity_fn(semantic_descriptors[test_word], semantic_descriptors[option])
            if sim > max_similarity:
                max_similarity = sim
                max_option = option
        if max_option == answer:
            tests_passed += 1
        total_tests += 1
    return tests_passed / total_tests * 100





if __name__ == "__main__":
    ##testing

    #cosine similarity works! matches doc test case
    #print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))

    

    #building semantic descriptors works! matches doc test case
    # s = [["i", "am", "a", "sick", "man"],
    # ["i", "am", "a", "spiteful", "man"],
    # ["i", "am", "an", "unattractive", "man"],
    # ["i", "believe", "my", "liver", "is", "diseased"],
    # ["however", "i", "know", "nothing", "at", "all", "about", "my",
    # "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    #print(build_semantic_descriptors(s)["man"])

    # d = build_semantic_descriptors_from_files(["small_sample.txt"])
    # print(d)

    # print(most_similar_word("Parents", ["eifnwiuf", "children",  "story", "experience"], d, cosine_similarity))
    #d = build_semantic_descriptors_from_files(["warandpeace.txt", "swannsway.txt"])
    #print(d["the"])
    print(build_semantic_descriptors_from_files(["tstring.txt"]))

    pass