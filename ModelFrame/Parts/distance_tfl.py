import numpy as np

from ModelFrame import SFM
from ModelFrame.Model_frame import Frame_Model

"""
This run function implements part 3 of calculating the distance to the traffic lights
It creates the current frame and the previous one
Now it can calculate the distance according to part 3
returns the updated frame
"""

class Distance_TFL:

    def run(self, new_path, curr_frame, new_tfl,curr_tfl, currentEm,focal,pp):
        prev_container = Frame_Model(curr_frame)
        curr_container = Frame_Model(new_path)
        prev_container.traffic_light = np.array(curr_tfl)
        curr_container.traffic_light = np.array(new_tfl)
        curr_container.EM = currentEm
        curr_container.corresponding_ind = SFM.calc_TFL_dist(prev_container, curr_container, focal, pp)
        return curr_container,prev_container

