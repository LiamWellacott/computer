#!/usr/bin/env python

import face_recognition as fr
import numpy as np
import cv2
import os

class FaceWaker(object):
    """docstring for ."""

    def __init__(self):

        # list containing known faces
        self.known_enco = []
        self.known_name = []

        self.frame=None

        self.init_known(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'faces'))

    def get_name(self, filename):
        # Assumes that the filename is /path/to/file/name.extension
        _, name = os.path.split(filename)
        return os.path.splitext(name)[0]

    def init_known(self, face_dir):
        files = [os.path.join(face_dir, f) for f in os.listdir(face_dir) if os.path.isfile(os.path.join(face_dir, f))]
        for face_file in files:
            img = fr.load_image_file(face_file)
            # want a width of 128 to speed up the process, be sure not to run out of memory.
            scale = float(img.shape[1])/480.
            small_frame = cv2.resize(img, (0, 0), fx=1./scale, fy=1./scale)

            self.known_name.append(self.get_name(face_file))
            face_loc = fr.face_locations(small_frame, model='cnn')
            face_encoding = fr.face_encodings(small_frame, face_loc)[0]
            self.known_enco.append(face_encoding)

    def check(self):
        cam = cv2.VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()

        if not s:
            print('Error getting image from camera')

        #reduce this to speed things up but will reduce the accuracy
        scale=1
        small_frame = cv2.resize(img, (0, 0), fx=1./float(scale), fy=1./float(scale))
        # convert back to RGB, cv uses BGR conventiion.

        face_loc = fr.face_locations(small_frame, model='cnn')
        face_encodings = fr.face_encodings(small_frame, face_loc)

        face_names = []
        for enc in  face_encodings:
            matches = fr.compare_faces(self.known_enco, enc)
            name = "Unkown"
            face_distances = fr.face_distance(np.array(self.known_enco), np.array(enc))
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_name[best_match_index]

            face_names.append(name)

        return face_names

