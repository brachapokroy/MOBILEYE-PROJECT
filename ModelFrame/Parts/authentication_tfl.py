try:
    import numpy as np

    from PIL import Image
except ImportError:
    print("Need to fix the installation")
    raise

"""
In this class we check whether thr traffic lights we found at part 1 are really traffic lights
we do this using a neural network that we trained on a dataset we built
for each image we create an instance by it's path and the model used
"""

class Authentication_TFL:
    def __init__(self, path, model):
        self.path = path
        self.model = model
        self.image = None

    """"
        for every traffic light candidate we found at part 1 we crop our image to size (81,81,3)
    """
    def __cropping(self, coord):
        width, height = 2048, 1024
        left = max(0, coord[0] - 41)
        top = max(0, coord[1] - 41)
        right = min(width, coord[0] + 40)
        bottom = min(height, coord[1] + 40)
        image_from_array = Image.fromarray(self.image)
        cropped_image = image_from_array.crop((left, top, right, bottom))
        if np.array(cropped_image).shape != (81, 81, 3):
            return None
        return cropped_image

    """
        Here we verify for a cropped image if it's a real traffic light or not
        By using the prediction of our model
        we assume the if the model predicts the image with a score higher than 0.5 it's really a traffic light
        and it will return 1,otherwise it is not ans we will return zero
    """
    def __is_tfl(self,image):
        crop_shape = (81, 81)
        test_image =np.array(image).reshape([-1] + list(crop_shape) + [3])
        predictions = self.model.predict(test_image)
        predicted_label = np.argmax(predictions, axis=-1)
        #predicted_label = 1 if predictions > 0.5 else 0
        return predicted_label

    """
    This functions receives the array of candidates
    it iterates over them and send the coordinates that round them the image will get cropped
    If that image is not being ignored and the score for the cropped image is 1
    it will be appended as a verified traffic light
    and will return the run function the  verified  traffic lights 
    """
    def __get_tfls(self, candidates):
        candidates_tfl = []
        for index, pixel in enumerate(candidates):
            crop_image = self.__cropping(candidates[index])
            if crop_image and self.__is_tfl(crop_image):
                candidates_tfl.append(pixel)
        return candidates_tfl

    """
    This function is called from the tfl_manager for part 2 and it returns the verified  traffic lights
    by calling other functions that validate the candidates
    """
    def run(self, red_candidates, green_candidates):
        self.image = np.array(Image.open(self.path))
        red_tfls = self.__get_tfls(red_candidates)
        green_tfls = self.__get_tfls(green_candidates)
        return red_tfls, green_tfls
