This simple python script iterates through all .jpg files in the folder in which it was run
For each image, it will use GPT-4 Vision to retrieve a description, and the image name and description will be stored in a text file ('image_descriptions.txt')
All of the image names and descriptions will also be stored in a numpy export ('filenames_and_descriptions.npy')

TODO: parallelize the calls to OPENAI to improve performance.
TODO: post sample code that will load the numpy file for later use.
