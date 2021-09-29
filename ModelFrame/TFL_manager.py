import numpy as np

from ModelFrame.Parts import Authentication_TFL, Distance_TFL
from ModelFrame.Parts.find_tfl import Find_TFL
from tensorflow.keras.models import load_model

"""
The tfl_Manager will be running all the parts of the project by creating an instance of every part object
Here he will manage the input and output to every part 
"""


class TFl_manager:
    def __init__(self, focal, pp):
        self.model = self.get_model()
        self.current_frame = None
        self.prev_path = ""
        self.prev_tfl_points = []
        self.focal = focal
        self.pp = pp

    """
    Loads the model we have created for part 2 that identifies whether it's really a traffic light or not
    """

    def get_model(self):
        loaded_model = load_model("C:/Users/pokro/Downloads/part4mobilie (1)/part4mobilie/ModelFrame/model.h5")
        return loaded_model

    """"
    This is where the controller gets us and it will be running all three of our parts by creating an object 
    for every part and running it on it's necessary imput and sending it's output to the next part....
    """

    def run_all(self, path, currentEm=None):

        """Part 1 finds all possible candidates for traffic lights"""
        find_tfl = Find_TFL()
        red_candidates, green_candidates = find_tfl.run(path)

        """Part 2 returns the verified traffic lights"""
        authentication_tfl = Authentication_TFL(path, self.model)
        red_TFLs, green_TFLs = authentication_tfl.run(red_candidates, green_candidates)

        """"makes sure the number of traffic lights did not increase after modeling in part 2"""
        try:
            assert len(red_TFLs) <= len(red_candidates) and len(green_TFLs) <= len(green_candidates)
        except AssertionError as msg:
            print(msg, ": could not have more point's after modeling")

        """Part 3 returns an object of frame model with it's updates properties that were calculated"""
        current_frame = None
        prev_frame = None
        new_tfl = red_TFLs + green_TFLs
        if self.prev_path:
            distance_tfl = Distance_TFL()
            current_frame, prev_frame = distance_tfl.run(path, self.prev_path, new_tfl, self.prev_tfl_points, currentEm,
                                                         self.focal, self.pp)

        self.prev_tfl_points = new_tfl
        self.prev_path = path

        """this will return the controller all the information calculated for this current frame"""
        return np.array(red_candidates), np.array(green_candidates), np.array(red_TFLs), np.array(
            green_TFLs), current_frame, prev_frame
