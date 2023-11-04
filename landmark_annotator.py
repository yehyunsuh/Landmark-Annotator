import os
import cv2
import argparse
from datetime import datetime

clicked_points = []
clone = None


def MouseLeftClick(event, x, y, flags, param):
    red = (0, 0, 255)
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((y, x))
        image = clone.copy()
        for point in clicked_points:
            cv2.circle(
                image, (point[1], point[0]), 5, red, thickness=-1)
        cv2.imshow("image", image)


def annotator(args):
    """
    This function saves txt files based on the annotations done in each image

    """
    global clone, clicked_points
    image_names = sorted(os.listdir(args.path))
    now = datetime.now()
    now_date = (
        now.year - 2000, now.month, now.day, now.hour, now.minute, now.second
    )
    now_str = "%s%02d%02d_%02d%02d%02d" % now_date
    txt_name = f'{args.name}/{now_str}_{args.path.split("/")[-1]}.txt'

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", MouseLeftClick)

    count = 0
    while True:
        try:
            image_name = image_names[count]
            blue = (0, 0, 255)
            image_path = f'{args.path}/{image_name}'
            image = cv2.imread(image_path)
            clone = image.copy()
            same = False

            print(image_name)
            while True:
                cv2.imshow("image", image)
                key = cv2.waitKey(0)

                if key == ord('n'):
                    count += 1
                    if clicked_points == []:
                        break

                    # TODO: erase if existed
                    if os.path.exists(txt_name):
                        file_read = open(txt_name, 'r')
                        lines = file_read.readlines()
                        for line in lines:
                            if image_name == line.split(',')[0]:
                                same = True
                                old = line
                        file_read.close()

                    text_output = image_name
                    text_output += "," + str(len(clicked_points))
                    for points in clicked_points:
                        text_output += f',{str(points[0])},{str(points[1])}'
                    text_output += '\n'

                    if same:
                        file_write = open(txt_name, 'w')
                        print(f'{old} has been changed to \n{text_output}')
                        for line in lines:
                            file_write.write(line.replace(old, text_output))
                        file_write.close()
                    else:
                        file_write = open(txt_name, 'a+')
                        file_write.write(text_output)
                        file_write.close()
                    clicked_points = []
                    break

                if key == ord('b'):
                    if len(clicked_points) > 0:
                        clicked_points.pop()
                        image = clone.copy()
                        for i in range(len(clicked_points)):
                            point = (
                                clicked_points[i][1], clicked_points[i][0])
                            cv2.circle(image, point, 5, blue, -1)
                        cv2.imshow("image", image)

                if key == ord('p'):
                    count -= 1
                    clicked_points = []
                    break

                if key == ord('q'):
                    cv2.destroyAllWindows()
                    exit()

        except Exception as e:
            print(e)
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default='png', help="Image directory path")
    parser.add_argument("--name", default='Yehyun')
    args = parser.parse_args()

    # create directory where txt file will be saved
    os.makedirs(args.name, exist_ok=True)

    annotator(args)
