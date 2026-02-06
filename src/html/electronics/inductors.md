DC current through a wire creates a non-uniform, stable, magnetic field.

PICTURE HERE

For a single wire  use the right hand rule: thumb for current, curled fingers give the direction of the magnetic field.

For a coil, however, the magnetic field *inside* the coil is *uniform* and can be concentrated using a ferrous metal core. Outside the coil it is not uniform. For a loop/coil still use the right hand, but now the fingers are used for the current direction and the thumb gives the direction of the magnetic field through the coil.

PICTURE HERE

## Lenz's Law
Lenz's Law states that the direction of an induced electric current or electromotive force (EMF) in a conductor, caused by a changing magnetic field, always opposes the change in magnetic flux that produced it

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


## Faraday's Law

INSERT DIAGRAM HERE

The flux density is $\mathbf{B}$.

The total flux is $\Phi$, also called "flux linkage":

$$
\Phi = N\mathbf{B}A
$$

Where $N$ is the number of turns in the coil and $A$ is the area of the coil.

*Faraday's law says that the **EMF induced is proportional to the rate of change of flux through the loop***:

$$
e.m.f \propto -\frac{d\Phi}{dt}
$$

The $-$ (negation) is from Lenz's law to show the induced e.m.f will *oppose* the voltage generating it.

What is the constant of proportionality? It is the *indictance* of the coil:

$$
e.m.f = L -\frac{dI}{dt}
$$

Where $L$ is the inductance measured in "Henrys". 

***THUS, INDUCTORS OPPOSE CHANGES IN CURRENT***

But wait a minute! We just replaced $\frac{d\Phi}{dt}$ with $\frac{dI}{dt}$. Why were we able to do this?

The answer is that we can replace "rate of change of flux" with "rate of change of current" only in the special case where the flux is produced by that same current, which is what happens in self inductance.

For a coil (or any inductor), the magnetic field it produces is proportional to the current $i$: $\lambda \propto i$ [[Ref]](https://openstax.org/books/university-physics-volume-2/pages/14-2-self-inductance-and-inductors).

So,

$$
e.m.f \propto -\frac{d\Phi}{dt} \propto -\frac{dI}{dt}
$$

Thence we got to

$$
e.m.f = L -\frac{dI}{dt}
$$

### Calculating L
TODO

## The Effect Of Inductance
The following animation what happens when a square voltage pulse is put across an inductor for increasing values
of inductance.

![](##IMG_DIR##/ltspice/electronics_pulse_into_ind_vary_inductance.mp4)

We can see that the instantaneous change of voltage across the inductor slows the increase of current so
that current *cannot change instantaneously* through an inductor. 

The current through the inductor will eventually be stable, and so threfore will the magnetic field will become
stable. We know from Faray's law that it is a *changing* current that the oposing e.m.f.

At the start, although the current is small, the *change in current* is *not* small, it can be quite large.

At the start, the induced e.m.f. is limited. In a simple series RL circuit with a step DC voltage 
$𝑉$:

$$
V = v_R + v_l
$$

We know how to define the two volates so we can write:

$$
V = iR + L\frac{di}{dt}
$$

So, when voltage first goes high, because no current is flowing (as per the graphs above) the
voltage across the resistor must be zero. 

Therefore, at $t = 0$, the entire voltage is across the inductor:

$$
V = v_l
$$


But, here's the thing, the change in current is *not* zero, so we get, at the start ($t = 0$):

$$
V = v_l = L\frac{di}{dt}
$$

If we know the inducance we know that the rate of change of current must be, just by rearranging the above
equation (again at $t = 0$):

$$
\left.\frac{di}{dt}\right|_{t=0}=\frac{V}{L}
$$

As bost $V$ and $L$ are finite values, the induced current is limited, i.e., not infinite, but it can
be very large if $V$ is large and/or $L$ is small.


## Reactance
This opposition to the current creating the magnetic field, as described by Lenz's law, is *like* a resistance, but because it is not exactly resistance, even though it opposes current. Unlike resistors, which dissipate energy as heat, inductors (minus parasitics) do not dissipate energy, they store energy and return it later! I.e:

* Resistance removes energy from the circuit as heat.
* Reactance swaps energy back and forth between the source and the fields.


An indictor's reactance $X_L$ at frequency $f$ is given by the following formula:

$$
X_L = 2\pi fL
$$

Where $X_L$ is the reactance of the inductor in Ohms, f is the frequency of the 
signal in Hz and L is the inductance in Henrys.

## Voltage Leads Current
if $i = \sin(\omega t)$, then

$$
v = L\frac{di}{dt} = L \cdot \omega \cos(\omega t)
$$

For inductors think ELI - Voltage leads current, or put another way current lags voltage:

<img src="##IMG_DIR##/electronics_inductor_current_lags_voltage.png">

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
