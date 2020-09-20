from tkinter import simpledialog, Tk
import cv2
import os

print("Copyright (c) 2020 Danish Humair. All rights reserved.\n")

print('''Hotkeys:\n• r: reset\n• c: clear\n• u: undo\n• esc: exit\n''')

images = []
for f in os.listdir("."):
    if f[-4:] in (".jpg", ".png", "jpeg"):
        images.append(f)

print(f"Found {len(images)} images!")
for c in range(len(images)):
    print(f"[{c+1}] {images[c]}")
choice = int(input("\nChoice: "))-1

Tk().withdraw()
img = cv2.imread(images[choice])
ix = -1
iy = -1
ratio = 0
fontScale = 1.5
drawing = False
refDrawn = False
original = img.copy()
cache = img.copy()


def calc_distance(x, y):
    global ix, iy
    return ((x-ix)**2+(y-iy)**2)**0.5


def draw_line(event, x, y, flags, param):
    global img, ix, iy, ratio, fontScale, drawing, refDrawn, cache
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cache = img.copy()
        ix = x
        iy = y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = cache.copy()
            d = calc_distance(x, y)
            if refDrawn:
                d *= ratio
            cv2.line(img, pt1=(ix, iy), pt2=(x, y), color=(150, 0, 0), thickness=2)
            cv2.putText(img, str(int(d)), (x+8, y+8), cv2.FONT_HERSHEY_PLAIN, fontScale, (150, 0, 0), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img = cache.copy()
        d = calc_distance(x, y)
        if not refDrawn:
            ratio = simpledialog.askinteger(title="Reference Line", prompt="What is the real distance of this line?")/d
            refDrawn = True
            img = cache.copy()
            d *= ratio
            cv2.line(img, pt1=(ix, iy), pt2=(x, y), color=(0, 50, 0), thickness=2)
            cv2.putText(img, str(int(d)), (x+8, y+8), cv2.FONT_HERSHEY_PLAIN, fontScale, (0, 50, 0), 2)
        else:
            d *= ratio
            cv2.line(img, pt1=(ix, iy), pt2=(x, y), color=(0, 0, 0), thickness=2)
            cv2.putText(img, str(int(d)), (x+8, y+8), cv2.FONT_HERSHEY_PLAIN, fontScale, (0, 0, 0), 2)


cv2.namedWindow(winname="Golf King Measure")
cv2.setMouseCallback("Golf King Measure", draw_line)

while True:
    cv2.imshow("Golf King Measure", img)
    key = cv2.waitKey(10)
    if key == ord('r'):
        img = original.copy()
        refDrawn = False
    if key == ord('c'):
        img = original.copy()
    elif key == ord('u'):
        img = cache.copy()
    elif key == 27:
        break
