# Image Resizer

This program creates resized image from source by given scale or width/height.

# Quick Start

Before start, you need to install Pillow library (if you have not it).
To get help of this program, type in command line:
```bash
python image_resize.py -h
```

Example of program works with scale given:
```bash
(lenv) user@Ihome:~/sproj/12_image_resize$ python image_resize.py -s 3 -f ~/Downloads/test_image.png 
Image saved at /home/user/Downloads as test_image__1500x1500.png
```

Example of program works with scale and output path given:
```bash
(lenv) user@Ihome:~/sproj/12_image_resize$ python image_resize.py -s 3 -f ~/Downloads/test_image.png -o /home/user/
Image saved at /home/user/Downloads as test_image__1500x1500.png
```

Launch in Windows is the same.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
