## References
* [Strapdown Inertial Navigation Technology (IEE Radar, Sonar, Navigation and Avionics Series)](https://www.slideshare.net/slideshow/strapdown-inertial-navigation-technology-iee-radar-sonar-navigation-and-avionics-series-pdfdrive-pdf/276598897)
* [Basic Inertial Navigation](https://www.slideshare.net/slideshow/basicnav/22449233)
* [NED (North-East-Down) Frame](https://www.sbg-systems.com/glossary/ned-north-east-down/)

## Pitch, Roll, Yaw, and Attitude
![Pitch Roll and Yaw of a plane](##IMG_DIR##/../IMU_inertial_frame_atadiat.com.png)
<br><sup>Image from https://atadiat.com/en/e-towards-understanding-imu-frames-vpython-visualize-orientation</sup>

*Roll*: Rotation about the forward body axis. It describes *tilting left or right*.

*Pitch*: Rotation about the lateral body axis. It describes *tilting up or down*.

*Yaw*: Rotation about the vertical body axis. It describes *heading or turning left or right*.

*Attitude*: The orientation of the sensor body relative to a chosen reference frame. It describes how the body axes are rotated with respect to a navigation frame such as North East Down or Earth centred Earth fixed. For exampl, an aircraft is flying straight east, wings level, with its nose raised slightly. Its attitude is:

* Roll = 0 degrees, no left or right tilt.
* Pitch = 5 degrees nose up.
* Yaw = 90 degrees, pointing east relative to north.

This single set of angles fully describes the aircraft orientation relative to the navigation frame.

Attitude can be represented by the vector [roll, pitch, yaw], but attitude itself is a three dimensional rotation, not inherently a vector. It is a rotation between coordinate frames.

## Rotating Body Frame To Reference (Navigation) Frame

![Rotating body frame to reference fame image](##IMG_DIR##/imu_body_frame_to_reference_frame_rotation.png)

## A 2D navigation example
![2D Example](##IMG_DIR##/2d_inertial_nav_example.png)
