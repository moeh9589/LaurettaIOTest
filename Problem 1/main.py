# TO TEST A DIFFERENT IMAGE, CHANGE THE VALUE IN LINE 65 TO THE NAME OF THE DESIRED FOLDER

import os
import cv2
import numpy
from PIL import Image 
import math


def get_images(dir_string):
    
    count = 0
    img_list = []

    for path in os.listdir(dir_string):
        if os.path.isfile(os.path.join(dir_string, path)):
            count += 1
            img_list.append( dir_string + "/" + path)

    return img_list


def find_circles(dir):
    images = []
    img_list = get_images(dir)

    blue = [(0,0,200),(20,20,255)] 
    red = [(200,0,0),(255,20,20)] 

    dot_colors = [red, blue]

    for im in img_list:
        red_count = 0
        blue_count = 0
        img = cv2.imread(im)   
        blur = cv2.medianBlur(img, 7)

        for lower, upper in dot_colors:
            output = img.copy()
            mask = cv2.inRange(blur,lower,upper) 
            contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]

            for c in contours:
                if lower == blue[0]:
                    blue_count += 1

                if lower == red[0]:
                    red_count += 1

                perimeter = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

                if len(approx) > 5:
                    cv2.drawContours(output, [c], -1, (36, 255, 12), -1)

        img_data = {"Image Name" : im, "Red Count" : red_count-1, "Blue Count" : blue_count-1}
        images.append(img_data)

    return images

def main():
    image_directory = "Problem 1/"
    # HERE IS WHERE TO ACCESS THE DIFFERENT TESTS... USE THE NAME OF THE FOLDER ASSOCIATED WITH EACH TEST
    desired_directory = "xray"
    image_directory += desired_directory

    images = find_circles(image_directory)
    img_width = int(math.sqrt(len(images)))
    reconstructed_image = [ [ None for i in range(img_width) ] for j in range(img_width) ]

    for i in range (len(images)):
        col = images[i].get('Red Count')
        row = images[i].get('Blue Count')
        reconstructed_image[row][col] = images[i].get("Image Name")
    
    ref_img = Image.open(reconstructed_image[0][0])
    size = ref_img.size
    final_image = Image.new('RGB', (img_width*size[0], img_width*size[1]), (250,250,250))
    
    for i in range(img_width):
        for j in range(img_width):
            current_image = Image.open(reconstructed_image[i][j])
            final_image.paste(current_image, (current_image.size[0]*i, current_image.size[1]*j))

    final_image.save("merged_image.jpg", "JPEG")   
    final_image.show()     
    

main()