## TL;DR
Inductor voltage is proportional to rate of change of current:

$$
V = L\frac{\textrm{d}I}{\textrm{d}t} \text{  and  } i = \frac{1}{L}\int_0^T v\ \textrm{d}t + i_0
$$

Putting a constant voltage actoss an inductor causes the current to rise as a ramp: 1V across 1H produces a ramp of 1 amp per second.

Once current is stable, i.e. when a constant current flows in an inductor, then $\textrm{d}i/\textrm{d}t = 0$, so there is zero voltage across the inductor. This means the inductor looks like a short circuit, the same as a plain wire. [[Ref]](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic/ee-natural-and-forced-response/a/wmc-inductor-in-action)

Enery spent ramping up current:

$$
U_L = \frac{1}{2}LI^2
$$
Unlike resitors, power is not turned into heat: stored as energy in magnatic field.

Current flowing though coil creates a magnetic field.

Change in magnetic field induce a voltage (back EMF) in a way that tries to cancel out those changes.


## Magnetic Fields Caused By Currents Brief Intro
DC current through a wire creates a non-uniform, stable, magnetic field:

![](##IMG_DIR##/../uni_florida_mag_field_single_wire1.jpg)
<br><sup>Image (modified) from [University of Central Florida College Physics eBook](https://pressbooks.online.ucf.edu/phy2053bc/chapter/magnetic-fields-produced-by-currents-amperes-law/)</sup>

For a single wire use the right hand rule: thumb for current, curled fingers give the direction of the magnetic field.

For a single loop we have: 

![](##IMG_DIR##/../uni_florida_mag_field_loop1.jpg)
<br><sup>Image from [University of Central Florida College Physics eBook](https://pressbooks.online.ucf.edu/phy2053bc/chapter/magnetic-fields-produced-by-currents-amperes-law/)</sup>

For a coil, however, the magnetic field *inside* the coil is *uniform* and can be concentrated using a ferrous metal core. Outside the coil it is not uniform. For a loop/coil still use the right hand, but now the fingers are used for the current direction and the thumb gives the direction of the magnetic field through the coil.

![](##IMG_DIR##/../uni_florida_field_coil1.jpg)
<br><sup>Image from [University of Central Florida College Physics eBook](https://pressbooks.online.ucf.edu/phy2053bc/chapter/magnetic-fields-produced-by-currents-amperes-law/)</sup>

## Lenz's Law
Lenz's law states that the induced e.m.f in a circuit is directed so that the current it drives produces a magnetic field opposing the change in magnetic flux that produced it. And if we use the right hand rule (section above) we see therefore that the induced current opposes the current that is flowing through the coil. This is why Faraday's (next section) law includes a minus sign.

***Induced e.m.f produces current opposing inducing current***

In simpler terms, when you try to change the magnetic environment of a circuit, the circuit responds in a way that pushes back against that change. 

This means that when current is first passed through the inductor, the magnetic field is establish and for an incredibly short time, before it becomes stable, is changing. Thus a momentary EMF, opposing the EMF across the inductor, is generated.

So in a loop, magnetic force IN means current OUT
And changing current IN means magnetic force OUT

<blockquote>
    <p>
        Lenz's law can also be considered in terms of conservation of energy. If pushing a magnet into a coil causes 
        current, the energy in that current must have come from somewhere. If the <b>induced current causes a magnetic 
        field opposing the increase in field of the magnet we pushed in</b>, then the situation is clear. We <b>pushed 
        a magnet against a field and did work on the system, and that showed up as current</b>. If it were not the case 
        that the induced field opposes the change in the flux, the magnet would be pulled in and produce a current 
        without any work. Electric potential energy would have been created, violating the conservation of energy.
    </p>
    <footer>-- From [OpenStax](https://openstax.org/books/university-physics-volume-2/pages/13-2-lenzs-law) (emphasis mine)</footer>
</blockquote>
<p></p>

More easily digested like this: Imagine pushing a magnet toward a loop of wire. As the magnet gets closer, the magnetic field through the loop increases. The loop responds by creating its own magnetic field that tries to oppose the magnet coming closer.

A changing magnetic field through a conductor induces a voltage. That voltage drives a current around the loop. The direction of that current is not arbitrary. It is chosen so that the magnetic field produced by the current opposes the original change in magnetic flux.

This direction rule is Lenz's law.

In an inductor, a changing current creates a changing magnetic field. That field induces a voltage in the same conductor which opposes the change in current. This is why inductors resist sudden changes in current.


## Faraday's Law

![](##IMG_DIR##/../fardays_law_physics_stackexchange.png)
<br><sup>Image from [Physics Stack Exchange](https://physics.stackexchange.com/q/459470)</sup>


The flux density is $\mathbf{B}$.

The total flux is $\Phi$, also called "flux linkage":

$$
\Phi = N\mathbf{B}A
$$

Where $N$ is the number of turns in the coil and $A$ is the area of the coil.

Faraday's law says that the **EMF induced is proportional to the rate of change of flux through the loop**:

$$
e.m.f \propto -\frac{\textrm{d}\Phi}{\textrm{d}t}
$$

The $-$ (negation) is from Lenz's law to show the induced e.m.f will *oppose* the voltage generating it.

What is the constant of proportionality? It is the *inductance* of the coil:

$$
e.m.f = -L\frac{\textrm{d}I}{\textrm{d}t}
$$

Where $L$ is the inductance measured in "Henrys". 

***THUS, INDUCTORS OPPOSE CHANGES IN CURRENT***

But wait a minute! We just replaced $\frac{\textrm{d}\Phi}{\textrm{d}t}$ with $\frac{\textrm{d}I}{\textrm{d}t}$. Why were we able to do this?

The answer is that we can replace "rate of change of flux" with "rate of change of current" only in the special case where the flux is produced by that same current, which is what happens in self inductance.

For a coil (or any inductor), the magnetic field it produces is proportional to the current $i$: $\lambda \propto i$ [[Ref]](https://openstax.org/books/university-physics-volume-2/pages/14-2-self-inductance-and-inductors).

So,

$$
e.m.f \propto -\frac{\textrm{d}\Phi}{\textrm{d}t} \propto -\frac{\textrm{d}I}{\textrm{d}t}
$$

Thence we got to

$$
e.m.f = -L \frac{\textrm{d}I}{\textrm{d}t}
$$

In words, *the rate of current change in an inductor is proportional to the voltage across it*.


## The Effect Of Inductance
The following animation what happens when a square voltage pulse is put across an inductor for increasing values
of inductance.

FIXME? Not sure this is quite right?

<video autoplay loop muted playsinline>
  <source src="##IMG_DIR##/ltspice/electronics_pulse_into_ind_vary_inductance.mp4" type="video/mp4">
  Your browser does not support the video element.
</video>

We can see that there is an instantaneous change of voltage across the inductor, but that the inductor slows the increase of current: current *cannot change instantaneously* through an inductor. 

The current through the inductor will eventually be stable, and therefore the magnetic field will become
stable. We know from Faray's law that it is a *changing* current that generates a changing magnatic field and therefore
the "back EMF".

We can also see that when the voltage is "turned off", the inductor "fights" this. The change in voltage again
causes a change in magnetic field, which the inductor tries to oppose.

At the start, although the current is small, the *change in current* is *not* small, it can be quite large.

At the start, the induced back e.m.f. is limited. In a simple series RL circuit with a step DC voltage 
$𝑉$:

$$
V = v_R + v_l
$$

We know how to define the two volates so we can write:

$$
V = iR + L\frac{\textrm{d}i}{\textrm{d}t}
$$

So, when voltage first goes high, because no current is flowing (as per the graphs above) the
voltage across the resistor must be zero. 

Therefore, at $t = 0$, the entire voltage is across the inductor:

$$
V = v_l
$$

But, here's the thing, the change in current is *not* zero, so we get, at the start ($t = 0$):

$$
V = v_l = L\frac{\textrm{d}i}{\textrm{d}t}
$$

If we know the inductance, we know that the rate of change of current must be, just by rearranging the above
equation (again at $t = 0$):

$$
\left.\frac{\textrm{d}i}{\textrm{d}t}\right|_{t=0}=\frac{V}{L}
$$

As both $V$ and $L$ are finite values, the induced current is limited, i.e., not infinite, but it can
be very large if $V$ is large and/or $L$ is small.


## Reactance
This *opposition to the current* creating the magnetic field, as described by Lenz's law, is *like* a resistance, but it is not exactly resistance, even though it opposes current. Unlike resistors, which dissipate energy as heat, inductors (minus parasitics) do not dissipate energy, they store energy and return it later! I.e:

* Resistance removes energy from the circuit as heat.
* Reactance swaps energy back and forth between the source and the fields.

Reactance X is defined as a real number that measures how strongly an inductor, in this case, opposes AC at a given angular frequency.

An indictor's reactance $X_L$ at frequency $f$ is given by the following formula:

$$
\begin{align}
X_L &= 2\pi fL \\\\
    &= \omega L
\end{align}
$$

Where $X_L$ is the reactance of the inductor in Ohms, f is the frequency of the 
signal in Hz and L is the inductance in Henrys.

How did we get here? We set current like so:

$$
I(t) = I_0\sin(\omega t) \\\\
$$

Then the voltage across the inductor will be:

$$
\begin{align}
V(t) &= L\frac{\mathrm{d}I(t)}{\mathrm{d}t} \\\\
     &= L\omega I_0 \cos(\omega t)
\end{align}
$$

The ratio of *magnitudes* gives reactance, our resistance-like quantity:

$$
\begin{align}
    \frac{|V|}{|I|} &= \frac{L \omega I_0}{I_0}  \\\\
                    &= \omega L \\\\
                    &= X_L
\end{align}
$$

This shows that inductors have a frequency-dependent reactance, which increases with increasing frequency. So, a  series inductor could be used to pass dc and low frequencies (where its reactance is small) while blocking high
frequencies (where its reactance is high), for example.


## Voltage Leads Current
If we say that 

$$
i = \sin(\omega t)
$$

Then

$$
v = L\frac{\textrm{d}i}{\textrm{d}t} = L \omega \cos(\omega t)
$$

So we are comparing:

$$
\begin{align}
    i &= \sin(\omega t) \\\\
    v &= L \omega \cos(\omega t)
\end{align}
$$

Thus voltage leads current because the voltage cosine reaches its peak earlier in time. To know this, write one
function in terms of the other:

$$
\cos(\omega t) = \sin\left(\omega t + \frac{\pi}{2}\right)
$$

So we are comparing:

$$
\begin{align}
    i &= \sin(\omega t) \\\\
    v &= L\omega \sin\left(\omega t + \frac{\pi}{2}\right)
\end{align}
$$

This tells you directly that cosine is a sine shifted forward by $\pi/2$ radians. A positive phase shift corresponds
to a shift to the left in time, meaning the waveform reaches its peaks earlier (see [maths revision notes on function scaling and shifting](../mathsy_stuff/math_revision.html#function-scaling)). *So cosine leads sine by 90 degrees.*

For inductors think ELI - Voltage leads current, or put another way current lags voltage. In the example above
we note that because current is a sine wave and voltage is a cosine wave, both of the same frequency, 
that they are 90 degrees out of phase.

<img src="##IMG_DIR##/electronics_inductor_current_lags_voltage.png">

In the above the voltage and current aren't exactly 90 degrees out of phase. This is because the modelled components are non-ideal
and the 90 degree phase shift is for an ideal resistor and ideal inductor, where the latter would have pure inductance etc.

[This article](https://electricalacademia.com/basic-electrical/rl-series-circuit) and [this article (much simpler explanation I liked it more)](https://www.hamradioschool.com/post/complex-impedance-part-3-putting-it-all-together) explain it futher.


The two voltages across the resitor and inductor are a **vector** sum, and are not directly additive as such:

![](##IMG_DIR##/../electricalacademia.com_rl_vector_sum.png)
<br><sup>Image from [Electrical Academia - RL Series Circuit](https://electricalacademia.com/basic-electrical/rl-series-circuit/)</sup>


### A Little Aside...
But.... why was current chosen as a sine and not a cosine? Well, first, the current was specified rather than the
voltage because we get a simple derivative rather than an integral - a little easier I guess. Second, it
doesn't matter whether we say the current is a sine or cosine as the physics wont change! Voltage will
always lead current.

Lets instead say that:

$$
i = \cos(\omega t)
$$

Then, we get this:

$$
v = L\frac{\textrm{d}i}{\textrm{d}t} = -L \omega \sin(\omega t)
$$

It might look, if you consider the signals at time $t = 0$, that current leads voltage, but it does *not*: 
the confusion comes from using the value at a single instant to judge phase. Phase lead or lag is not determined 
by which signal is larger at t equals 0. It is determined by the relative phase angle between the two sinusoids.

But, we know 

$$
\sin(\omega t) = \cos\left(\omega t - \frac{\pi}{2}\right)
$$

So, we rewrite the voltage in this case as:

$$
v = L\frac{\textrm{d}i}{\textrm{d}t} = -L \omega \sin(\omega t) = -L \omega \cos\left(\omega t - \frac{\pi}{2}\right)
$$

So we are comparing:

$$
\begin{align}
i &= \cos(\omega t) \\\\
v &= -L \omega \cos\left(\omega t - \frac{\pi}{2}\right)
\end{align}
$$

Hence they are still 90 degrees out of phase, with voltage leading current (a negative phase shift means a shift to 
the right in time and the minus sign inverts the waveform.)


## Adding Complexity
Reactance is not complex in itself. Reactance is a real valued quantity. The complexity appears when reactance is combined with $j$ to represent phase. This is done when we talk about impedance, because impedance is $R + X_L$. We know that the voltage and current across the purely resistive component, $R$, are in phase, but across the inductive reactance component, voltage leads current; the two are out of phase by 90 degrees.

For pure resistance, lets choose current as our reference. We would then, on an argand diagram plot curret and voltage on the same axis, for example:

```
----------->--------> i(t)
           v(t)
```

But, for a purely reactive inductance, voltage and current are out of phase. Again, choose I as our reference (this is somewhat arbitrary, we could choose voltage) and we can plot on an argand diagram (see [maths revision notes on complex numbers](../mathsy_stuff/math_revision.html#complex-numbers)):

```
     V
     ^
     |
v(t) -
     |
     |-------|-------> I
             i(t)
```

We still maintain the corrrect magnitude for the voltage and current, but we have now also shown that they are
90 degrees out of phase. We'd express this relationship using a complex number in rectangular form as:

$$
v(t) + j i(t)
$$

Goto polar form:

$$
\begin{align}
r &= \sqrt{v(t)^2 + i(t)^2} \\\\
\theta &= \tan^{-1}(\frac{v(t)}{i(t)})
\end{align}
$$

To complex form:

$$
\sqrt{v(t)^2 + i(t)^2} e^{\tan^{-1}(\frac{v(t)}{i(t)})}
$$

Which can just be represented generically as:

$$
e^{j\theta}
$$

Thus, we have represented the amplitude of the signal and the phase relationship beteen voltage and current in one neat little package - the complex number.

Note that $j$ does not mean the component itself is imaginary. It is a mathematical marker that encodes the phase relationship between voltage and current. It allows phase shifts to be handled using algebra instead of trigonometry (see [maths revision notes on phasors](../mathsy_stuff/math_revision.html#phasors)).

*The physical quantity reactance remains real, but its effect on phase is represented using the imaginary axis.*






--
TODO
--
When we move to impedance, we need to represent both magnitude and phase. A +90 degree phase shift corresponds to multiplication by $j$, a -90 degree shift corresponds to minus $j$.

Thats why we sometimes see

$$
X_L = j \omega L
$$


So... we have complex inductance. The phase shift is the phase shift between voltage and current. We can no longer
represent current at some time, $t$, as just an amplitude, because we need to know its phase with respect to the voltage and vice versa.

We have already seen that we can write this (with phase now included):

$$
\begin{align}
I(t) &= I_0 \sin(\omega t ) \\
V(t) &= L \omega I_0 \cos(\omega t)
\end{align}
$$
--



## Inductors In Series

$$
L_{\text{eq}} = L_1 + L_2 + \cdots + L_n
$$

## Inductors In Parallel

$$
\frac{1}{L_{\text{eq}}} = \frac{1}{L_1} + \frac{1}{L_2} + \cdots + \frac{1}{L_n}
$$

So, for 2 inductors in parallel:

$$
L_{\text{eq}} = \frac{L_1L_2}{L_1 + L_2}
$$


## Worked Examples

### 1

![](##IMG_DIR##/electronics_inductance_worked_example_1.png)

We know $X_L = 2 \pi fL = 2 \pi \cdot 10^7 \cdot 2 \cdot 10^{-3} = 4\pi 10^4$.

