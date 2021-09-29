import numpy as np
from matplotlib import pyplot as plt
from ModelFrame import SFM


class View:
    def __init__(self,frame, red_candidates, green_candidates, red_TFLs, green_TFLs,current_frame,prev_frame,focal,pp):
        self.view_plot(frame, red_candidates, green_candidates, red_TFLs, green_TFLs,current_frame,prev_frame,focal,pp)

    def view_plot(self, path, red_candidates, green_candidates, red_TFLs, green_TFLs,current_frame,prev_frame,focal,pp):
        fig, (distance_sec, tfl_sec, suspicious_sec) = plt.subplots(1, 3, figsize=(12, 6))

        fig.canvas.set_window_title('Mobileye Project 2020')
        plt.suptitle(f"Frame {path}")

        '''part 1'''
        suspicious_sec.set_title('Suspicious candidates')
        suspicious_sec.imshow(plt.imread(path))
        suspicious_sec.plot(red_candidates[:, 0], red_candidates[:, 1], 'ro', color='r', markersize=4)
        suspicious_sec.plot(green_candidates[:, 0], green_candidates[:, 1], 'ro', color='g', markersize=4)

        '''part 2'''
        tfl_sec.set_title('Traffic light candidates')
        tfl_sec.imshow(plt.imread(path))
        tfl_sec.plot(red_TFLs[:, 0], red_TFLs[:, 1], 'ro', color='r', markersize=4)
        tfl_sec.plot(green_TFLs[:, 0], green_TFLs[:, 1], 'ro', color='g', markersize=4)

        '''part 3'''

        distance_sec.set_title('tfl distances')
        if current_frame and prev_frame:
            norm_prev_pts, norm_curr_pts, R, norm_foe, tZ = SFM.prepare_3D_data(prev_frame, current_frame, focal, pp)
        #    norm_rot_pts = SFM.rotate(norm_prev_pts, R)
         #   rot_pts = SFM.unnormalize(norm_rot_pts, focal, pp)

            foe = np.squeeze(SFM.unnormalize(np.array([norm_foe]), focal, pp))

            distance_sec.imshow(current_frame.img)
            curr_p = current_frame.traffic_light
            distance_sec.plot(curr_p[:, 0], curr_p[:, 1], 'b+')

            for i in range(len(current_frame.traffic_light)):
                    distance_sec.plot([current_frame.traffic_light[i, 0], foe[0]], [current_frame.traffic_light[i, 1], foe[1]], 'b')
                    if current_frame.valid[i]:
                        distance_sec.text(current_frame.traffic_light[i, 0], current_frame.traffic_light[i, 1],
                                      r'{0:.1f}'.format(current_frame.traffic_lights_3d_location[i, 2]), color='r')
        elif current_frame:
            distance_sec.imshow(current_frame.img)
            #distance_sec.plot(foe[0], foe[1], 'r+')
            #distance_sec.plot(rot_pts[:, 0], rot_pts[:, 1], 'g+')

        plt.show()
