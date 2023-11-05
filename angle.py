import math
import cv2
import numpy as np
import os
from PIL import Image, ImageFont, ImageDraw


def innerProduct(v1, v2):
    EPSILON = 1e-8

    # θ = inner_product(x, y) / (L2(x) * L2(y))
    inner_product = np.dot(v1, v2)
    v1_L2_norm = np.linalg.norm(v1)
    v2_L2_norm = np.linalg.norm(v2)
    theta = inner_product / (v1_L2_norm * v2_L2_norm) 
    if theta < -1:
        theta = -1 + EPSILON
    if theta > 1:
        theta = 1 - EPSILON

    # radian value
    x = math.acos(theta)

    # pi value
    return math.degrees(x)


def calculation(coordinates):
    hip_l = coordinates[0]
    hip_r = coordinates[1]
    cup_u = coordinates[2]
    cup_l = coordinates[3]
    cup_e = coordinates[4]

    vector1 = [hip_l[0]-hip_r[0], hip_l[1]-hip_r[1]]
    vector2 = [cup_u[0]-cup_l[0], cup_u[1]-cup_l[1]]
    vector3 = [cup_e[0]-cup_l[0], cup_e[1]-cup_l[1]]
    
    if vector1 == [0,0]: vector1 = [0.1, 0.1]
    if vector2 == [0,0]: vector2 = [0.1, 0.1]
    if vector3 == [0,0]: vector3 = [0.1, 0.1]

    hip2cup = innerProduct(vector1, vector2)
    cup2cup = innerProduct(vector3, vector2)
    
    if hip2cup > 90: hip2cup = 180 - hip2cup
    if cup2cup > 90: cup2cup = 180 - cup2cup

    return [hip2cup, cup2cup]


def intersection(coordinate_preds):
    y1, x1 = coordinate_preds[0][0], coordinate_preds[0][1]
    y2, x2 = coordinate_preds[1][0], coordinate_preds[1][1]
    y3, x3 = coordinate_preds[2][0], coordinate_preds[2][1]
    y4, x4 = coordinate_preds[3][0], coordinate_preds[3][1]

    if x2 == x1:
        x2 = x1 + 1e-6
    m1 = (y2-y1)/(x2-x1)

    if x4 == x3:
        x4 = x3 + 1e-6
    m2 = (y4-y3)/(x4-x3)

    inter_x = (y1-y3+m2*x3-m1*x1)/(m2-m1)
    inter_y = m1*(inter_x-x1)+y1

    return round(inter_x), round(inter_y)


def draw_line(draw, line_pixel, rgb, line_width):
    draw.line(line_pixel[0], fill=rgb[0], width=line_width)
    draw.line(line_pixel[1], fill=rgb[2], width=line_width)
    draw.line(line_pixel[2], fill=rgb[2], width=line_width)
    return draw


def draw_text(draw, text_pixel, text, rgb, font):
    draw.text(text_pixel[0], text[0], fill=rgb[3], align ="left", font=font) 
    draw.text(text_pixel[1], text[1], fill=rgb[3], align ="left", font=font) 
    return draw


def visualization(args, image, image_name, clicked_points, angles, colors):
    print("visualization")
    line_width, circle_size = 3, 5
    degree_sign = u'\N{DEGREE SIGN}'

    hip2cup = f'Predict: {angles[0]:.2f}{degree_sign}'  
    cup2cup = f'Predict: {angles[1]:.2f}{degree_sign}\n Degree: {np.degrees(np.arcsin(np.tan(np.radians(angles[1])))):.2f}{degree_sign}'
    red, green, blue, white = (255, 0, 0), (0,102,0), (0, 0, 255), (255,255,255)
    rgb = [red, green, blue, white]
    text = [hip2cup, cup2cup]
    font = ImageFont.truetype("./font/Gidole-Regular.ttf", size=15)

    x,y = intersection(clicked_points)
    clicked_points.append([y, x])

    for i in range(len(clicked_points)):
        point = clicked_points[i]
        # color hip as red
        if i < 2:
            cv2.circle(image, (point[1], point[0]), circle_size, colors[0], thickness=-1)
        # color cup as blue
        else:
            cv2.circle(image, (point[1], point[0]), circle_size, colors[2], thickness=-1)
    cv2.imshow("image", image)

    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    line1 = ((clicked_points[0][1],clicked_points[0][0]),(clicked_points[1][1],clicked_points[1][0]))
    line2 = ((clicked_points[2][1],clicked_points[2][0]),(clicked_points[5][1],clicked_points[5][0]))
    line3 = ((clicked_points[3][1],clicked_points[3][0]),(clicked_points[4][1],clicked_points[4][0]))
    line_pixel = [line1, line2, line3]

    if clicked_points[2][1] < 512 // 2:
        text_pixel = [
            (((7*clicked_points[0][1]+3*clicked_points[1][1])/10), (clicked_points[0][0]+clicked_points[1][0])/2 - 50),
            ((clicked_points[3][1]+30), (clicked_points[2][0]+clicked_points[3][0])/2 - 20),
        ]
    else:
        text_pixel = [
            (((7*clicked_points[0][1]+3*clicked_points[1][1])/10), (clicked_points[0][0]+clicked_points[1][0])/2 - 50),
            ((clicked_points[3][1]-105), (clicked_points[2][0]+clicked_points[3][0])/2 - 30),
        ]

    draw = draw_line(draw, line_pixel, rgb, line_width)
    draw = draw_text(draw, text_pixel, text, rgb, font)

    os.makedirs(f'{args.name}_cup_position', exist_ok=True)
    image.save(f'./{args.name}_cup_position/{image_name}.png')
    
    return np.array(image)