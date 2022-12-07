import argparse
import bz2
import os


def split(
    file_path, output_dir, num_of_files, games_per_file):
    
    try:
        os.makedirs(output_dir, exist_ok=False)
    except FileExistsError:
        print("Output dir already exists. Remove it!")
        
    counter = 0
    with bz2.BZ2File(file_path, 'r') as input:
        half = False
        one_png = []
        results = []
        for line in input:
            line = line.decode()
            if line == "\n":
                if not half:
                    half = True
                else:
                    half = False

                    with open(
                        f'{output_dir}/{counter//games_per_file}.txt',
                        'a'
                    ) as output_file:
                        output_file.write(''.join(one_png)+'\n')
                    one_png = []
                    counter += 1
                    if counter >= num_of_files * games_per_file:
                        return
            else:
                one_png.append(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='path to input file')
    parser.add_argument('--output', help='path to output dir', default='output')
    parser.add_argument('--num_of_files', help='number of files to produce', type=int, default=1)
    parser.add_argument('--games', help='number of games per file', type=int, default=10)
    args = parser.parse_args()

    split(args.input, args.output, args.num_of_files, args.games)

if __name__ == '__main__':
    main()
