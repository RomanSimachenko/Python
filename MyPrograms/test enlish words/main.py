import random


def main(command):
    if command.lower() == 'end':
        print('Bye!')
        return

    if command.lower() == 'add':
        print()
        print("Say 'stop' to finish adding.")
        word_means = input("What word do you want to add?(word-mean1;mean2...)(stop to finish):")
        while word_means.lower() != 'stop':
            print()
            with open(r"dictionary of words.txt", 'a') as file:
                tmp1, tmp2 = word_means.strip().split('-')
                word, means = tmp1.strip(), tmp2.strip()
                if means[-1] == ";":
                    means = means[:-1]
                file.write(f"{word}: {means}\n")
            word_means = input("What word do you want to add?(word-mean1;mean2...)(stop to finish):")

    if command.lower() == 'test':
        words = []
        means = []
        with open(r"dictionary of words.txt") as file:
            string = file.readline()
            while string != '':
                word_means = string.strip().split('\n')
                for el in word_means:
                    word, mean = el.strip().split(':')
                    words.append(word)
                    means.append(mean.strip())
                string = file.readline()
        max_marks = len(words)
        marks = 0
        for i in range(len(words)):
            print()
            choice = random.randrange(0, len(words))
            choice_word = words[choice]
            choice_means = means[choice]
            del words[choice], means[choice]
            input_mean = input(f"Your word - {choice_word}. Write your mean or stop: ")
            if input_mean.lower() == 'stop':
                break
            if input_mean.lower() in ' ':
                print("Fail...")
                continue
            if input_mean.lower() in choice_means:
                marks += 1
                print("Yes! You are right!")
            else:
                print("Fail...")
        print(f'This is all. Your result: {marks}/{max_marks}')
    print()
    command = input("What do you want to do?(add, test, end): ")
    main(command)


if __name__ == '__main__':
    print()
    command = input("What do you want to do?(add, test, end): ")
    main(command)