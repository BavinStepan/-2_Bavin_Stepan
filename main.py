import hangman_module as hm

def main():
    words = hm.load_words_from_file()
    if not hm.is_list_non_empty(words):
        hm.display_message("Не удалось загрузить слова. Игра завершена.")
        return

    gallows = hm.load_gallows_stages()
    if not hm.is_list_non_empty(gallows):
        hm.display_message("Не удалось загрузить этапы виселицы. Игра завершена.")
        return

    played_words = hm.run_game_session(words, gallows)

    hm.save_unique_words_to_file("count.txt", played_words)

if __name__ == "__main__":
    main()