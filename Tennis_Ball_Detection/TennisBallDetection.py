
import cv2
import numpy as np
import imutils
from tkinter import *
import webbrowser
from PIL import ImageTk, Image
from abc import ABC, abstractmethod


class tennis_ball_detect(ABC):
    @abstractmethod
    def number_of_balls(self):
        pass

    @abstractmethod
    def coordinate(self):
        pass


class region_number(tennis_ball_detect):
    def number_of_balls(self):
        pass

    def coordinate(self):
        pass

    def centroid(self):
        # To read video from file:
        # webcam = cv.VideoCapture('Video.mp4')

        webcam = cv2.VideoCapture(0)  # For camera connection (0-1-2-3)

        def nothing(x):
            pass

        cv2.namedWindow("Trackbar")

        cv2.createTrackbar("LH", "Trackbar", 0, 179, nothing)
        cv2.createTrackbar("LS", "Trackbar", 0, 255, nothing)
        cv2.createTrackbar("LV", "Trackbar", 0, 255, nothing)
        cv2.createTrackbar("UH", "Trackbar", 0, 179, nothing)
        cv2.createTrackbar("US", "Trackbar", 0, 255, nothing)
        cv2.createTrackbar("UV", "Trackbar", 0, 255, nothing)

        ONLY_MAX = False  # if True only the max circle is drawn

        while True:

            ret, frame = webcam.read()
            frame = cv2.flip(frame, 1)  # cam flip
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lh = cv2.getTrackbarPos("LH", "Trackbar")
            ls = cv2.getTrackbarPos("LS", "Trackbar")
            lv = cv2.getTrackbarPos("LV", "Trackbar")
            uh = cv2.getTrackbarPos("UH", "Trackbar")
            us = cv2.getTrackbarPos("US", "Trackbar")
            uv = cv2.getTrackbarPos("UV", "Trackbar")

            # select color range:
            # green_range = ((29, 86, 6), (64, 255, 255))
            # orange_range = ((160, 100, 47), (179, 255, 255))
            # yellow_range = ((10, 100, 100), (40, 255, 255))

            # best green range values
            # lower_green = np.array([29, 86, 6])
            # upper_green = np.array([64, 255, 255])

            lower_green = np.array([lh, ls, lv])
            upper_green = np.array([uh, us, uv])

            mask = cv2.inRange(hsv, lower_green, upper_green)
            bitwise = cv2.bitwise_and(frame, frame, mask=mask)

            line_0 = cv2.line(frame, (0, 0), (0, 480), (0, 255, 0), 2)
            line_1 = cv2.line(frame, (128, 0), (128, 480), (0, 255, 0), 2)
            line_2 = cv2.line(frame, (256, 0), (256, 480), (0, 255, 0), 2)
            line_3 = cv2.line(frame, (382, 0), (382, 480), (0, 255, 0), 2)
            line_4 = cv2.line(frame, (510, 0), (510, 480), (0, 255, 0), 2)
            line_5 = cv2.line(frame, (640, 0), (640, 480), (0, 255, 0), 2)

            contour = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            if len(contour) > 1:
                pixelArray = []
                greenPixels = np.sum(mask == 255)
                pixelArray.append(greenPixels)
                textBegin = 20
                index = 0
                Text = "Total Pixel: "
                cv2.putText(frame, Text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                for ctr in contour:
                    if ONLY_MAX:
                        cmax = max(contour, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(cmax)
                    else:
                        ((x, y), radius) = cv2.minEnclosingCircle(ctr)

                    if radius >= 25:  # draw circle if radius>40 px
                        # pi = 3.141592
                        # area_circle = pi * radius * radius
                        totalPixels = "Pixel= " + str(pixelArray)
                        cv2.putText(frame, totalPixels, ((int(x), int(y + radius + 10))),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)

                        strXY = str(int(x)) + "," + str(int(y))
                        cv2.putText(frame, strXY, (int(x), int(y)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    """
                    for cmax in contour:
                        xValue = 0
                        ((x, y), radius) = cv2.minEnclosingCircle(cmax)
                        xValue = int(x)
                        yValue = int(y)
                        try:
                            if xValue > 0 & xValue <= 128 & yValue > 0 & yValue < 480:
                                print("Our tennis ball is in the 1. region.")
                            if xValue > 128 & xValue <= 256 & yValue > 0 & yValue < 480:
                                print("Our tennis ball is in the 2. region")
                            if xValue > 256 & xValue <= 382 & yValue > 0 & yValue < 480:
                                print("Our tennis ball is in the 3. region")
                            if xValue > 382 & xValue <= 510 & yValue > 0 & yValue < 480:
                                print("Our tennis ball is in the 4. region")
                            if xValue > 510 & xValue <= 640 & yValue > 0 & yValue < 480:
                                print("Our tennis ball is in the 5. region")

                        except ValueError:
                            print("Ball not detect")
                            continue


                # could not be implemented :(

                xRegion = []
                xRegion.append(int(xValue))
                dynamicValue = 10
                regionValue = 0
                for ballRegion in xRegion:
                    dynamicValue = dynamicValue + 20
                    regionValue = regionValue + 1
                    cv2.putText(frame, "Ball Region" + str(regionValue) + ":" + str(ballRegion), (120, dynamicValue),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                """

                for Pixels in pixelArray:
                    textBegin = textBegin + 20
                    index = index + 1
                    cv2.putText(frame, str(Pixels), (10, textBegin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            cv2.imshow("RegionNumber", frame)
            cv2.imshow("mask", mask)
            cv2.imshow("bitwise", bitwise)

            if cv2.waitKey(4) & 0xFF == ord('q'):
                break

        webcam.release()
        cv2.destroyAllWindows()


class general_control(tennis_ball_detect):
    def __init_(self, a, b, c):
        self.__number_of_ball = a
        self.__coordinate = b
        self.__centroid = c

    def number_of_balls(self):
        return self.__number_of_ball

    def coordinate(self):
        return self.__coordinate

    def centroid(self):

        webcam = cv2.VideoCapture(0)  # For camera connection (0-1-2-3)

        def nothing(x):
            pass

        cv2.namedWindow("Trackbar")

        cv2.createTrackbar("LH", "Trackbar", 0, 179, nothing)
        cv2.createTrackbar("LS", "Trackbar", 0, 255, nothing)
        cv2.createTrackbar("LV", "Trackbar", 0, 255, nothing)
        cv2.createTrackbar("UH", "Trackbar", 0, 179, nothing)
        cv2.createTrackbar("US", "Trackbar", 0, 255, nothing)
        cv2.createTrackbar("UV", "Trackbar", 0, 255, nothing)

        ONLY_MAX = False  # if True only the max circle is drawn

        while True:

            ret, frame = webcam.read()
            frame = cv2.flip(frame, 1)  # cam flip
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lh = cv2.getTrackbarPos("LH", "Trackbar")
            ls = cv2.getTrackbarPos("LS", "Trackbar")
            lv = cv2.getTrackbarPos("LV", "Trackbar")
            uh = cv2.getTrackbarPos("UH", "Trackbar")
            us = cv2.getTrackbarPos("US", "Trackbar")
            uv = cv2.getTrackbarPos("UV", "Trackbar")

            lower_green = np.array([lh, ls, lv])
            upper_green = np.array([uh, us, uv])

            mask = cv2.inRange(hsv, lower_green, upper_green)
            bitwise = cv2.bitwise_and(frame, frame, mask=mask)

            contour = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            if len(contour) > 1:
                for ctr in contour:
                    if ONLY_MAX:
                        cmax = max(contour, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(cmax)
                    else:
                        ((x, y), radius) = cv2.minEnclosingCircle(ctr)

                    if radius >= 20:  # draw circle if radius>40 px
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)

                        strXY = str(int(x)) + "," + str(int(y))
                        cv2.putText(frame, strXY, (int(x), int(y)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            cv2.imshow("Coordinate", frame)
            cv2.imshow("mask", mask)
            cv2.imshow("bitwise", bitwise)

            if cv2.waitKey(4) & 0xFF == ord('q'):
                break

        webcam.release()
        cv2.destroyAllWindows()


def main():
    arayuz = Tk()
    arayuz.geometry('520x580')
    arayuz.title("Tennis Ball Detection")
    arayuz.configure(bg='SlateGray1')

    logo = Image.open("thku_logo.png")
    photo = ImageTk.PhotoImage(logo)
    lab = Label(image=photo, bg='SlateGray1')
    lab.pack(pady=10)

    logo2 = Image.open("tennis_ball.png")
    photo2 = ImageTk.PhotoImage(logo2)
    lab2 = Label(image=photo2, bg='SlateGray1')
    lab2.pack()

    label_0 = Label(arayuz, text="Tennis Ball Detection", bg='greenyellow', relief="solid", width=20,
                    font=("arial", 19, "bold"))
    label_0.pack(pady=20)

    def cikis():
        exit()

    def regionNumberFind():
        a = region_number()
        a.centroid()

    def coordinateFind():
        b = general_control()
        b.centroid()

    def openURL(x):
        new = 2
        webbrowser.open(x, new=new)

    # create buttons:

    button1 = Button(arayuz, text='Region Number', width=20, bg='RoyalBlue4', fg='white',
                     command=regionNumberFind).pack(pady=15)

    button2 = Button(arayuz, text='Coordinates', width=20, bg='RoyalBlue4', fg='white',
                     command=coordinateFind).pack(pady=15)
    button_exit = Button(arayuz, text='Exit', width=12, bg='darkred', fg='white',
                         command=cikis).pack(pady=25)

    label_1 = Label(arayuz, text="Designed by Furkan YILMAZ", bg='SlateGray1', fg='black', width=25,
                    font=("bold", 12)).pack(side=TOP)

    button_link_1 = Button(arayuz, text='Furkan YILMAZ\n -LinkedIn-', width=17, bg='SteelBlue2', fg='black',
                           command=lambda: openURL("https://www.linkedin.com/in/furkann-yilmaz/")).pack(side=LEFT)

    button_link_2 = Button(arayuz, text='Dr. Masoud LATIFI NAVID\n -LinkedIn-', width=20, bg='SteelBlue2', fg='black',
                           command=lambda: openURL("http://linkedin.com/in/masoud-latifinavid")).pack(side=RIGHT)

    arayuz.mainloop()


if __name__ == "__main__":
    main()

