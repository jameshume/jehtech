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
can yield the vector $[a, b]$.

Same with the signal $x(t) = a\cos(\omega t) + b\sin(\omega t)$. If I just have the signal $x(t)$, in the same way as I did above,
I can decompose it into the basis functions $\cos(\omega t)$ and $\sin(\omega t)$.

How?

To get $a$, do the following...

Multiply both sides by \cos(\omega t). This gives

$$
\begin{align}
    \text{As}\ x(t) = a\cos(\omega t) + b\sin(\omega t) \\\\
    \therefore x(t)\cos(\omega t) &= [a\cos(\omega t) + b\sin(\omega t)]\cos(\omega t) \\\\
                                  &= a\cos(\omega t)\cos(\omega t) + b\sin(\omega t)\cos(\omega t) \\\\
                                  &= a\cos^2(\omega t) + b\sin(\omega t)\cos(\omega t)
\end{align}
$$

Integrate that result over one period.


$$
\begin{align}
&\int_{0}^{T} a\,\underbrace{\cos^2(\omega t)}_{\int =\,\frac{T}{2}} + b\,\underbrace{\sin(\omega t)\cos(\omega t)}_{\int =\, 0} \\\\
& = a\frac{T}{2}
\end{align}
$$

Thus we have a forumla that results in $a\frac{T}{2}$. Multiple by $\frac{T}{2}$ to remove the half-period to ge just $a$. This gives us the result

$$
a = \frac{T}{2} \int_{0}^{T} a\,\cos^2(\omega t) + b\,\sin(\omega t)\cos(\omega t)
$$

This completely an unambiguously extracts the "amount", $a$ of the basis vector $\cos(\omega t)$ contained in our signal $x(t)$.