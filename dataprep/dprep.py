import json 

class DataPrep():
"""
This class is used to process the dataset for the transformer

    Args : 
        max_seq (integer) : The number of sequences to be taken into consideration while preprocessing the data for the transformer
        converse (string) : The dataset path containing the conversation 
        movies_lines (string): The dataset path containing the movie lines
"""
    def __init__(self, max_seq, converse, movie_lines, ):
        
        self.max_seq =  max_seq
        self.converse =  converse
        self.movie_lines = movie_lines
    
    def remove_punct(self, sent):
        """
             Method used to remove the punctuation in the sentence

        Args
            sent (string) : The sentence for which the punctuation is to removed
        
        Returns :
            punc_less (string) : The resultant string with the punctuations removed
        """
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        punc_less = ""
        for ch in sent:
            if ch not in punc:
                punc_less += ch # consider the edge case where the space is also a character
        return punc_less.lower()



    def load_data_and_process(self):
        """
            Method used to  Loads the data

            Returns:
             qpairs (dict) : Returns question and pairs in a processed dictionary
        """
        with open(self.converse, 'r') as con:
            conv = con.readlines()
        with open(self.movies_lines, 'r') as mov:
            movies = mov.readlines()
            
        
        # Split around the pattern
        lines_dc = {}
        for l in movies:
            data = movies.split('+++$+++')
            line_dc[data[0]] = data[-1]
        
        # Process the data in the pairs of questions and pairs
        qpairs = []
        for con in self.converse:
            l_id = eval(con.split("+++$+++")[-1])
            for idx in range(len(l_id)):
                qa = []

                # reached the end of the lines
                if idx == len(l_id)-1:
                    break

                fqa = self.remove_punct(lines_dc[l_id[idx]].strip())
                sqa = self.remove_punct(lines_dc[l_id[idx+1]].strip())
                qa.append(fqa.split()[:self.max_seq])
                qa.append(sqa.split()[:self.max_seq])
                qpairs.append(qa)
        
        return qpairs



    def word_counter(self, pairs):
        """
        Method used to update the word frq for each pairs

        Args :
            pairs (dict) : Dictionary consisting of questions and pairs

        Returns:
            word_fr (dict) : Returns the count of each words that are ocurring in the dataset
        """
        word_fr = Counter()
        for pa in pairs:
            word_fr.update(pairs[0])
            word_fr.update(pairs[1])

        return word_fr
        
    def word_mapping(self, word_freq):
        """
            Method used to form the word mapping based on the likehood of the word that is to occur
            
            Args:
                word_freq : The dictionary containing the word frequency 

            Returns :
                word_map (dict) :  The mapped version of the word mapping 
        """
        min_word_freq = 5
        words = [word in for word in word_freq.keys() if word_freq[word] > min_word_freq]
        word_map = {key:val + 1 for val, key in enumerate(words)}
        word_map['<unkn>'] = len(word_map) + 1
        word_map['<start>'] = len(word_map) + 1
        word_map['<end>'] = len(word_map) + 1
        word_map['<pad>'] = 0
        
        # dump the wordmap for future ref
        wirh open('word_map.json', 'w') as word:
            json.dumps(word_map, word)

        return word_map

