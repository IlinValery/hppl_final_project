import matplotlib.pyplot as plt
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-be', '--basic-encryptor-times', type=str, help='Path to the encryptor times file',
                        default='basic_encryptor_times.txt')
    parser.add_argument('-bd', '--basic-decryptor-times', type=str, help='Path to the decoder times file',
                        default='basic_decryptor_times.txt')

    parser.add_argument('-ae', '--advanced-encryptor-times', type=str, help='Path to the encryptor times file',
                        default='advanced_encryptor_times.txt')
    parser.add_argument('-ad', '--advanced-decryptor-times', type=str, help='Path to the decoder times file',
                        default='advanced_decryptor_times.txt')

    args = parser.parse_args()

    basic_encryptor_times = []
    basic_decryptor_times = []
    advanced_encryptor_times = []
    advanced_decryptor_times = []
    text_sizes = []
    missed_lines = []
    with open(args.advanced_encryptor_times, "r") as f:
        i = -1
        for line in f:
            i += 1
            data = line.split(" - ")
            if data[0][:5] == "text_":
                text_sizes.append(int(data[0][5:].split('.')[0]))
                advanced_encryptor_times.append(float(data[1]))
            else:
                missed_lines.append(i)

    with open(args.advanced_decryptor_times, "r") as f:
        i = -1
        for line in f:
            i += 1
            if i in missed_lines:
                continue
            data = line.split(" - ")
            advanced_decryptor_times.append(float(data[1]))

    with open(args.basic_decryptor_times, "r") as f:
        i = -1
        for line in f:
            i += 1
            if i in missed_lines:
                continue
            data = line.split(" - ")
            basic_decryptor_times.append(float(data[1]))

    with open(args.basic_encryptor_times, "r") as f:
        i = -1
        for line in f:
            i += 1
            if i in missed_lines:
                continue
            data = line.split(" - ")
            basic_encryptor_times.append(float(data[1]))

    sorted_data = sorted(zip(text_sizes, advanced_encryptor_times, advanced_decryptor_times, basic_encryptor_times,
                             basic_decryptor_times), key=lambda x: x[0])
    text_sizes, advanced_encryptor_times, advanced_decryptor_times, basic_encryptor_times, basic_decryptor_times = zip(
        *sorted_data)
    fig, ax = plt.subplots()
    ax.plot(text_sizes, advanced_encryptor_times, label="Advanced encryptor")
    ax.plot(text_sizes, advanced_decryptor_times, label="Advanced decryptor")
    ax.plot(text_sizes, basic_encryptor_times, label="Basic encryptor")
    ax.plot(text_sizes, basic_decryptor_times, label="Basic decryptor")
    ax.legend()
    ax.set_xlabel("Text size, number of letters")
    ax.set_ylabel("Time, secs")
    ax.set_title("Comparison of advanced and basic processing")
    plt.grid(zorder=0)
    fig.tight_layout()
    plt.savefig("Productivity comparison.png", bbox_inches='tight')
