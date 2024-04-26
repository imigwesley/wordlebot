import argparse

def main():
    # define word bank tuple
    with open('valid-guesses.txt', 'r') as bank_file:
        words_tuple = tuple(line.strip() for line in bank_file)  

    parser = argparse.ArgumentParser(description='to parse arguments, naturally')
    parser.add_argument('--interactive', action='store_true', help='If you want this to be an assistant')
    parser.add_argument('--testing', action='store_true', help='Test different algorithms/strategies')
    parser.add_argument('--model', type=str, help='Which algo/system will be used.')
    # model_dict = {0:'valid frequencies individual letters valid guesses', 1:''}
    args = parser.parse_args()

    if args.model == 0:
        letter_frequency(words_tuple)
    elif args.model == 1:
        print('sumn I havent written yet')

def letter_frequency(remaining_words):
    # define letter frequency dictionary
    with open('letter-frequencies-valid-guesses.txt', 'r') as freq_file:
        frequency_dict = {}
        next(freq_file)
        for line in freq_file:
            letter, freq = line.strip().split(',')
            frequency_dict[letter] = float(freq)

    # while (len(word) != 5 or not word.isalpha()):
    #     word = input('What you provided was either not five letters long or contained something other than letters. Please provide a valid word:\n')
    
    # play loop. i is number of guesses left.
    response = '     '
    word_played = ''
    for i in range(1, 7, 1):
        remaining_words = clean_up_remaining(remaining_words, word_played, response)
        print(f'len remaining words is {len(remaining_words)}')
        recommended_word_s = calculate_lf_word(remaining_words, frequency_dict, response)
        print('##############################################################################')
        if len(recommended_word_s) > 1:
            formatted_words = ''
            for index, info in enumerate(recommended_word_s.items()):
                if index != len(recommended_word_s) - 1:
                    formatted_words += f'"{info[0]}" (scored {info[1]:.2f}), '
                else:
                    formatted_words += f'and "{info[0]}" (scored {info[1]:.2f})'
            print(f"Try number {i}. There are {len(remaining_words)} possible words still in play. Multiple words are equally as likely to work. They are: {formatted_words}.\n") # something about percent accuracy maybe
                
        else:
            print(f"Try number {i}. There are {len(remaining_words)} possible words still in play. The best word you should try is: {next(iter(recommended_word_s.keys()))}. It scored a {next(iter(recommended_word_s.values())):.2f} score.\n") # something about percent accuracy maybe
        word_played, response = prompt_for_performance()
        if 'y' and 'b' not in response:
            print(f'Good job completing the wordle in {i} tries.')
            break
        else:
            print(f'Darn. On to the next try.\n')
        

def calculate_lf_word(remaining_words, frequency_dict, letters_to_check):
    # determine which word is statistically best.
    possible_guesses_no_repeats = {}
    highest_score = 0.0
    for word in remaining_words:
        word_score = 0.0
        letters_used = []
        for i in range(0, 5, 1):
            if letters_to_check[i] == 'g':
                # Exclude already correct letters from probability score.
                continue
            if word[i] not in letters_used:
                # ensures letters are not repeated. Favors letter diversity.
                word_score += frequency_dict[word[i]]
                letters_used.append(word[i])
        if word_score > highest_score:
            possible_guesses_no_repeats = {word: word_score}
            highest_score = word_score
        elif word_score == highest_score:
            possible_guesses_no_repeats[word] = word_score
    # print(f'DEBUG: possible_guesses_nr is {possible_guesses_no_repeats}')
    return possible_guesses_no_repeats
            



def prompt_for_performance():
    word_played = input("What word did you play?\n")
    while (len(word_played) != 5 or not word_played.isalpha()):
        word_played = input('What you provided was either not five letters long or contained something other than letters. Please provide a valid word:\n')
    response = input("What was the response? (please input your green, black, and yellow response as g's, b's, and y's. Example is gbyyb.\n")
    while (len(response) != 5 or not response.isalpha()):
        response = input('What you provided was either not five letters long or contained something other than letters. Please provide a valid sequence:\n')
    return word_played, response

def clean_up_remaining(original_words, played_word, play_response):
    # print(f'DEBUG: inside clean up remaining. original words is len {len(original_words)}, played word is {played_word}, response was {play_response}')
    still_possible = []
    black_letters = []
    green_letters = []
    yellow_letters = []

    for i in range(0, 5, 1):
        if play_response[i] == 'b':
            black_letters.append(played_word[i])
        elif play_response[i] == 'y':
            yellow_letters.append({i: played_word[i]})
        elif play_response[i] == 'g':
            green_letters.append({i: played_word[i]})

    # print(f'DEBUG: Black letters are {black_letters}, green letters are {green_letters}, yellow letters are {yellow_letters}')
        
    
    for word in original_words:
        if word == 'vapid': print('found vapid')
        continue_outer = False
        # if letter['b'] in word: do not proceed
        for black_letter in black_letters:
            if black_letter in word:
                if word == 'vapid': print('made it black')
                continue_outer = True
                break
        if continue_outer:
            continue
        # if letter['y'] not in word or yellow letter in same place as previous guess: do not proceed 
        for yellow_dict in yellow_letters:
            (yellow_index, yellow_letter), = yellow_dict.items()
            if yellow_letter not in word or word[yellow_index] == yellow_letter:
                if word == 'vapid': print('made it yellow')
                continue_outer = True
                break
        if continue_outer:
            continue
        # if greens do not match: do not proceed
        for green_dict in green_letters:
            (green_index, green_letter), = green_dict.items()
            if word[green_index] != green_letter:
                if word == 'vapid': print('made it green')
                continue_outer = True
                break
        if continue_outer:
            continue

        still_possible.append(word)
    return still_possible



if __name__ == "__main__":
    main()

'''
Future Development ideas
- automatic tester
- command line arguments to determine what you want to run (interactive, solo)
- word frequencies in actual language
- starting letter frequency
- 


- tough bc they come up with the word day-of, so there is no bank of actual solution words, not just allowed guesses
'''

