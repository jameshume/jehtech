Two signals are in quadrature if:

* They have the same frequency
* They differ in phase by exactly 90 degrees

Example:

$$
\begin{align}
    I(t) &= \cos(2\omega t) \\\\
    Q(t) &= \sin(2\omega t)
\end{align}
$$

These are quadrature signals.

The signals are **orthogonal**, i.e., they do not interfere with eachother which, for example, allows two independent signals to share the same carrier frequency - very useful!

I think of the orthogonality of the signals in the same way I was taught orthogonality for vectors (see [linear algrebra notes on orthogonality and indpendence](../mathsy_stuff/linear_alg.html#orthogonal_linear_independence)).

In linear algebra world, assuming the normal cartesian basis vectors, if I have a vector, $[a, b]$, I can decompose it into basis vectors like this - $a[1, 0] + b[0, 1]$ - and I can only decompose it this way. There is no other combination of basis vectors that
can yield the vector $[a, b]$. It's like I could mix two "signals", the vectors $[0,1]$ and $[1,0]$ in various quantities into a third signal, and then recover the original two signals and their "amplitudes" from that third, mixed up signal.

Same with the signal $x(t) = a\cos(\omega t) + b\sin(\omega t)$. If I just have the signal $x(t)$, in the same way as I did above,
I can decompose it into the basis functions $\cos(\omega t)$ and $\sin(\omega t)$. I.e. $x(t)$ is some mixed up jumble of two sinusoidal signals and I can recover the exact mix of the two sinusoids because those sinusoids are orthogonal or **quadrature** signals.

Sine and cosine are othogonal because:

$$
\int_{0}^{T} \cos(\omega t)\sin(\omega t)\,\mathrm{d}t = 0
$$

How?

To get $a$, do the following...

Multiply both sides of $x(t) = a\,\cos(\omega t) + b\,\sin(\omega t)$ by $\cos(\omega t)$. This gives

$$
\begin{align}
    x(t)\cos(\omega t) &= [a\,\cos(\omega t) + b\,\sin(\omega t)]\cos(\omega t) \\\\
                                  &= a\,\cos(\omega t)\cos(\omega t) + b\,\sin(\omega t)\cos(\omega t) \\\\
                                  &= a\,\cos^2(\omega t) + b\,\sin(\omega t)\cos(\omega t)
\end{align}
$$

Integrate that result over one period.
TEST

$$
\begin{align}
    &\int_{0}^{T} a\,\underbrace{\cos^2(\omega t)}_{\int =\,\frac{T}{2}} + b\,\underbrace{\sin(\omega t)\cos(\omega t)}_{\int =\, 0} \,\mathrm{d}t\\\\
    &= a\frac{T}{2}
\end{align}
$$

$$
\begin{align}
    \int_{0}^{T} a\,\underbrace{\cos^2(\omega t)}_{test} + \overbrace b{\sin(\omega t)\cos(\omega t)}^{test}\,\mathrm{d}t\\\\
    &= a\frac{T}{2}
\end{align}
$$


Thus we have a forumla that results in $a\frac{T}{2}$. Multiple by $\frac{2}{T}$ to remove the half-period to ge just $a$. This gives us the result

$$
a = \frac{2}{T} \int_{0}^{T} a\,\cos^2(\omega t) + b\,\sin(\omega t)\cos(\omega t)\,\mathrm{d}t
$$

This completely an unambiguously extracts the "amount", $a$ of the basis vector $\cos(\omega t)$ contained in our signal $x(t)$.

To find $b$ the same method is repeated, but with sine, to get:

$$
b = \frac{2}{T}\int_{0}^{T} x(t)\sin(\omega t)\,dt
$$
