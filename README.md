# Spot Localization Test

This app will create a terminal printout of the Spot vision frame, Spot odom frame, and frames of all fiducials in range and output the data to a .csv file in the working directory.

First, clone the files:



Then build the docker image while in the app root directory:

```docker build -t localization_test .```

Then run the image using:

```sudo docker run -ti -v $(pwd):/pos_out/ localization_test --username USERNAME --password PASSWORD ROBOT_IP```

If making changes and debugging from a containerized environment in VSCode you can run the program without rebuilding the docker image using:

```python3 localization_test.py -vs --username USERNAME --password PASSWORD ROBOT_IP```