# infinite-recursive-image
A script to create the [Droste effect](https://en.wikipedia.org/wiki/Droste_effect) with any image. Supports both rectangular and skewed boxes.

## Usage

Run:

```
$ git clone github.com/EkanshdeepGupta/infinite-recursive-image
$ cd ./infinite-recursive-image
$ python ./nested_photo.py -h
    usage: nested_photo.py [-h] [-o | -s] [-n COUNT] filename dimensions

    positional arguments:
      filename              the filename of the image to be processed.
      dimensions            the pixel dimensions of the box to create the effect. With -n, the
                            dimensions have to be given as "x1,y1,x2,y2" With the -s flag, dimensions
                            have to be given as "(x1,y1),(x2,y2),(x3,y3),(x4,y4)"

    optional arguments:
      -h, --help            show this help message and exit
      -o, --orthogonal      flag used to run the script on an orthogonally rectangular box. Defaults
                            to orthogonal mode.
      -s, --skew            flag used to run the script on a non orthogonally rectangular box.
      -n COUNT, --count COUNT
                            number of times to recurse. Defaults to 10.
```

For orthogonal mode, the dimensions can be given as a comma separated string of four numbers, which denote the pixel coordinates of the left, top, right, bottom edge respectively, of the box on which to generate the Droste effect. Since orthogonal mode only works on orthogonal rectangles, only the edges can be specified. For non-rectangular boxes, use skew mode with the `-s` flag.

For skew mode, the dimensions can be given as a string of four 2-tuples of numbers, which denote the pixel coordinates of the left, top, right, bottom corner respectively, of the box on which to generate the Droste effect.

## Examples

Get the outputs stored in `./examples` as follows:

<img src="examples/test.webp" alt="test.webp" style="zoom:33%;" />

```bash
$ python ./nested_photo.py ./examples/test.webp "552,238,1049,540"
```

<img src="examples/test-output.png" alt="test-output" style="zoom: 33%;" />

<img src="examples/living-room-tv.jpg" alt="living-room-tv" style="zoom:80%;" />

```bash
$ python ./nested_photo.py ./examples/living-room-tv.jpg "162,185,337,280"
```
<img src="examples/living-room-tv-output.png" alt="living-room-tv" style="zoom:80%;" />

<img src="examples/image.webp" style="zoom: 33%;" />

```bash
$ python ./nested_photo.py ./examples/image.webp -s "(456,155), (863,237), (857,468), (457,451)"
```
<img src="examples/image-output.png" style="zoom:33%;" />

<img src="examples/seats.jpg" style="zoom: 25%;" />

```bash
$ python nested_photo.py "./examples/seats.jpg" -s "(1233,284),(2346,270),(2360, 1007),(1249, 1024)"
```
<img src="examples/seats-output.png" style="zoom:25%;" />



### To-do

- [x] Create a skew version to handle non-square boxes.
