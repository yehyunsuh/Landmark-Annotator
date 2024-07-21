""" 
This code orgainzes the txt files to 1 txt file assuming that there  are multiple txt files in the same directory
"""

import argparse

from glob import glob
from tqdm import tqdm


def get_unique_directory(txt_files):
    unique_directory_list = []
    for txt_file in txt_files:
        txt_file_split = txt_file.split("/")
        txt_file_file_name = txt_file_split[-1]

        txt_file_file_name_split = txt_file_file_name.split(".")[0].split("_")
        txt_file_time = f'{txt_file_file_name_split[0]}_{txt_file_file_name_split[1]}'
        
        txt_file_png_directory = ""
        for i in range(2, len(txt_file_file_name_split)):
            if i == len(txt_file_file_name_split) - 1:
                txt_file_png_directory += f'{txt_file_file_name_split[i]}'
            else:
                txt_file_png_directory += f'{txt_file_file_name_split[i]}_'
        
        if txt_file_png_directory not in unique_directory_list:
            unique_directory_list.append(txt_file_png_directory)

    return unique_directory_list


def organize_txt(args):
    txt_files = glob(f"{args.text_directory}/*.txt")

    unique_directory_list = get_unique_directory(txt_files)
    for unique_directory in tqdm(unique_directory_list):
        txt_files = sorted(glob(f"{args.text_directory}/*{unique_directory}*.txt"))
        
        annotation_list = []
        for txt_file in txt_files:
            with open(txt_file, "r") as file_read:
                lines = file_read.readlines()
                for line in lines:
                    annotation_list.append(line)

        for annotation in annotation_list:
            ## Check if there is a duplicate and keep the last one
            for i in range(len(annotation_list)-1, 1, -1):
                for j in range(i-1, 0, -1):
                    if annotation_list[i].strip().split(".png")[0] == annotation_list[j].strip().split(".png")[0]:
                        annotation_list[j] = ""
        
        with open(f"{args.text_directory}/{unique_directory}.txt", "w") as file_write:
            for annotation in annotation_list:
                file_write.write(annotation)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--text_directory", default="text", help="Image directory path")

    args = parser.parse_args()
    
    organize_txt(args)