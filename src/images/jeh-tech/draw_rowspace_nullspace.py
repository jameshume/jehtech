import matplotlib.pyplot as pl
import numpy as np
import matplotlib.animation as animation
import math

fig, ax = pl.subplots()
aniquiv = None
ani_theta = 0.;

annotations = []

# y = 3/2x
def aniquiv_coords(x, theta_deg):
    y = 3./2. * x
    vec_a = np.array([27./13., -2./3. * 27./13.])
    vec_a_len = np.linalg.norm(vec_a)
    vec_c = np.array([2, 3])
    unit_vec_c = vec_c / np.linalg.norm(vec_c)
    scaler = math.tan(np.deg2rad(theta_deg)) * vec_a_len
    scaled_vec_c = vec_c * scaler
    vec_b = scaled_vec_c + vec_a
    return [(x,y), (vec_b[0], vec_b[1])]


def init():
    global aniquiv
    c = aniquiv_coords(0, ani_theta)
    aniquiv = ax.quiver(c[0][0], c[0][1], c[1][0], c[1][1], color='b', angles='xy', scale_units='xy', scale=1, zorder=1, alpha=0.5)
    # 27./13., -2./3. * 27./13.

    ax.quiver(0, 0, 2./3., 1, color='r', angles='xy', scale_units='xy', scale=1, zorder=2)
#    ax.quiver(3, 0, 2./3., 1, color='g', angles='xy', scale_units='xy', scale=1, zorder=2)
    ax.quiver(0, 0, 27./13., -2./3. * 27./13., color='b', angles='xy', scale_units='xy', scale=1, zorder=2)
    
    ax.plot([27./13.], [-2./3. * 27./13.], marker='o', markersize=4, color="black", zorder=1)
    ax.plot([-10, 10], [-15, 15], color='r', zorder=0, alpha=0.5)
    ax.plot([-10, 10], [20.0/3.0, -20.0/3.0], color='b', zorder=0, alpha=0.5)
    ax.plot([-7, 13], [-15, 15], color='g', zorder=0, alpha=0.5)

    ax.grid();
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

    a = ax.annotate( r'Solution set'
               , xy=(.75, -3.4)
               , xytext=(10, -40)
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(facecolor='green', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="g", alpha=0.5)
    )
    annotations.append(a)

    a = ax.annotate( r'$\vec{n_o}\in \mathrm{N}(A)$'
               , xy=(2./12., 0.25)
               , xytext=(-30, 35)
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(facecolor='red', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="r")
    )
    annotations.append(a)

    a = ax.annotate( r'$\mathrm{N}(A)$'
               , xy=(-2, -3)
               , xytext=(-10, 35)
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(facecolor='red', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="r", alpha=0.5)
    )
    annotations.append(a)

    a = ax.annotate( r'$\vec{r_0}\in\mathrm{C}(A^T)$'
               , xy=(0.9, -0.6)
               , xytext=(-30, -40)
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(facecolor='blue', shrink=0.05, connectionstyle="arc3,rad=-0.1", fc="b")
    )
    annotations.append(a)
    
    a = ax.annotate( r'$\mathrm{C}(A^T)$'
               , xy=(-3, 2)
               , xytext=(-30, -40)
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(facecolor='blue', shrink=0.05, connectionstyle="arc3,rad=-0.1", fc="b", alpha=0.5)
    )
    annotations.append(a)

state = "up"

def animate(i):
    global ani_theta
    global aniquiv
    global state
    global annotations

    # if i < 50:
    #   return aniquiv
    # elif i == 50:
    #   for a in annotations:
    #     print(dir(a))
    #     a.remove()



    if state == "up":
      ani_theta += .5
      if ani_theta > 15.:
        state = "down"
    else:
      ani_theta -= .5
      if ani_theta < -15.:
        state = "up"

    c = aniquiv_coords(-1.5, ani_theta)
    aniquiv.set_UVC(c[1][0],c[1][1])
    return aniquiv


Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='James Hume @ www.jeh-tech.com'), bitrate=1800)

ani = animation.FuncAnimation(fig, animate, frames= 30*4 + 4, init_func=init, interval=100, blit=False)
ani.save('animation.mp4', writer=writer)

