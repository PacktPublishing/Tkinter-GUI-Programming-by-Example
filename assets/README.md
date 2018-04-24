This is the assets folder for chapters 3 and 4.

To obtain the assets used by the book's author, download the images from this URL:

https://opengameart.org/sites/default/files/Free-Game-Assets-08-Playing-Cards.zip

Inside are three sets of cards. Choose which set you like more. Screenshots from the book are using "Modern". 

Copy the cards from this folder back into your "assets" folder. 

Now the images need to be resized and renamed.

This can be done from a command line using a program named "ImageMagick".

http://www.imagemagick.org/script/index.php

This python script should do it for you:

```python
import os

no = ["tabletop.png", "resize.py", "README.md", "sounds"]

filename_map = {
    "h": "Hearts",
    "d": "Diamonds",
    "c": "Clubs",
    "s": "Spades",
}

value_map = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K",
}

images = os.listdir()

for i in images:
    if i.startswith('.'):
        continue

    if i not in no:
        value = int(i[1:-4])
        if value == 1 or value > 10:
            value = value_map[value]
        filename = filename_map[i[0:1]] + str(value) + ".png"
        os.system(f"convert {i} -resize 80x111\> {filename}")


```

This script can be found in this folder, named `resize.py`. 

