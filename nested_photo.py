#!/usr/bin/python

import sys
from PIL import Image


def resizeImg(img):
    width, height = img.size

    crop_width = dim[2] - dim[0]
    crop_height = dim[3] - dim[1]

    if (width / crop_width) > (height / crop_height):
        l,r = computeCrop(0, dim[0], dim[2], img.width, (crop_width*height)/crop_height)

        if l != 0:
            dim[0] -= l
            dim[2] -= l

        img2 = img.crop((l, 0, r, height))
    else:
        t,b = computeCrop(0, dim[1], dim[3], img.height, (crop_height*width)/crop_width )

        if t != 0:
            dim[1] -= t
            dim[3] -= t

        img2 = img.crop((0, t, width, b))

    return img2

def computeCrop(i1, i2, i3, i4, length):
    crop_amount = i4-i1-length
    first_overhang = i2-i1
    second_overhang = i4-i3

    diff = abs(first_overhang - second_overhang)
    if diff > crop_amount:
        if first_overhang > second_overhang:
            first_overhang -= crop_amount
        else:
            second_overhang -= crop_amount

    else:
        first_overhang = second_overhang = min(first_overhang, second_overhang)
        first_overhang -= (crop_amount - diff) / 2
        second_overhang -= (crop_amount - diff) / 2

    return (round(i2-first_overhang), round(i3+second_overhang))

def sum_1_to_i(count, r, n): #returns n * (1 + r^1 + ... + r^count)
    acc = 0

    for i in range(count):
        acc += r ** i

    acc *= n

    return round(acc)

  

def main():
    if len(sys.argv) != 6:
        print("Incorrect number of arguments")
        return -1

    else:

        try:
            org_img = Image.open(sys.argv[1])
        except FileNotFoundError:
            print("File not found. Error.")
            return -1


        org_dim = list(map(int, (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])))
        global dim
        dim = org_dim.copy() # Making copy of org_dim; need org_dim untouched by resizeImg(), to place last copy on original image.


        img = resizeImg(org_img)
        crop_img = img.copy()

        org_paste_point = (dim[0], dim[1])
        org_crop_size = (dim[2] - dim[0], dim[3] - dim[1])
        ratio = org_crop_size[0] / img.width

        for i in range(100):
            crop_size = tuple(map(lambda x: round(x * (ratio ** i)), img.size ) )
            paste_point = tuple(map(lambda x: sum_1_to_i(i, ratio, x), org_paste_point))

            if crop_size[0] * crop_size[1] == 0:
                break

            img2 = crop_img.resize(crop_size)
            img.paste(img2, paste_point)    

        img2 = img.resize(org_crop_size)
        org_img.paste(img2, org_dim[:2])

        org_img.save("output.jpg")  

if __name__ == "__main__":
    main()
