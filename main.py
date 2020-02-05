from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, run_async, PicklePersistence
import requests
import random
import sys
import asyncio
import telepot

SOWPODS_FILE = "sowpods.txt"
ANIMAL_FILE = "animals.txt"
STATIONERY_FILE = "stationary.txt"


class HangManBot():
    def __init__(self, *args, **kwargs):
        #my_persistence = PicklePersistence(filename='my_file')
        updater = Updater('1045683428:AAED1-6AFyjiXAd-sPxhBvCPtZ1Bb2bqW00')
        self.choice_flag = 0
        self.started_flag = False
        self.word = ""
        self.found_letters = []
        self.incorrect_guesses = []
        self.correct_count = 0
        self.number_of_tries = 6
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('random', self.choice))
        dp.add_handler(MessageHandler(Filters.text, self.main_game))
        dp.add_handler(CommandHandler('animals',self.choice))
        dp.add_handler(CommandHandler('stationeries',self.choice))
        updater.start_polling()
        updater.idle()
    
    def random_word(self, filename=SOWPODS_FILE):
        f = open(filename, 'r')
        lines = f.readlines()
        word = random.choice(lines).strip()
        f.close()
        #print(word)
        return word

    def random_animal(self, filename=ANIMAL_FILE):
        f = open(filename, 'r')
        lines = f.readlines()
        word = random.choice(lines).strip()
        f.close()
        #print(word)
        return word

    def random_stat(self, filename=STATIONERY_FILE):
        f = open(filename, 'r')
        lines = f.readlines()
        word = random.choice(lines).strip()
        f.close()
        #print(word)
        return word

    def start(self, bot, update):  # choose category
        chat_id = update.message.chat_id
        update.message.reply_text('Choose a category: \n 1: /random \n 2: /animals \n 3: /stationeries')

    def choice(self, bot, update):
        print(update.message.text)
        if '/random' in update.message.text:
            self.choice_flag = 1
        elif '/animals' in update.message.text:
            self.choice_flag = 2
        elif '/stationeries' in update.message.text:
            self.choice_flag = 3
        self.main_game(bot, update)

    def main_game(self, bot, update):
        if self.choice_flag == 1:
            self.randomWord(bot, update)
        elif self.choice_flag == 2:
            # 2nd game
            self.animals(bot, update)
        elif self.choice_flag == 3:
            # 3rd game
            self.stat(bot, update)
        else:
            # no game selected
            print("No game selected")

    def reset_game(self):
        self.choice_flag = 0
        self.started_flag = False
        self.word = ""
        self.found_letters = []
        self.incorrect_guesses = []
        self.correct_count = 0
        self.number_of_tries = 6

    def randomWord(self, bot, update):
        if not self.started_flag:
            self.word = self.random_word()
            self.started_flag = True
            update.message.reply_text("Category chosen: Random word \n Uncover the mystery word by guessing the letters it contains.")
            update.message.reply_text(
                ''.join([a + ' ' if a in self.found_letters else '_ ' for a in self.word]))
        elif self.started_flag:
            c = update.message.text.upper()
            #print(c)
            if len(c) != 1:
                update.message.reply_text("Enter one letter at a time")
            if c.isalpha():
                if c in self.incorrect_guesses or c in self.found_letters:
                    update.message.reply_text("You already tried that.")    
            else:
                update.message.reply_text("Must be between a-z.")
            if self.correct_count < len(self.word) and len(self.incorrect_guesses) < self.number_of_tries:
                if c in self.word:
                    self.found_letters.append(c)
                    self.correct_count += self.word.count(c)
                else:
                    if c not in self.incorrect_guesses and c.isalpha and len(c) == 1: #changes
                        self.incorrect_guesses.append(c)
                if len(self.incorrect_guesses) != 0:
                    update.message.reply_text("Incorrect guesses:"+", ".join(self.incorrect_guesses))
                    update.message.reply_text("{} guesses left".format(
                        self.number_of_tries - len(self.incorrect_guesses)))
                    if len(self.incorrect_guesses) < self.number_of_tries: #changes
                        update.message.reply_text("Guess a new letter:")
                update.message.reply_text(
                    ''.join([a + ' ' if a in self.found_letters else '_ ' for a in self.word]))
            if self.correct_count == len(self.word):  
                #print("Correct")
                update.message.reply_text(self.word)
                update.message.reply_text("Correct.  Well done!")
                self.reset_game()
            if len(self.incorrect_guesses) >= self.number_of_tries:
                #print("Wrong")
                update.message.reply_text("FKING LOSER!  You failed to guess the word.")
                update.message.reply_text("The word is " + self.word)
                self.reset_game()

    def animals(self, bot, update):
        if not self.started_flag:
            self.word = self.random_animal()
            self.started_flag = True
            update.message.reply_text("Category chosen: Animals\n Uncover the mystery word by guessing the letters it contains.")
            update.message.reply_text(
                ''.join([a + ' ' if a in self.found_letters else '_ ' for a in self.word]))
        elif self.started_flag:
            c = update.message.text.upper()
            #print(c)
            if len(c) != 1:
                update.message.reply_text("Enter one letter at a time")
            if c.isalpha():
                if c in self.incorrect_guesses or c in self.found_letters:
                    update.message.reply_text("You already tried that.")    
            else:
                update.message.reply_text("Must be between a-z.")
            if self.correct_count < len(self.word) and len(self.incorrect_guesses) < self.number_of_tries:
                if c in self.word:
                    self.found_letters.append(c)
                    self.correct_count += self.word.count(c)
                else:
                    if c not in self.incorrect_guesses and c.isalpha and len(c) == 1: #changes
                        self.incorrect_guesses.append(c)
                if len(self.incorrect_guesses) != 0:
                    update.message.reply_text("Incorrect guesses:"+", ".join(self.incorrect_guesses))
                    update.message.reply_text("{} guesses left".format(
                        self.number_of_tries - len(self.incorrect_guesses)))
                    if len(self.incorrect_guesses) < self.number_of_tries: #changes
                        update.message.reply_text("Guess a new letter:")
                update.message.reply_text(
                    ''.join([a + ' ' if a in self.found_letters else '_ ' for a in self.word]))
            if self.correct_count == len(self.word):
                #print("Correct")  
                update.message.reply_text(self.word)
                update.message.reply_text("Correct.  Well done!")
                self.reset_game()
            if len(self.incorrect_guesses) >= self.number_of_tries:
                #print("Wrong")
                update.message.reply_text("FKING LOSER!  You failed to guess the word.")
                update.message.reply_text("The word is " + self.word)
                self.reset_game()
    
    def stat(self, bot, update):
        if not self.started_flag:
            self.word = self.random_stat()
            self.started_flag = True
            update.message.reply_text("Category chosen: Stationeries \n Uncover the mystery word by guessing the letters it contains.")
            update.message.reply_text(
                ''.join([a + ' ' if a in self.found_letters else '_ ' for a in self.word]))
        elif self.started_flag:
            c = update.message.text.upper()
            #print(c)
            if len(c) != 1:
                update.message.reply_text("Enter one letter at a time")
            if c.isalpha():
                if c in self.incorrect_guesses or c in self.found_letters:
                    update.message.reply_text("You already tried that.")    
            else:
                update.message.reply_text("Must be between a-z.")
            if self.correct_count < len(self.word) and len(self.incorrect_guesses) < self.number_of_tries:
                if c in self.word:
                    self.found_letters.append(c)
                    self.correct_count += self.word.count(c)
                else:
                    if c not in self.incorrect_guesses and c.isalpha and len(c) == 1: #changes
                        self.incorrect_guesses.append(c)
                if len(self.incorrect_guesses) != 0:
                    update.message.reply_text("Incorrect guesses:"+", ".join(self.incorrect_guesses))
                    update.message.reply_text("{} guesses left".format(
                        self.number_of_tries - len(self.incorrect_guesses)))
                    if len(self.incorrect_guesses) < self.number_of_tries: #changes
                        update.message.reply_text("Guess a new letter:")
                update.message.reply_text(
                    ''.join([a + ' ' if a in self.found_letters else '_ ' for a in self.word]))
            if self.correct_count == len(self.word): 
                #print("Correct") 
                update.message.reply_text(self.word)
                update.message.reply_text("Correct.  Well done!")
                self.reset_game()
            if len(self.incorrect_guesses) >= self.number_of_tries:
                #print("Wrong")
                update.message.reply_text("FKING LOSER!  You failed to guess the word.")
                update.message.reply_text("The word is " + self.word)
                self.reset_game()

HangManBot()
