"""
This code visualizes the annotations saved in txt files on the images in /png directory
"""

import argparse
import cv2
import os

from tqdm import tqdm


def visualize_annotation(args):
    annotated_image_directory = f'image_annotated/{args.text_file_name.split(".")[0]}'
    os.makedirs(annotated_image_directory, exist_ok=True)

    text_file_path = f'{args.text_directory}/{args.text_file_name}'
    with open(text_file_path, "r") as file_read:
        lines = file_read.readlines()
        for line in tqdm(lines):
            line_split = line.split(",")
            image_name = line_split[0]
            points = line_split[2:]

            image = cv2.imread(f"{args.image_directory}/{image_name}")
            for i in range(0, len(points), 2):
                y = int(points[i])
                x = int(points[i+1])
                cv2.circle(image, (x, y), 15, (0, 255, 0), -1)

            cv2.imwrite(f"{annotated_image_directory}/{image_name}", image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--image_directory", default="image", help="Image directory path")
    parser.add_argument("--text_directory", default="text", help="Image directory path")
    parser.add_argument("--text_file_name", default="", help="Image directory path")

    args = parser.parse_args()

    visualize_annotation(args)