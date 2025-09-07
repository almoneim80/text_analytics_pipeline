import text_analyzer as ta
import pathlib

# read file
ext = ['.txt']


def read_files(file_path):
    for file in file_path:
        if pathlib.Path(file) is False:
            continue

        if pathlib.Path(file).is_dir():
            continue

        if pathlib.Path(file).suffix not in ext:
            continue
    else:
        data = []
        for file in file_path:
            with open(file, 'r', encoding="utf-8") as f:
                data.append(f.read())
    return data


print(f"please input all files you want to analyse, (just extension allowed is {ext})")
print("If you done enter (C) character")


paths = []
inp = ''
for i in range(10):
    inp = input("Please, input file path: ")
    if inp == 'C' or inp == 'c':
        break
    else:
        if pathlib.Path(inp).is_dir():
            print("path not valid")
        elif pathlib.Path(inp).suffix not in ext:
            print("path not valid")
        else:
            paths.append(inp)

if len(paths) == 0:
    print("Please input any file you want to analyse")

text = read_files(paths)
for i in range(len(text)):
    ta.outputs(text[i], i, True, True, 8, 5, 1)
    ta.out_to_file()
    ta.top_popular_words_to_csv()
