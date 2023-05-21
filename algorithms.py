import copy
#python .\main.py schemas\schema0.txt words\words0.txt Backtracking
#python .\main.py schemas\schema4.txt words\words4.txt ArcConsistency
#python .\main.py schemas\schema0.txt words\words0.txt ArcConsistency

class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass

import numpy as np

def PosToCoord(pos,M,N):
    x,y=divmod(pos,N)
    return x,y

def CoordToPos(x,y, M,N):
    place=x*N+y
    return place
import re

def seperate_string_number(string):
    previous_character = string[0]
    groups = []
    newword = string[0]
    for x, i in enumerate(string[1:]):
        if i.isalpha() and previous_character.isalpha():
            newword += i
        elif i.isnumeric() and previous_character.isnumeric():
            newword += i
        else:
            groups.append(newword)
            newword = i

        previous_character = i

        if x == len(string) - 2:
            groups.append(newword)
            newword = ''
    return groups

def getCoordinates(var,word, M,N):
    [pos, orientation]=seperate_string_number(var)
    pos=int(pos)
    x, y = divmod (pos, N)
    coord=[]
    for i in range(len(word)):
        coord.append([[x, y], word [i]])
        if orientation=='h':
            y+=1
        else:
            x+=1
    return coord

import copy

def choose_word(words):
    return words[0], 0

def choose_word_alph(words):
    words1=copy.deepcopy(words)
    words1.sort()
    best_word=words1[0]
    i=0
    for word in words:
        if word==best_word:
            return word, i
        else:
            i+=1

def choose_min_contraining_word(words, av_words, assigned, var, M, N):
    min_count=1000
    i=0
    for word in words:
        count=0
        coords1=getCoordinates(var, word, M, N)
        for words1, values1 in av_words:
            if values1 not in [x [0] for x in assigned] and values1 != var:  # uzmemo drugu rec sa kojom proveravamo i njena opcije tj reci words2
                for word1 in words1:
                    flag=False
                    coords2=getCoordinates((values1, word1, M, N))
                    for place, letter in coord1:
                        retrieved_elements = list (filter (lambda x: place in x, coord2))
                        if len (retrieved_elements) > 0:
                            constrain_exists = True
                            same_places, same_letter = retrieved_elements [0]
                            if letter != same_letter:
                                flag=True
                                break
                    if flag:
                        count+=1
                    if not constrain_exists:
                        break
        if count<min_count:
            best_word=word
            place=i
        i+=1
    return best_word, place


def chose_var(var_options, av_words):
    min=1000
    for var in var_options:
        retrieved_elements = list (filter (lambda x: var in x, av_words))
        possible_words = retrieved_elements[0][0]
        if not possible_words:
            return var
        else:
            if min>len(possible_words):
                min=len(possible_words)
                best_var=var
    return best_var


class Backtracking(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):

        M, N = np.shape(tiles)
        # Initialize a list of available words
        solution, stack_words, av_words, assigned, history, av_words_copy = [], [], [], [], [], []

        #Unar restrains
        av_words = [[[word for word in words if len (word) == length],pos] for pos,length in variables.items()]
        stack_words.append(av_words)

        # Loop through the variables in the puzzle
        while(len(assigned)<len(variables)):
            #var_options=[]
            for var, length in variables.items():
                if var not in [x[0] for x in assigned]:
                    #var_options.append(var)
                    break
            #var=chose_var(var_options, av_words)

            retrieved_elements = list(filter(lambda x: var in x, av_words))
            possible_words = retrieved_elements[0][0]
            #ako smo dosli do greske
            while not possible_words:
                av_words_copy=copy.deepcopy(av_words)
                domains = {y: x for x, y in av_words_copy}
                stack_words.pop()
                solution.append([var, None, domains])

                var, chosen_word = assigned.pop()
                av_words = stack_words [len (stack_words) - 1]
                for words, pos in av_words:
                    if pos == var and chosen_word in words:
                        words.remove(chosen_word)
                        break
                retrieved_elements = list(filter(lambda x: var in x, av_words))
                possible_words = retrieved_elements[0][0]
                av_words = copy.deepcopy(stack_words [len (stack_words) - 1])

            #fja koja bira promenljivu
            chosen_word, chosen_index = choose_word(possible_words)

            #ispis u solution

            av_words_copy=copy.deepcopy(av_words)
            domains = {y: x for x, y in av_words_copy}
            solution.append([var, chosen_index, domains])
            assigned.append([var, chosen_word])

            #duboko kopiranje
            av_words_old=av_words
            av_words=copy.deepcopy(av_words_old)

            #izbacivanje reci iz av_words
            for words, pos in av_words:
                if pos == var and chosen_word in words:
                    words.remove (chosen_word)
                    break

            #dodavanje novih ogranicenja
            coord=getCoordinates(var, chosen_word,M,N)
            for words, val in av_words:
                if val not in [z [0] for z in assigned]:

                    removed_list=[]
                    for word in words:
                        coord1=getCoordinates(val, word, M,N)
                        for place, letter in coord:
                            retrieved_elements = list(filter(lambda x: place in x, coord1))
                            if len(retrieved_elements)>0:
                                same_places, same_letter=retrieved_elements[0]
                                if letter!=same_letter:
                                    removed_list.append(word)
                    for word in removed_list:
                        words.remove(word)

            stack_words.append(av_words)
        return solution

class Forwardchecking(Algorithm):
    def get_algorithm_steps(self, tiles, variables, words):
        # Initialize a list of available words
        solution, stack_words, av_words, assigned, history, av_words_copy = [], [], [], [], [], []
        M, N = np.shape(tiles)
        flag=False

        av_words = [[[word for word in words if len (word) == length],pos] for pos,length in variables.items()]
        stack_words.append(av_words)
        # Loop through the variables in the puzzle
        while(len(assigned)<len(variables)):
        #for var, length in variables.items():
            for var, length in variables.items():
                if var not in [x[0] for x in assigned]:
                    break

            retrieved_elements = list(filter(lambda x: var in x, av_words))
            possible_words = retrieved_elements[0][0]
            #ako smo dosli do greske
            while not possible_words:
                av_words_copy=copy.deepcopy(av_words)
                domains = {y: x for x, y in av_words_copy}
                stack_words.pop()
                solution.append([var, None, domains])
                var, chosen_word = assigned.pop()
                av_words = stack_words [len (stack_words) - 1]
                for words, pos in av_words:
                    if pos == var and chosen_word in words:
                        words.remove(chosen_word)
                        break
                retrieved_elements = list(filter(lambda x: var in x, av_words))
                possible_words = retrieved_elements[0][0]
                import copy
                av_words = copy.deepcopy(stack_words [len (stack_words) - 1])

            #fja koja bira promenljivu
            chosen_word, chosen_index = choose_word(possible_words)

            #ispis u solution
            av_words_copy=[]
            import copy
            av_words_copy=copy.deepcopy(av_words)
            domains = {y: x for x, y in av_words_copy}
            solution.append([var, chosen_index, domains])
            assigned.append([var, chosen_word])

            #duboko kopiranje
            av_words_old=av_words
            import copy
            av_words=copy.deepcopy(av_words_old)

            #izbacivanje reci iz av_words
            for words, pos in av_words:
                if pos == var and chosen_word in words:
                    words.remove(chosen_word)
                    break

            #dodavanje novih ogranicenja
            pos=int(var[0])
            orientation=var[1]
            coord=getCoordinates(var, chosen_word,M,N)
            for words, val in av_words:
                if val not in [z [0] for z in assigned]:

                    removed_list=[]
                    for word in words:
                        coord1=getCoordinates(val, word, M,N)
                        for place, letter in coord:
                            retrieved_elements = list(filter(lambda x: place in x, coord1))
                            if len(retrieved_elements)>0:
                                same_places, same_letter=retrieved_elements[0]
                                if letter!=same_letter:
                                    removed_list.append(word)
                    for word in removed_list:
                        words.remove(word)
            flag=False

    #forward checking
            for words, values in av_words:
                if values not in  [x[0] for x in assigned] and len(words)==0 and not flag:
                    flag=True
                    av_words_copy=copy.deepcopy(av_words)
                    domains = {y: x for x, y in av_words_copy}
                    sol = [var, None, domains]
                    retrieved_elements = list (filter (lambda x: var in x, av_words))
                    possible_words = retrieved_elements [0] [0]
                    if not possible_words:
                        pass
                    else:
                        solution.append(sol)
                    assigned.pop()
                    av_words=av_words_old
                    for words1, pos1 in av_words:
                        if pos1 == var:
                            words1.remove(chosen_word)
                            break
                if flag:
                    stack_words.pop()
                    break
            stack_words.append(av_words)
        return solution


def arc_consistency(word1, words2, var1, var2, M, N):
    options=len(words2)
    coord1=getCoordinates(var1,word1,M,N)
    constrain_exists=False
    for word2 in words2:
        resolved=False
        re = 0
        coord2=getCoordinates(var2,word2,M,N)
        for place, letter in coord1:
            retrieved_elements = list (filter (lambda x: place in x, coord2))
            if len (retrieved_elements) > 0 and not resolved:
                constrain_exists=True
                same_places, same_letter = retrieved_elements[0]
                if letter != same_letter:
                    options_prev=options
                    options-=1
                    resolved=True
            if options==0:
                return False
        if not constrain_exists:
            return True
    return True

class ArcConsistency(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):

        M, N = np.shape(tiles)
        # Initialize a list of available words
        solution, stack_words, av_words, assigned, history, av_words_copy = [], [], [], [], [], []

        av_words = [[[word for word in words if len (word) == length],pos] for pos,length in variables.items()]
        stack_words.append(av_words)
        # Loop through the variables in the puzzle
        while(len(assigned)<len(variables)):
        #for var, length in variables.items():
            for var, length in variables.items():
                if var not in [x[0] for x in assigned]:
                    break

            retrieved_elements = list(filter(lambda x: var in x, av_words))
            possible_words = retrieved_elements[0][0]
            #ako smo dosli do greske
            while not possible_words:
                av_words_copy=copy.deepcopy(av_words)
                domains = {y: x for x, y in av_words_copy}
                stack_words.pop()
                solution.append([var, None, domains])
                #ovde imam problem kad se vracam nekoliko puta, udje u krug, tako da moram da pamtim sve koje je vec probao i da
                #ih izbrisem u vracanju
                if len(assigned)>0:
                    var, chosen_word = assigned.pop()
                else:
                    print('error')
                av_words = stack_words[len(stack_words) - 1]
                for words, pos in av_words:
                    if pos == var:
                        words.remove(chosen_word)
                retrieved_elements = list(filter(lambda x: var in x, av_words))
                possible_words = retrieved_elements[0][0]
                av_words = copy.deepcopy(stack_words [len (stack_words) - 1])

            #fja koja bira promenljivu
            chosen_word, chosen_index = choose_word(possible_words)

            #ispis u solution
            av_words_copy=copy.deepcopy(av_words)
            domains = {y: x for x, y in av_words_copy}
            solution.append([var, chosen_index, domains])
            assigned.append([var, chosen_word])

            #duboko kopiranje
            av_words_old=av_words
            av_words=copy.deepcopy(av_words_old)

            #izbacivanje reci iz av_words
            for words, pos in av_words:
                if pos==var:
                        words.remove(chosen_word)
                        break

            #dodavanje novih ogranicenja
            pos=int(var[0])
            orientation=var[1]
            coord=getCoordinates(var, chosen_word,M,N)
            for words, val in av_words:
                if val not in [z [0] for z in assigned]:
                    removed_list=[]
                    for word in words:
                        coord1=getCoordinates(val, word, M,N)
                        for place, letter in coord:
                            retrieved_elements = list(filter(lambda x: place in x, coord1))
                            if len(retrieved_elements)>0:
                                same_places, same_letter=retrieved_elements[0]
                                if letter!=same_letter:
                                    removed_list.append(word)
                    for word in removed_list:
                        words.remove(word)

                # forward checking
            flag=False
            for words, values in av_words:
                if values not in [x [0] for x in assigned] and len (words) == 0 and not flag:
                    flag = True
                    av_words_copy = copy.deepcopy (av_words)
                    domains = {y: x for x, y in av_words_copy}
                    sol = [var, None, domains]
                    retrieved_elements = list (filter (lambda x: var in x, av_words))
                    possible_words = retrieved_elements [0] [0]
                    if not possible_words:
                        pass
                    else:
                        solution.append(sol)
                    assigned.pop ()
                    av_words = av_words_old
                    for words1, pos1 in av_words:
                        if pos1 == var:
                            words1.remove (chosen_word)
                            break
                    if flag:
                        stack_words.pop ()
                        break
            #arc consisntency

            #uzmi sve reci i jednu vrednost od reci koje su ostale slobodne
            flag1=False
            for words, values in av_words:
                if flag:
                    break
                if values not in  [x[0] for x in assigned]:
                    #rec za koju analiziramo se zove arc_word
                    for words1, values1 in av_words:
                        removed_list=[]
                        if values1 not in  [x[0] for x in assigned] and values1!=values: #uzmemo drugu rec sa kojom proveravamo i njena opcije tj reci words2
                            for word in words:
                                if not arc_consistency(word, words1,values, values1,M,N):
                                    removed_list.append(word)
                            for word in removed_list:
                                words.remove(word)
            stack_words.append(av_words)
        return solution
