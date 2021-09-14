# MOBILEYE-PROJECT
In this Mobileye project we detect traffic lights and calculate the distance to them.

This project is divided into four parts. We worked gradually on each part until the complete and then we went on to the next part.
We used a huge dataset of pictures for our tests.

Part 1:
In this part we were meant to detect all suspicious points that can be a traffic light.We do this by building a kernel that will phrase over the image and activate the convolution function.Therefore the kernel we defined must be as close as possible to the traffic light features.
After trying and testing all types of kernel( such as a red and green circle surrounded by a black square,white circle...) we ended up doing a blurry white circle since the traffic light colour is usually not all a solid colour. Around it was a black square for the contrast that there is around a traffic light.
Then we divided our image into two matrix images(using the numpy library of python) , a red one and a green one.
Now we activate the convolution function on every matrix using the kernel we built. 
After phrasing on each matrix the highest pixels were the ones near a red or green traffic light since those were most alike the kernel.We take those max points for every area for red lights and green lights and these are our traffic lights candidates.
We realized that the kernel would only identify the TFLs that  were similar to it also in size so we then made our image smaller using Gaussian pyramid and doing all the above to the thumbnail.
The results were pretty good. We managed to get close to all the TFLs in every image though we did get some incorrect points.

Part 2:
In this part we had to build our own dataset and train it on a neuron network.
We build the dataset by iterating over our candidates points from part 1 and checking if they are real TFL or not.
For every real TFL we inserted one that is not a TFL in order to keep the ratio between them to be 50/50.
Every point we inserted we cropped around 81 height and 81 width we wrote that to a binary file called images and if it was a TFL we wrote 1 to a binary file called labels if it wasn't we wrote 0.
After our dataset was ready we divided it into training and validation.
Now we wanted to define a neuron network and train it.We decided to use the pretrained model VGG16 which is known to be good at image classification. 
We froze the layers so that they should not change every time.Then at the bottom layers we define our own classification that the output layer had as an activation function sigmoid, which is known to be used as giving the probability of a binary option a score between 0 -1.To match it up we used as our loss function "binary-corrostropy" that is also used for binary cases.
The results were not great but slowly by adding generators, changing optimizer, tuning the arguments we managed to improve the concurrency.
We also changed the threshold that was defined for the output result,instead of taking the max of each pair we scored the result by selecting if it was under 0.5 it would score 0 , if it was higher it would score 1.

Part 3:
In this part we had to find the estimated distance to all TFL.
To do this we have to have  two images one will be the current and the other will be the previos. The TFL light is defined as point p where we have a line in both images to the car in the rotated image we'll call it p'. The line between the cars in both images is called the baseline. Now we can define the epiporplane and having thet we can define the epipolar lines.Than by definition , P’s projection into the second image p must be located on the epipolar line of the second image.
To get the real position we used the formula that declares that to get from image to image it will be multiplied by a rotation R and then by a translation T(EGO MOTION).
in both the images from where we are calculating the distance to THAT POINT P. in a known time difference and then we will rotate the image that we will find a line to the Tfl in both images(epipoline) and then we can calculate the distance and then can use the formula of calculating the rotated image multiplied by a special matrix.
Than we find the distance by calculating the relatively between them and that will be the distance.

Part 4:
In this part we had to do the integration of all parts.
We did that by using the CMV pattern.
We had a controller class that was incharge of opening the input file and reading the shared data of all frames.
In an array we kept all the frame paths and then we iterated over it and activated it's run function of the tflManger object.
In the tflManger class we have a run function that runs all three parts by building an instance of every part and activating it's run function one after the other, using the output of part 1(our traffic candidates)  to be inserted to part 2(to be verified) and inserting the valid TFLs to part 3 to find the distances
After all this calculation the tflManger returns it's result to the controller.
The controller then builds an instance of the view class and activates its view function that will present the results of each part.
