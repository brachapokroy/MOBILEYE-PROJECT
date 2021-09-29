import pickle

import numpy as np

from ModelFrame.TFL_manager import TFl_manager
from View.view import View

"""
The program is handled by the controller.
The controller has an instance of tfl_Manger that by him the actual program will be compiled
The controller gets a file that is like a user's imput
which contains the current pkl file, the starting index of the photos and a series of photos paths
taken in slightly different times
"""


class Controller:

    def __init__(self, pls_path):
        self.pls_path = pls_path
        self.pkl, self.index, self.frame_list = self.get_paths()
        self.data = self.load_data()
        self.focal = self.data['flx']
        self.pp = self.data['principle_point']
        self.tfl_man = TFl_manager(self.focal, self.pp)
        self.run()

    """
    loading the pkl file which contains the information of our focal and pp
    """

    def load_data(self):
        with open(self.pkl, 'rb') as pklfile:
            data = pickle.load(pklfile, encoding='latin1')
        return data

    """
    parsses over  the input file and extract's the data
    the pkl file path
    the starting index
    an array of paths for all the photos
    """

    def get_paths(self):
        pkl = ""
        frame_list = []
        with open(self.pls_path, "r") as pls_file:
            paths_list = pls_file.readlines()
            for path in paths_list:
                path = path.strip('\n')
                if path.endswith('pkl'):
                    pkl = path
                elif path.endswith('png'):
                    frame_list.append(path)
                else:
                    index = int(path)
        return pkl, index, frame_list

    """
    calculates the current egomotion_matrix according to it's formula
    """

    def calculate_EM(self, prev_frame_id, curr_frame_id, EM=np.eye(4)):

        if prev_frame_id < 0:
            return EM
        for i in range(prev_frame_id, curr_frame_id):
            EM = np.dot(self.data['egomotion_' + str(i) + '-' + str(i + 1)], EM)
        return EM

    """
     Here the controller actually starts running the program by running the tfl_manage run
    The tfl_manager run_all function receives the current image's path and it's egomotion_matrix
    """

    def run(self):

        currentEm = np.eye(4)

        # we will first fun on the first image because it does not have a previous one
        self.tfl_man.run_all(self.frame_list[0], currentEm)

        # iterates over the photo's array path and calculate's it's index and egomotion_matrix
        # then runs the tfl_mananger run function
        for frame in self.frame_list[1:]:
            prev_frame_id = int(frame.strip('_leftImg8bit.png')[-2:])
            currentEm = self.calculate_EM(prev_frame_id - 1, prev_frame_id, currentEm)
            red_candidates, green_candidates, red_TFLs, green_TFLs, current_frame, prev_frame = self.tfl_man.run_all(
                frame, currentEm)

            # sends the view object the returned data to be displayed
            View(frame, red_candidates, green_candidates, red_TFLs, green_TFLs, current_frame, prev_frame, self.focal,
                 self.pp)


if __name__ == '__main__':
    controler = Controller('play_list.pls')
    controler.run()
