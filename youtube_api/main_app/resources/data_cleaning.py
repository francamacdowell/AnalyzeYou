import sys
sys.path.append('../../..')
import re
import string
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import unicodedata
from unidecode import unidecode


class DataCleaning:
    def __init__(self):
        self.tokens_list = list()
        self.vocabulary = list()
        self.all_words = list()
        self.emoticons_str = r"""
                    (?:
                        [:=;] # Eyes
                        [oO\-]? # Nose (optional)
                        [D\)\]\(\]/\\OpP] # Mouth
                    )"""
        self.regex_str = [
            self.emoticons_str,
            r'<[^>]+>',  # HTML tags
            r'(?:@[\w_]+)',  # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
            r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
            r'(?:[\w_]+)',  # other words
            r'(?:\S)'  # anything else
        ]
        self.tokens_re = re.compile(r'(' + '|'.join(self.regex_str) + ')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile("["u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)

    def steps_control_to_cleaning_dataset(self, comments):
        for i in comments:
            self.de_emojify(i)

        for i in range(0, len(self.tokens_list)):
            self.tokens_list[i] = self.lemmatization(self.tokens_list[i])

        """self.vocabulary = self.generate_pos_tag_to_tokens(self.vocabulary)
        counter = Counter(self.vocabulary).most_common()
        percent = int(counter[0][1] - (counter[0][1] * 0.95))
        self.vocabulary = [term[0] for term in counter if term[1] >= percent]

        for i in self.tokens_list:
            i = self.generate_pos_tag_to_tokens(i)

        self.vocabulary = self.lemmatization(self.vocabulary)
        return self.vocabulary"""

    def de_emojify(self, comment):
        tokens = self.pre_process(comment)
        tokens = self.remove_stop_words(tokens)

        tokens_aux = list()
        for i in tokens:
            try:
                i.encode('ascii')
                self.vocabulary.append(i)
                tokens_aux.append(i)
            except UnicodeEncodeError:
                break

        self.tokens_list.append(tokens_aux)

    def pre_process(self, my_string):
        tokens = self.tokenize(my_string)
        tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    def tokenize(self, s):
        return self.tokens_re.findall(s)

    def generate_pos_tag_to_tokens(self, tokens):
        tags = ['JJ', 'JJR', 'JJS', 'RB', 'RBS', 'RBR']
        tokens_tags = nltk.pos_tag(tokens)
        result = list()

        for i in tokens_tags:
            if i[1] in tags:
                result.append(i[0])

        return result

    def lemmatization(self, tokens):
        new_tokens = list()
        lem = WordNetLemmatizer()
        for i in tokens:
            lemma = lem.lemmatize(i)
            new_tokens.append(lemma)
            self.all_words.append(lemma)
        return new_tokens

    def remove_stop_words(self, tokens):
        stop = stopwords.words('english') + list(string.punctuation) + ['...', '<', ':']
        return [term.lower() for term in tokens if term not in stop and not term.startswith(('#', '@')) and not term.isnumeric()]

