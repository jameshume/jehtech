## References
* [Strapdown Inertial Navigation Technology (IEE Radar, Sonar, Navigation and Avionics Series)](https://www.slideshare.net/slideshow/strapdown-inertial-navigation-technology-iee-radar-sonar-navigation-and-avionics-series-pdfdrive-pdf/276598897)
* [Basic Inertial Navigation](https://www.slideshare.net/slideshow/basicnav/22449233)
* [NED (North-East-Down) Frame](https://www.sbg-systems.com/glossary/ned-north-east-down/)
* [How does an INS work?](https://inertiallabs.com/how-does-an-ins-works/)
* [Towards understanding IMU: Frames of reference used to represent IMU orientation and how to visualize the circuit orientation using Vpython library](https://atadiat.com/en/e-towards-understanding-imu-frames-vpython-visualize-orientation/)

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
A vehicle lets say, moving at a constant attitude.

![2D Example](##IMG_DIR##/2d_inertial_nav_example.png)

A gyro measures angular velocity, $\omega$, so get get the angle of the base frame w.r.t to the navigation frame
we integrate $\omega$ w.r.t. time:

$$
\theta(t) = \int_{t_0}^{t} \omega(\tau)\, d\tau
$$

Where $\tau$ is a dummy variable for integration ($t$ used for the integration limits).

Once we have $\theta$ that will rotate the force from the body to reference frame we can do the rotation - well i think it is more
of a projection of the body force vectors onto the nagivation frames axis:

![Project body frame force vectors onto navigation frame E, or x, axis](##IMG_DIR##/inertial_nav_project_body_forces_to_reference_x.png)

So we get:

$$
x_i = \left| z_b \right| \sin(\theta) + \left| x_b \right| \cos(\theta)
$$

And using similar reasoning:

$$
z_i = \left| -x_b \right| \sin(\theta) + \left| z_b \right| \cos(\theta)
$$

These forces measured by the IMU are accelleration. Integrate to get velocity and again to get distance.

$$
\begin{align}
V_{x_i}(t) = \int_{t_0}^{t} x_i(\tau) \, d\tau + V_0 \\\\
           = \int_{t_0}^{t} \left| z_b(\tau) \right| \sin(\theta(\tau)) + \left| x_b(\tau) \right| \cos(\theta(\tau)) \, d\tau  + V_0 \\\\
           = \Bigl[ \left| z_b(t) \right| -\cos(\theta(t))  + \left| x_b(t) \right| \sin(\theta(t)) + K_1 \Bigr]
              - \Bigl[ \left| z_b(t_0) \right| -\cos(\theta(t_0))  + \left| x_b(t_0) \right| \sin(\theta(t_0)) + K_2 \Bigr] + V_0 \\\\
           = \Bigl[ \left| z_b(t_0) \right| \cos(\theta(t_0)) -\left| z_b(t) \right| \cos(\theta(t)) \Bigr]
                + \Bigl[ \left| x_b(t) \right| \sin(\theta(t)) - \left| x_b(t_0) \right| \sin(\theta(t_0)) \Bigr] + V_0 + K
                        
\end{align}
$$