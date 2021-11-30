# Spot Localization Test

This app will create a terminal printout of the Spot vision frame, Spot odom frame, and frames of all fiducials in range and output the data to a .csv file in the working directory.

First, build the docker image while in the app working directory:

```docker build -t localization_test .```

to run this file use:

```sudo docker run -ti -v $(pwd):/pos_out/ localization_test --username USERNAME --password PASSWORD ROBOT_IP```
