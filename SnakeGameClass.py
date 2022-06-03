import math
import cv2
import random
import numpy as np

import cvzone


class SnakeGameClass:

    def __init__(self, path_of_food):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.current_length = 0  # total length of the snake
        self.allowed_length = 150  # total allowed length
        self.previous_head = 0, 0  # previous head point
        self.thickness = 20

        self.imgFood = cv2.imread(path_of_food, cv2.IMREAD_UNCHANGED)
        self.imgFood = cv2.resize(self.imgFood, (64, 64))
        self.height_of_food, self.width_of_food, _ = self.imgFood.shape
        self.food_points = 0, 0
        self.random_food_location()

        self.game_over = False

        self.score = 0

    def random_food_location(self):
        self.food_points = random.randint(100, 1000), random.randint(100, 600)

    def update(self, img_main, current_head):

        if self.game_over:
            cvzone.putTextRect(img_main, "GAME OVER", (300, 400), scale=7, thickness=5, offset=20)
            cvzone.putTextRect(img_main, f'SCORE: {self.score}', (300, 550), scale=5, thickness=5, offset=20)

        else:
            prev_x, prev_y = self.previous_head
            curr_x, curr_y = current_head

            self.points.append((curr_x, curr_y))
            distance = math.hypot(curr_x - prev_x, curr_y - prev_y)
            self.lengths.append(distance)
            self.current_length += distance
            self.previous_head = curr_x, curr_y

            # length reduction
            if self.current_length > self.allowed_length:
                for i, length in enumerate(self.lengths):
                    self.current_length -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.current_length < self.allowed_length:
                        break

            # Check if snake ate food
            rand_x, rand_y = self.food_points
            if rand_x - self.width_of_food//2 < curr_x < rand_x + self.width_of_food//2 \
                    and rand_y - self.height_of_food//2 < curr_y < rand_y + self.height_of_food//2:
                print("yum")
                self.random_food_location()
                self.allowed_length += 50
                self.score += 1
                print(self.score)

            # Draw snake
            if self.points:

                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(img_main, self.points[i - 1], point, (random.randint(200, 256), random.randint(200, 256),
                                                                       random.randint(200, 256)), self.thickness)
                        # self.thickness += 1
                cv2.circle(img_main, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

            # Draw Food
            rand_x, rand_y = self.food_points
            img_main = cvzone.overlayPNG(img_main, self.imgFood, (rand_x - self.width_of_food // 2,
                                                                  rand_y - self.height_of_food // 2))

            # Draw Score
            cvzone.putTextRect(img_main, f'SCORE: {self.score}', (50, 50), scale=3, thickness=5, offset=20)

            # Check for collision
            points = np.array(self.points[:-2], np.int32)  # take all points but the last two
            points = points.reshape((-1, 1, 2))
            cv2.polylines(img_main, [points], False, (0, 200, 0), 3)
            min_distance = cv2.pointPolygonTest(points, (curr_x, curr_y), True)  # true to return measure distance
            if -1 < min_distance < 1:
                print("hit")
                self.game_over = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.current_length = 0  # total length of the snake
                self.allowed_length = 150  # total allowed length
                self.previous_head = 0, 0  # previous head point
                self.thickness = 20

        return img_main
