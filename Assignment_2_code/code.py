import urllib.request
import re
import matplotlib.pyplot as plt
import nltk     #install the package
nltk.download('vader_lexicon')      #download the necessary package

"""open the stop_words document"""
stop_words = open('stop_words.txt')
"""create a new list"""
stop_list = []
"""put the stop words to a list which can be used as for the in logistics"""
for line in stop_words:
    stop_list.append(line.strip())
print(stop_list)

"""open the text file with the url and decode the data in the format of UTF-8 and store it into text1 and nltk_text1"""
url1 = 'https://www.gutenberg.org/cache/epub/66627/pg66627.txt'
response = urllib.request.urlopen(url1)
data1 = response.read()
text1 = data1.decode('utf-8')
nltk_text1 = data1.decode('utf-8')

"""open the text file with the url and decode the data in the format of UTF-8 and store it into text2 and nltk_text2"""
url2 = 'https://www.gutenberg.org/cache/epub/66623/pg66623.txt'
response = urllib.request.urlopen(url2)
data2 = response.read()
text2 = data2.decode('utf-8')
nltk_text2 = data2.decode('utf-8')
"""define the veriable strippables, which are the special characters that can be stripped form the text"""
strippables = r"(?:s|'s|!+|,|\.|;|:|\(|\)|\"|\?+)?\s"

"""subtitude the strippables with white space, and make all letters into lower cases"""
text1 = re.sub(strippables, ' ', text1)
text1 = text1.lower()
text2 = re.sub(strippables, ' ', text2)
text2 = text2.lower()

"""
Define the function cout_words that takes in a text file and return a dictionary with 
the words as the key and how many times it occur in the text as the value
"""


def count_words(book):
    word_count = {}     # define a dictionary
    for i in book.split():      # create a loop for the list that is created by spliting the string by white space
        # count the word in the dictionary
        if i in stop_list:
            continue
        else:
            word_count[i] = word_count.get(i, 0)+1
    return word_count  # return the word count


"""
Define the function ranked_words that takes in a dictionary in the format that is outputed by count_words 
the function will be able to sort the dictionary by values in the reverse format from the largest to the smallest.
"""


def ranked_words(dic):
    # Sort the values in reverse
    sorted_values = sorted(dic.values(), reverse=True)
    sorted_dict = {}  # create a dictionary

    for i in sorted_values:     # loop in the sorted_value list
        for k in dic.keys():    # loop in the dictionary keys
            if dic[k] == i:     # Reverse search for the value in dictionary
                # put the key value pair in the dictionary
                sorted_dict[k] = dic[k]

    return(sorted_dict)  # return the dictionary


"""
Define the function top_x_words that takes in a dictionary in the format that is outputed by count_words 
the function will be able to sort the dictionary by values in the reverse format from the largest to the smallest and return the top
10 words that occur the most in the book.
"""


def top_x_words(dic):
    # Sort the values in reverse
    sorted_values = sorted(dic.values(), reverse=True)
    sorted_dict = {}  # create a dictionary
    sorted_top = []     # create a list
    for i in range(10):     # loop 10 times to put the top 5 values into the new list
        sorted_top.append(sorted_values[i])

    for i in sorted_top:    # look in the new list
        for k in dic.keys():  # look in the dictionary key to reverse search the top 10 from the new list
            if dic[k] == i:
                sorted_dict[k] = dic[k]

    return(sorted_dict)     # return the dictionary


"""
Define a funtion compare_top_x to compare the top 10 words for two books and output the words in the top 10 of each book
that is not in the top 10 of the other. The function takes in two arguements which are dictionaries in the format of the out put 
of count_words.

"""


def compare_top_x(dict_1, dict_2):
    d1 = top_x_words(dict_1)        # find the top 10 words of book 1
    d2 = top_x_words(dict_2)        # finf the top 10 words of book 2
    l = []      # create a new list
    for key in d1:      #loop in the top 10 dictionary of book 1
        if key not in d2.keys():    #append the key of dictionary in 1 that is not in 2 to the list
            l.append(key)
    for key in d2:      #loop in the top 10 dictionary of book 2
        if key not in d1.keys():    #append the key of dictionary in 2 that is not in 1 to the list
            l.append(key)
    no_dup_list = []        #Create a new list
    for i in l:     #loop in the new list
        if i not in no_dup_list:    #remove the duplicate in the list l and put it in the new list no_dup_list
            no_dup_list.append(i)
    return no_dup_list      #return the new list

"""
Define a function sentiment_analysis that takes in the book text as the arguement and analize the sentiment of the book
"""
def sentiment_analysis(nltk_text):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer     #import the sentiment analysis function

    sentence = nltk_text    #set veriable sentence equals to the input text
    score = SentimentIntensityAnalyzer().polarity_scores(sentence)      #calculate the score of sentiment and store it in score
    return score    #return the score

"""
Define a function compare_sentiment to compare the sentiment score of two books by using the score of book 1 subtracting the score
of book 2. The function takes in two arguments that are the book texts as the arguement
"""
def compare_sentiment(nltk_text1, nltk_text2):
    d1 = sentiment_analysis(nltk_text1)     #Create a dictionary d2 to store the sentiment score of the book 1
    d2 = sentiment_analysis(nltk_text2)     #Create a dictionary d1 to store the sentiment score of the book 2
    d3 = {}     #Create a new dictionary
    for key in d1:  #loop the keys in d1
        d3[key] = d1[key] - d2[key]     #make d3 have the same key and values as the difference between the values of d1 and d2
    return d3      #return d3


def main():
    book = text1
    print(f'the word count for book 1 is: {count_words(book)}')

    dic = count_words(book)
    dic2 = count_words(text2)
    print(f'the rank of work occur in book 1 is: {ranked_words(dic)}')

    print(f'the top 10 occured word in book 1 is: {top_x_words(dic)}')
    print(f'the top 10 occured word in book 2 is: {top_x_words(dic2)}')
    
    top1 = top_x_words(dic)
    top2 = top_x_words(dic2)
    
    keys1 = top1.keys()
    values1 = top1.values()
    keys2 = top2.keys()
    values2 = top2.values()
    
    plt.bar(keys1, values1)
    plt.savefig('b.png')

    dict_1 = count_words(text1)
    dict_2 = count_words(text2)
    print(
        f'the difference of top 10 word for book 1 and book 2 is: {compare_top_x(dict_1,dict_2)}')

    print(
        f'the sentiment analysis for book 1 is {sentiment_analysis(nltk_text1)}')
    print(
        f'the sentiment analysis for book 2 is {sentiment_analysis(nltk_text2)}')

    print(
        f'the diffence in the scores of sentiment analysis between book 1 and 2 is: {compare_sentiment(nltk_text1, nltk_text2)}')


if __name__ == "__main__":
    main()
