#!/usr/bin/python

import sys
import argparse
from PIL import Image
import numpy
import datetime


def find_coeffs(pa, pb):
    # Code copied from mmgp's answer at https://stackoverflow.com/a/14178717/5564605
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.array(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.linalg.solve(A,B)

    return numpy.array(res).reshape(8)

def resizeImg(img,box):
    width, height = img.size
    new_box = box.copy()

    crop_width = box[2] - box[0]
    crop_height = box[3] - box[1]

    if (width / crop_width) > (height / crop_height):
        l,r = computeCrop(0, box[0], box[2], img.width, (crop_width*height)/crop_height)

        if l != 0:
            new_box[0] -= l
            new_box[2] -= l

        img2 = img.crop((l, 0, r, height))
    else:
        t,b = computeCrop(0, box[1], box[3], img.height, (crop_height*width)/crop_width )

        if t != 0:
            new_box[1] -= t
            new_box[3] -= t

        img2 = img.crop((0, t, width, b))

    return (img2,new_box)

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the filename of the image to be processed.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o", "--orthogonal", action="store_true", default=True,
        help="flag used to run the script on an orthogonally rectangular box. Defaults to orthogonal mode.")
    group.add_argument("-s", "--skew", action="store_true",
        help="flag used to run the script on a non orthogonally rectangular box.")

    parser.add_argument("dimensions", 
        help='''the pixel dimensions of the box to create the effect. \n
         With -n, the dimensions have to be given as "x1,y1,x2,y2" \n
         With the -s flag, dimensions have to be given as "(x1,y1),(x2,y2),(x3,y3),(x4,y4)"''')
    parser.add_argument("-n", "--count", type=int, help="number of times to recurse. Defaults to 10.", default=10)

    args = parser.parse_args()

    try:
        img = Image.open(args.filename)
    except FileNotFoundError:
        print("File not found. Error.")
        return -1

    img = img.convert("RGBA")
    width,height = img.size

    if args.skew:
        dim_list = args.dimensions.split(',')
        box = list(map(eval, map(','.join, zip(dim_list[::2], dim_list[1::2]))))

        for i in range(args.count):
            try:
                coeffs = find_coeffs(box,
                    [(0, 0), (width, 0), (width, height), (0, height)])
            except:
                break

            img2 = img.transform(img.size, Image.PERSPECTIVE, coeffs)
            img.paste(img2, (0,0), img2)

    else: # args.orthogonal case.
        box = list(map(int, args.dimensions.split(',')))
        crop_img,crop_box = resizeImg(img, box)
        crop_size = (box[2]-box[0], box[3]-box[1])

        for i in range(args.count - 1):
            img2 = crop_img.resize(crop_size)
            crop_img.paste(img2, (crop_box[0], crop_box[1]))

        img2 = crop_img.resize(crop_size)
        img.paste(img2, (box[0], box[1]))

    img.save("output-" + str(datetime.datetime.now()) + ".png")

if __name__ == "__main__":
    main()
