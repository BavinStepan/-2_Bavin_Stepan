import random

MAX_MISTAKES = 6
GALLOWS_PREFIX = "gallows"
WORDS_FILE = "words.txt"

def get_empty_list():
    return []

def is_list_non_empty(lst):
    return bool(lst)

def has_words_left(all_words, played_words):
    return len(played_words) < len(all_words)

def load_words_from_file(filename=None):
    if filename is None:
        filename = WORDS_FILE

    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                word, description = line.split(':', 1)
                words.append((word.strip().lower(), description.strip()))
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
    except Exception as error:
        print(f"Ошибка при чтении файла '{filename}': {error}")

    return words

def load_gallows_stages(prefix=None, stages_count=None):
    if prefix is None:
        prefix = GALLOWS_PREFIX
    if stages_count is None:
        stages_count = MAX_MISTAKES + 1

    stages = []
    for stage_number in range(stages_count):
        filename = f"{prefix}_{stage_number}.txt"
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                stages.append(file.read())
        except FileNotFoundError:
            print(f"Ошибка: файл виселицы '{filename}' не найден.")
            return []
        except Exception as error:
            print(f"Ошибка при чтении '{filename}': {error}")
            return []

    return stages

def save_unique_words_to_file(filename, played_words):
    try:
        unique_words = sorted(set(played_words))
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Всего уникальных слов: {len(unique_words)}\n")
            file.write("=" * 25 + "\n")
            for word in unique_words:
                file.write(word + "\n")
    except Exception as error:
        print(f"Ошибка при сохранении файла '{filename}': {error}")

# ==================== Выбор слова ====================
def select_random_word(words, played_words):
    remaining_words = [
        item for item in words
        if item[0] not in played_words
    ]
    if not remaining_words:
        return None, None
    return random.choice(remaining_words)

def display_gallows(stage, gallows_stages):
    if 0 <= stage < len(gallows_stages):
        print(gallows_stages[stage])
    else:
        print("[Ошибка: этап виселицы не найден]")

def display_word_progress(word, guessed_letters):
    parts = []
    for letter in word:
        if letter in guessed_letters:
            parts.append(letter)
        else:
            parts.append('■')
    return ' '.join(parts)

def display_message(message):
    print(message)

def get_user_input(prompt):
    return input(prompt)

def ask_play_again():
    answer = get_user_input("Хотите сыграть ещё? (да/нет): ").strip().lower()
    return answer in ('да', 'д', 'yes', 'y')

def is_single_letter(input_str):
    return len(input_str) == 1 and input_str.isalpha()

def is_word_guess_correct(word, guess):
    return guess.lower() == word

def is_letter_already_guessed(letter, guessed_letters):
    return letter in guessed_letters

def is_letter_in_word(letter, word):
    return letter in word

def is_word_fully_guessed(word, guessed_letters):
    return all(letter in guessed_letters for letter in word)

def process_guess(guess, word, guessed_letters, mistakes):
    if len(guess) > 1:
        if is_word_guess_correct(word, guess):
            return mistakes, 'win', f"Поздравляем! Вы отгадали слово: {word}"
        else:
            return mistakes + 1, 'wrong', "Неверно!"

    if is_single_letter(guess):
        if is_letter_already_guessed(guess, guessed_letters):
            return mistakes, 'continue', "Вы уже называли эту букву. Попробуйте другую."

        guessed_letters.add(guess)
        if is_letter_in_word(guess, word):
            return mistakes, 'continue', "Верно!"
        else:
            return mistakes + 1, 'wrong', "Неверно!"

    return mistakes, 'invalid', "Некорректный ввод. Введите одну букву или всё слово целиком."

def play_round(word, description, gallows_stages):
    mistakes = 0
    guessed_letters = set()

    display_message(f"\nПодсказка: {description}")

    while mistakes <= MAX_MISTAKES:
        display_gallows(mistakes, gallows_stages)
        progress = display_word_progress(word, guessed_letters)
        display_message(progress)

        if is_word_fully_guessed(word, guessed_letters):
            display_message(f"Поздравляем! Вы отгадали слово: {word}")
            return True

        guess = get_user_input("Введите букву или слово целиком: ").strip().lower()
        if not guess:
            display_message("Вы ничего не ввели. Попробуйте ещё раз.")
            continue

        mistakes, result, message = process_guess(guess, word, guessed_letters, mistakes)
        display_message(message)

        if result == 'win':
            return True
        if result == 'wrong' and mistakes > MAX_MISTAKES:
            break

    display_gallows(mistakes, gallows_stages)
    display_message(f"Вы проиграли! Загаданное слово: {word}")
    return False

def run_game_session(words, gallows_stages):
    played_words = get_empty_list()

    while has_words_left(words, played_words):
        word, description = select_random_word(words, played_words)
        if word is None:
            break

        play_round(word, description, gallows_stages)
        played_words.append(word)

        if not ask_play_again():
            break

    return played_words