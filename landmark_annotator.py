import os
import re
import cv2
import argparse
from datetime import datetime
from glob import glob

clicked_points = []
clone = None
colors = ()


def MouseLeftClick(event, x, y, _, __):
    """
    Activated at every left click and draws the added annotation on the image
    :param event: cv2 event
    :param x: x coordinate of the left click
    :param y: y coordinate of the left click
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((y, x))
        image = clone.copy()
        for point in clicked_points:
            cv2.circle(image, (point[1], point[0]), 5, colors[2], thickness=-1)
        cv2.imshow("image", image)


def annotator(args):
    """
    This function saves txt files based on the annotations done in each image
    :param args: arguments from argparser
    """
    global clone, clicked_points, colors
    image_path_list = sorted(glob(f'{args.path}/*.png'))
    now = datetime.now()
    now_date = (now.year - 2000, now.month, now.day, now.hour, now.minute, now.second)
    now_str = "%s%02d%02d_%02d%02d%02d" % now_date
    txt_name = f'{args.name}/{now_str}_{args.path.split("/")[-1]}.txt'
    colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255))  # BGR

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", MouseLeftClick)
    count = 0
    while count != len(image_path_list):
        annotated = False
        image_path = image_path_list[count]
        image_name = image_path.split('/')[-1]
        original_image = cv2.imread(image_path)
        clone = original_image.copy()
        same_image = False

        if os.path.exists('checkpoint.txt'):
            file_read = open("checkpoint.txt", "r")
            lines = file_read.readlines()
            for line in lines:
                if image_name == line.strip():
                    annotated = True
                    count += 1
                    break
                file_read.close()

        if not annotated:
            print(image_name)
            while True:
                image = cv2.imread(image_path)
                for point in clicked_points:
                    cv2.circle(image, (point[1], point[0]), 5, colors[2], thickness=-1)
                cv2.imshow("image", image)
                key = cv2.waitKey(0)

                # when you press b - erase the most recent anntation
                if key == ord("b"):
                    if len(clicked_points) > 0:
                        clicked_points.pop()

                # when you press n - moves to the next image after saving the annotation
                if key == ord("n"):
                    file_write_txt = image_name + "\n"
                    file_write = open("checkpoint.txt", "a+")
                    file_write.write(file_write_txt)
                    file_write.close()
                    count += 1
                    # if there has been clicks
                    if clicked_points != []:
                        # check if there was a same image that has been annotated before
                        # needs this to re-annotate previous images
                        if os.path.exists(txt_name):
                            file_read = open(txt_name, "r")
                            lines = file_read.readlines()
                            for line in lines:
                                if image_name == line.split(",")[0]:
                                    same_image = True
                                    previous_annotation = line
                            file_read.close()

                        # change the format of changed points
                        text_output = image_name
                        text_output += "," + str(len(clicked_points))
                        for points in clicked_points:
                            text_output += f",{str(points[0])},{str(points[1])}"
                        text_output += "\n"

                        # when there was a same image that has been annotated - replace previous
                        if same_image:
                            file_write = open(txt_name, "w")
                            print(f"{previous_annotation} has been changed to \n{text_output}")
                            for line in lines:
                                file_write.write(line.replace(previous_annotation, text_output))
                            file_write.close()

                        # when it is first time being annotated - add to the current txt file
                        else:
                            file_write = open(txt_name, "a+")
                            file_write.write(text_output)
                            file_write.close()
                    clicked_points = []
                    break

                if key == ord("p"):
                    count -= 1
                    clicked_points = []
                    break
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    exit()
        else:
            print(f'{image_name} has been already annotated')

    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="png", help="Image directory path")
    parser.add_argument("--name", default="Yehyun")
    args = parser.parse_args()

    # create directory where txt file will be saved
    os.makedirs(args.name, exist_ok=True)

    annotator(args)
