import urllib.request
import re
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
text1 = re.sub(strippables, ' ',text1)
text1 = text1.lower()
text2 = re.sub(strippables, ' ',text2)
text2 = text2.lower()

"""
Define the function cout_words that takes in a text file and return a dictionary with 
the words as the key and how many times it occur in the text as the value
"""
def count_words(book):
    word_count = {}     # define a dictionary
    for i in book.split():      # create a loop for the list that is created by spliting the string by white space
        word_count[i] = word_count.get(i,0)+1       #count the word in the dictionary
    return word_count   #return the word count

"""
Define the function ranked_words that takes in a dictionary in the format that is outputed by count_words 
the function returns a dictionary with words as key and times it 
"""
def ranked_words(dic):
    sorted_values = sorted(dic.values(),reverse=True) # Sort the values
    sorted_dict = {}

    for i in sorted_values:
        for k in dic.keys():
            if dic[k] == i:
                sorted_dict[k] = dic[k]

    return(sorted_dict)


def top_x_words(dic,x):
    sorted_values = sorted(dic.values(),reverse=True) # Sort the values
    sorted_dict = {}
    sorted_top = []
    for i in range(10):
        sorted_top.append(sorted_values[i])

    for i in sorted_top:
        for k in dic.keys():
            if dic[k] == i:
                sorted_dict[k] = dic[k]

    return(sorted_dict)

def compare_top_x(dict_1,dict_2,x):
    d1 = top_x_words(dict_1,x)
    d2 = top_x_words(dict_2,x)
    l = []
    for key in d1:
        if key not in d2.keys():
            l.append(key)
    for key in d2:
        if key not in d1.keys():
            l.append(key)
    no_dup_list = []
    for i in l:
        if i not in no_dup_list:
            no_dup_list.append(i)
    return no_dup_list

def sentiment_analysis(nltk_text):
    import nltk
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sentence = nltk_text
    score = SentimentIntensityAnalyzer().polarity_scores(sentence)
    return score

def compare_sentiment(nltk_text1, nltk_text2):
    d1 = sentiment_analysis(nltk_text1)
    d2 = sentiment_analysis(nltk_text2)
    d3 = {}
    for key in d1:
        d3[key] = d1[key] - d2[key]
    return d3

def main():
    book = text1
    print(f'the word count for book 1 is: {count_words(book)}')
    
    dic = count_words(book)
    print(f'the rank of work occur in book 1 is: {ranked_words(dic)}')
    
    x = 10
    print(f'the top {x} occured word in book 1 is: {top_x_words(dic,x)}')
    
    dict_1 = count_words(text1)
    dict_2 = count_words(text2)
    print(f'the difference of top {x} word for book 1 and book 2 is: {compare_top_x(dict_1,dict_2,x)}')

    print(f'the sentiment analysis for book 1 is {sentiment_analysis(nltk_text1)}')
    print(f'the sentiment analysis for book 2 is {sentiment_analysis(nltk_text2)}')

    print(f'the diffence in the scores of sentiment analysis between book 1 and 2 is: {compare_sentiment(nltk_text1, nltk_text2)}')
if __name__ == "__main__":
    main()
