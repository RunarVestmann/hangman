from word_bank import WordBank
from score_data import ScoreData
import os
from datetime import date

SCORES_FILENAME = 'scores.txt'
WORDLIST_FILENAME = 'word_list.txt'

def get_menu_input():
    user_input = ''
    while not user_input.startswith('a') and not user_input.startswith('h')\
          and not user_input.startswith('p') and not user_input.startswith('q'):
        print('(A)dd word   (H)ighscores    (P)lay  (Q)uit')
        user_input = input('Enter a letter in the brackets: ').lower()

    return user_input

def prompt_user_to_add_a_word():
    new_word = input('Enter a word to add: ')
    while not new_word.isalpha():
        print('The word can only contain letters from the alphabet')
        new_word = input('Enter a word to add: ')
    add_new_word_to_file(new_word, WORDLIST_FILENAME)
    print("The word '{}' has been added".format(new_word))

def add_new_word_to_file(new_word, filename):
    f = open(filename, 'a+')

    #If the file is not empty we add a new line before adding the word
    f.seek(0)  
    if len(f.read(100)) > 0:
        f.write('\n')

    f.write(new_word)

    f.close()

def print_scores():
    f = open(SCORES_FILENAME, 'r')
    score_list= []

    #Add the lines in the file to a list
    for line in f:
        username, score, wins, losses, date = line.strip().split()
        score_list.append(ScoreData(username, int(score), wins, losses, date))

    #Sort the list and print it's contents
    for i,data in enumerate(sorted(score_list, key=lambda x: x.score, reverse=True)):
        print('{}. username: {:10} score: {:<10} wins: {:<10} losses: {:<10} date: {:<10}'.format(i+1, data.username,data.score,data.wins,data.losses,data.date))

    f.close()

def generate_word_bank_instance(filename):
    '''Returns a WordBank instance containing the words in the given file'''

    word_list = get_word_list_from_file(filename)
    last_modification_time = os.path.getmtime(filename)
    return WordBank(word_list, last_modification_time)

def prompt_user_for_max_guess_count():
    '''Returns the max amount of guesses the user has, keeps asking 
       the user for input while he does not enter an integer above zero'''

    max_guess_count = input('How many guesses will you have?: ')
    while not max_guess_count.isdigit() or int(max_guess_count) == 0:
        print('Please enter a positive integer above zero')
        max_guess_count = input('How many guesses will you have?: ')
    return int(max_guess_count)

def get_word_list_from_file(filename):
    f = open(filename, 'r')

    word_list = []
    for line in f:
        word_list.append(line.strip())

    f.close()
    return word_list

def show_progress(word, user_guess_set):
    '''Prints a representation of the word that the user is guessing'''

    progress_str = ''
    for letter in word.lower():
        if letter in user_guess_set:
            progress_str += letter
        else:
            progress_str += '-'
    print(progress_str)

def get_user_guess(count):
    return input('Enter guess number {}: '.format(count+1))

def prompt_user_to_guess(guess_count, user_guess_set):
    '''Returns the letter the user guessed, keeps asking the user to
       guess if he doesn't enter a single letter or has already guessed on the letter'''

    guess = get_user_guess(guess_count)
    while not guess.isalpha() or guess.lower() in user_guess_set:
        if not guess.isalpha():
            print('You can only enter letters in the alphabet')
            guess = get_user_guess(guess_count)
        elif guess.lower() in user_guess_set:
            print('You have already guessed: ' + guess)
            guess = get_user_guess(guess_count)
 
    return guess

def is_the_game_won(word, user_guess_set):
    '''Returns True if the game is won, returns False otherwise'''

    for letter in word:
        if letter not in user_guess_set:
            return False
    return True

def save_score(username, score, wins, losses):
    '''Saves a given score to the score file'''

    f = open(SCORES_FILENAME, 'a+')

    #If the file is not empty we add a new line before appending to the file
    f.seek(0)
    if len(f.read(100)) > 0:
        f.write('\n')

    f.write(f'{username} {score} {wins} {losses} {date.today()}')

    f.close()

def prompt_for_username():
    '''Returns the username the user inputs'''

    username = input('Enter your username: ')
    while len(username) > 10:
        print('The username can not be longer then 10 characters')
        username = input('Enter your username: ')
    return username

def play_game():
    #Store the words in the file in an instance of the WordBank class
    word_bank = generate_word_bank_instance(WORDLIST_FILENAME)

    user_wants_to_play = True
    username = prompt_for_username()
    
    total_wins = total_losses = 0
    total_guess_count = 0
    score = 0

    while user_wants_to_play:
        #If the words in the word bank are outdated we read the words from the file again
        if os.path.getmtime(WORDLIST_FILENAME) > word_bank.get_time_of_last_modification():
            word_bank = generate_word_bank_instance(WORDLIST_FILENAME)

        print('New game started!')

        game_won = False
        max_guess_count = prompt_user_for_max_guess_count()
        word_to_guess = word_bank.get_random_word()

        user_guess_count = 0

        user_guess_set = set()

        while user_guess_count < max_guess_count and not game_won:
            show_progress(word_to_guess, user_guess_set)

            guess = prompt_user_to_guess(user_guess_count, user_guess_set)

            user_guess_count += 1

            #If the user guesses the entire word correctly we break out of the loop
            if guess == word_to_guess:
                for letter in word_to_guess:
                    user_guess_set.add(letter)
                game_won = True
                break

            #Store all the guesses in a set
            user_guess_set.add(guess.lower())

            #Check if the game has been won and store the result
            game_won = is_the_game_won(word_to_guess, user_guess_set)

        show_progress(word_to_guess, user_guess_set)

        if(game_won):
            total_wins += 1
            print('Congratulations, you won the game!')
        else:
            total_losses += 1
            print('You ran out of guesses so you lost the game')

        total_guess_count += user_guess_count
        score = (total_wins * 5) - (total_guess_count // int((total_wins+total_losses) * 2)) - total_losses
        if score < 0:
            score = 0
        print(f'Score: {score} Wins:{total_wins} Losses: {total_losses}')

        input_str = input('Want to play again? (y/n): ').strip().lower()

        #Keep asking for a new input while the input is not a clear command
        while not input_str.startswith('y') and not input_str.startswith('n'):
            print("Please enter 'y' to play again or 'n' to quit")
            input_str = input('Want to play again? (y/n): ').strip().lower()

        if input_str.startswith('y'):
            user_wants_to_play = True
        else:
            save_score(username, score, total_wins, total_losses)
            print('Your score was saved successfully!')
            user_wants_to_play = False
    
def main():
    menu_input = get_menu_input()

    while menu_input != 'q':
        if menu_input == 'a':
            prompt_user_to_add_a_word()
        elif menu_input == 'h':
            print_scores()
        elif menu_input == 'p':
            play_game()

        menu_input = get_menu_input()

    print('Goodbye')

main()