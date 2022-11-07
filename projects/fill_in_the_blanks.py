#!/usr/bin/env python3

# Clara Penn
# IPND Stage 2 Final Project


easy_level_paragraph = '''Taylor ___1___ is a leading American singer-songwriter and one of the best-selling pop
artists of all time. ___1___ has sold more than 40 million ___2___. She started out with ambitions
to be a ___3___ music star, and aged 14, moved to ___4___, Tennessee, to pursue that dream. Her
eponymously named debut album "Taylor ___1___", a crossover between ___3___ and pop music, spent
157 weeks at the no.5 ranking in the Billboard 200 ___2___ chart in the United States, the longest
stay on the chart by any release in the noughties. ___1___ is the eighth-most-followed user on
Instagram, with 108 million followers.'''

easy_answers = ['Swift', 'albums', 'country', 'Nashville']

medium_level_paragraph = '''A ___1___ is created with the def keyword. You specify the inputs a ___1___ takes by
adding ___2___ separated by commas between the parentheses. ___1___s by default return ___3___ if you
don't specify the value to return. ___2___ can be standard data types such as string, number, dictionary,
tuple, and ___4___ or can be more complicated such as objects and lambda functions.'''

medium_answers = ['function', 'arguments', 'None', 'list']

hard_level_paragraph = '''Rick ___1___ became the subject of a viral Internet ___2___ in which an estimated
25 million Internet users were tricked into watching Rick ___1___'s ___3___ "Never Gonna ___4___ You Up"
by posting it under the name of other popular ___3___ titles. The practice is now known as Rickrolling.
The phenomenon became so popular that on April 1, 2008, ___5___ pranked its users by making every
single featured ___3___ on the front page a Rickroll.'''

hard_answers = ['Astley', 'meme', 'video', 'Give', 'YouTube']


def choose_level():

    '''Takes input from the user stating the level at which they want to play,
    and returns two outputs: a string containing the correct-level paragraph
    with missing words, and a list containing the matching answers.'''

    level_choice = input("\n\nChoose a level: easy, medium or hard: ").lower().strip()

    if level_choice == "easy":
        print("\n\nYou chose easy level!\n\n")
        return (easy_level_paragraph, easy_answers)

    elif level_choice == "medium":
        print("\n\nYou chose medium level!\n\n")
        return (medium_level_paragraph, medium_answers)

    elif level_choice == "hard":
        print("\n\nYou chose the hardest level!\n\n")
        return (hard_level_paragraph, hard_answers)

    else:
        print("\n\nThat is not a valid level\n\n")
        return choose_level()  # I am using recursion to give the user another chance to set the level.

def choose_lives():
    '''Takes input from the user as to how many lives they want.'''

    try:
        lives = int(input("\n\nHow many lives would you like? "))
    except ValueError:
        print("That's not a valid number of lives!")
        return choose_lives()

    if lives < 1:
        print("You can't have less than one life!")
        return choose_lives()

    return lives



def correct_answer_response(current_paragraph, blank_to_replace, correct_answer, score):

    '''Four parameters are passed in here. It gets the current paragraph and replaces
    the missing numbered strings with the correct answer from the answers list. It then
    increments the score by one.
    This has so many parameters because I aimed to reduce the number of lines
    of code in my main run_game function. By separating out this function I was able
    to take out the final couple of lines of code to bring it in line with the project rubric.'''

    print("\n\nCorrect!\n")
    current_paragraph = current_paragraph.replace(blank_to_replace, correct_answer)
    score += 1

    return (current_paragraph, score)


def finish_game(lives):

    '''Takes the variable lives as input, and if the number
    of lives is equal to zero, it calls the function lose_game,
    but if the player has lives remaining, it calls the function win_game.'''

    if lives == 0:
        lose_game()
    else:
        win_game()

def win_game():

    '''Takes input from the user on winning the game and calls the function run_game
    if they want to play again, or wraps it up if not.'''

    print("You won!\n\n")
    winner_choice = input("\n\nWant to play again? Enter Y or N ").lower().strip()
    if winner_choice == "y":
        print("\nGreat! Let's play again!\n\n")
        run_game()
    else:
        print("\n\nOK! \n\nBye!\n\n")


def lose_game():

    '''Takes input from the user on losing the game and calls the function run_game
    again if they want to play again, or wraps it up if not.'''

    loser_choice = input("\n\nYou have zero lives left! \n\nWant to play again? Enter Y or N ").lower().strip()
    if loser_choice == "y":
        run_game()
    else:
        print("\n\nOK! \n\nBye!\n\n")


def run_game():
    '''The main function that runs the game, by calling the functions defined above.'''

    score = 0

    # set current_paragraph to be the value of selected paragraph
    # and answers to be the value of the selected answers
    current_paragraph, answers = choose_level()

    lives = choose_lives()

    while score < len(answers) and lives > 0:

        blank_number = score + 1
        blank_to_replace = "___" + str(blank_number) + "___"

        print("\nLives left: " + str(lives))
        print("\nThe current_paragraph reads:\n\n" + current_paragraph)

        guess = input("\n\nWhat should be substituted in for " + blank_to_replace + "? ").strip()
        correct_answer = answers[score]
        if guess == correct_answer:
            current_paragraph, score = correct_answer_response(current_paragraph, blank_to_replace, correct_answer, score)

        else:
            lives = lives - 1
            print("\n\nThat's the wrong answer.\n")
            if lives > 0:
                print("Try again!")

    # loop has finished now

    finish_game(lives)

if __name__ == "__main__":
    # run the main function to start the game
    run_game()
