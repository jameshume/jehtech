## GNSS Basic Principles

* Satellites broadcast their exact ephemerides (data that represent the trajectory of an object over
  time) and time whilst orbiting about 20,000 Km above the earth's surface.

* The time for a radio signal to propagate to a point is directly proportional to the distance.

* Trilateration with multiple distances allows pinpointing the exact location in space.
    * Because the range estimation is based on blocks the satellites have extremely accurate clocks 
      (they use atomic clocks) and the clocks between satellites are synchronised.
          * For example a rubidium clock is accurate to 5 parts per 1E11!
    * Receiver clock is usually much less accurate! To avoid errors introduced by clock bias
      the receiver must "lock onto" the satellites clock.
          * For example, a quartz crystal might only be accirate to 5 parts per million! If a receiver
            used its own clock it would get an accuracy works than 1.5 Km, which would be awful!
          * To trilaterate in 3D, 3 satellites are required. To correct the receiver's clock a
            fourth satellite is required at a minimum, but in practice the more the better.
    * The distribution of satellites in the sky is important - need to be "spread out". Clustered
      satellites lead to a dilution of precision (DOP).

* GNSS architecture includes the space segment, control segment and user segment.
    * Space segment is the satellites,
    * Control segment is the base stations that update the satellites orbit parameters and clocks,
      when necessary. Data upload stations, master control stations and base stations.
    * User segment includes the GNSS receivers

* There are the following GNSS constellations:
    * GPS - world wide coverage - USA - 24 satellites
    * GLONASS - world wide coverage - Russia - 24 satellites
    * Galileo - world wide coverage - EU - 24 satellites
    * BeiDou - world wide coverage - China - 28 satellites
    * IRNSS - mainly continent coverage - India - 8 satellites
    * QZSS - m=ainly continent coverage - Japan - 4 satellites

* Satellite Signals
    * Each satellite has its own unique code (PRN -pseudo random noise numbers - which identify the ranging codes).
      Use in CDMA (code division multiplexing).
    * L1 GPS - Navigation Message
        * A navigation message is transmitted at 50 bps and contains 
            1. GPS date and time.
            2. Satellite status and health.
            3. Satellite ephemeris data - allows receiver to calculate satellite position - valid for only 4 hours.
            4. Almanac - consists of information and status of all GPS satellites so that receiver knows which sats are available for tracking - can be valid for up to 2 weeks.
        * Coarse acquisition code (C/A) - freely available to general public.
            * 1023 bits long and repeated every miliisecond.
        
