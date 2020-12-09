import sys
import wanakana
import time
import os
import pandas as pd
from random import randint
from google_speech import Speech
import re

# CONFIGURATION FILE
FILENAME_TXT="kotoba.txt"
DIRNAME, FILENAME = os.path.split(os.path.abspath(__file__))
DRIVER_DELAY = 0.5 # second(s)
N_TIMES = 3 #repetition

class Vocab:
    def __init__(self, filename, format_file):
        if(format_file=='txt'):
            with open(DIRNAME+"/"+filename, 'r', encoding="utf8") as reader:
                raw_data = reader.read().splitlines()
            self.__df=raw_data
        elif (format_file=='csv'):
            # not completed yet
            self.__df=pd.read_csv(filename, error_bad_lines=False)
        else:
            print('error')

    def __parse_txt(self, raw_data):
        en=[]
        jp=[]
        for idx in range (len(raw_data)):
            line = raw_data[idx]
            en.append(re.search('/(.+?)/', line).group(1))
            end=line.find(' ')
            jp.append(line[:end])
        list_of_tuples=list(zip(jp,en))
        return pd.DataFrame(list_of_tuples, columns=('jp', 'en'))
        
    def get_rand_vocab(self,):
        row_num = randint(0,len(self.__df)-1)
        jp=self.__df[row_num]
        print(row_num)
        print(jp)
        return jp
    
class Speaker:
    def __init__(self,):
        self.__vocab = Vocab(FILENAME_TXT, 'txt')

    def __driver(self, text, lang):
        speech=Speech(text, lang)
        sox_effects = ("speed", "1.0")
        speech.play(sox_effects)
        time.sleep(DRIVER_DELAY)

    def __driver_jp(self, text):
        self.__driver(text, "ja")

    def __driver_en(self, text):
        self.__driver(text, "en")
        
    def speak_jp_to_en(self, interval):
        jp=self.__vocab.get_rand_vocab()
        for idx in range(N_TIMES):
            self.__driver_jp(jp)
        time.sleep(interval)
                
    def speak_en_to_jp(self, interval):
        en,jp=self.__vocab.get_rand_vocab()
        for idx in range(N_TIMES):
            self.__driver_en(jp)
            self.__driver_jp(en)
        time.sleep(interval)
        
def main():
    arg=1
    try:
        if (arg==0):
            speaker=Speaker(DEFAULT_VOCAB_FILE)
        else:
            speaker=Speaker()
        while True:
            speaker=Speaker()
            speaker.speak_jp_to_en(DRIVER_DELAY)
    except KeyboardInterrupt:
        print("Interrupt")
        pass

if __name__ == '__main__':
    main()
