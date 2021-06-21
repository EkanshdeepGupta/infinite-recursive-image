# infinite-recursive-image
A script to create the [Droste effect](https://en.wikipedia.org/wiki/Droste_effect) with any image.

## Usage

Run:

```
git clone github.com/EkanshdeepGupta/infinite-recursive-image
cd ./infinite-recursive-image
python ./nested_photo.py "original_photo.jpg" x1 y1 x2 y2
```

to save a copy of `"original_photo.jpg"` with the Droste effect in the box bounded by the pixel coordinates `x1`, `y1`, `x2`, `y2`. Here `x1` denotes the left edge of the box, `y1` the top edge, `x2` the right and `y2` the bottom edge.

### To-do

Create a skew version to handle non-square boxes.
