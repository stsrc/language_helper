#!/usr/bin/python3

import json
import glob
import random 

import speech_recognition as sr

import os, sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def mark_as_difficult(data, english_verb, file_object, data_category):
    difficult = data[data_category]
    if english_verb in difficult:
        return

    difficult.append(english_verb)
    file_object.truncate(0)
    file_object.seek(0)
    json.dump(data, file_object, indent = 8, ensure_ascii = False)

def remove_from_difficult(data, english_verb, file_object, data_category):
    difficult = data[data_category]
    for idx, obj in enumerate(difficult):
        if obj == english_verb:
            difficult.pop(idx)
    file_object.truncate(0)
    file_object.seek(0)
    json.dump(data, file_object, indent = 8, ensure_ascii = False)

def learn_czech_difficult_verbs(data, file_object):
    keys = ["infinitiv", "já", "ty", "on/ona/ono", "my", "vy", "oni/ony/ona"] 
    verbs = data['verbs']
    difficult_verbs = data['difficult verbs']
    if not difficult_verbs:
        print("difficult verbs list is empty, aborting")
        return

    while(1):
        english_verb = random.choice(difficult_verbs)
        czech_verbs = verbs[english_verb]
        key = random.randint(0, len(keys) - 1)
        splited_czech_verbs = czech_verbs.split(', ')
        print_string = english_verb + ", " + keys[key] + ": "
        input_char = input(print_string)
        if (input_char == 'h'):
            print(splited_czech_verbs[0])
            input(print_string)
        print('\n\033[92m' + splited_czech_verbs[key] + '\033[0m')
        input_char = input("\nShow all - a; Remove from difficult - b; Next - any key: ")
        if (input_char == 'a'):
            print('\n')
            print(splited_czech_verbs)
            input_char = input("\nRemove from difficult - 'b'; Next - any key: ")
        if (input_char == 'b'):
            remove_from_difficult(data, english_verb, file_object, 'difficult verbs')
        print()
        
def learn_czech_verbs(data, file_object):
    keys = ["infinitiv", "já", "ty", "on/ona/ono", "my", "vy", "oni/ony/ona"] 
    verbs = data['verbs']
    while(1):
        english_verb, czech_verbs = (random.choice(list(verbs.items())))
        key = random.randint(0, len(keys) - 1)
        splited_czech_verbs = czech_verbs.split(', ')
        print_string = english_verb + ", " + keys[key] + ": "
        input_char = input(print_string)
        if (input_char == 'h'):
            print(splited_czech_verbs[0])
            input(print_string)
        print('\n\033[92m' + splited_czech_verbs[key] + '\033[0m')
        input_char = input("\nShow all - 'a'/'h'; Mark as difficult - 'b'; Next - any key: ")
        if (input_char == 'a' or input_char == 'h'):
            print("")
            print(splited_czech_verbs)
            input_char = input("\nMark as difficult - 'b'; Next - any key: ")
        if (input_char == 'b'):
            mark_as_difficult(data, english_verb, file_object, 'difficult verbs')
        print()

def learn_czech(filename):
    file_object = open(filename, 'r+')
    parsed_json = json.load(file_object)
    print("What would you like to learn?")
    for i in parsed_json:
        choice = input(i + "? y/n: ").lower()
        if (choice == 'y'):
            if (i == 'verbs'):
                learn_czech_verbs(parsed_json, file_object)
                break
            elif (i == 'difficult verbs'):
                learn_czech_difficult_verbs(parsed_json, file_object)
                break

def learn_english_words(data, category, file_object):
    words = data[category]
    while(1):
        answer, question = (random.choice(list(words.items())))
        print_string = '\n' + question + ": "
        input(print_string)
        print('\n\033[92m' + answer + '\033[0m\n')
        input_char = input("Mark as difficult - 'b'; Next - any key: ")
        if (input_char == 'b'):
            mark_as_difficult(data, answer, file_object, 'difficult words')

def learn_english_difficult_words(data, category, file_object):
    words = data['words and phrases to english']
    difficult_words = data['difficult words']
    if not difficult_words:
        print("difficult words list is empty, aborting")
        return

    while(1):
        difficult_word = random.choice(difficult_words)
        question = words[difficult_word]
        print_string = '\n' + question + ": "
        input_char = input(print_string)
        print('\n\033[92m' + difficult_word + '\033[0m\n')
        input_char = input("Unmark from difficult - 'b'; Next - any key: ")
        if (input_char == 'b'):
            remove_from_difficult(data, difficult_word, file_object, 'difficult words')

def learn_english_words_sr():
    r = sr.Recognizer()
    while(1):
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            try:
                print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

def learn_english(filename):
    file_object = open(filename, 'r+')
    parsed_json = json.load(file_object)
    choice = input("\nWhat would you like to learn?\nSpeach recognition mode? y/n: ").lower()
    if (choice == 'y'):
        learn_english_words_sr()

    for i in parsed_json:
        choice = input(i + "? y/n: ").lower()
        if (i == 'words and phrases to english' and choice == 'y'):
            learn_english_words(parsed_json, i, file_object)
        elif (i == 'difficult words' and choice == 'y'):
            learn_english_difficult_words(parsed_json, i, file_object)

def main():
    print("Which language would you like to learn?")
    files = glob.glob("*.json")
    choice = input(files[0] + "? y/n: ").lower()
    if (choice == 'y'):
        learn_czech(files[0])
    else:
        choice = input(files[1] + "? y/n: ").lower()
        if (choice == 'y'):
            learn_english(files[1])

if __name__ == "__main__":
    main()
