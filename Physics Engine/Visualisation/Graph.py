import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
fig, (ax_y, ax_y2) = plt.subplots(1, 2)


def update(frame, simulation):
    ax_y.clear()
    ax_y2.clear()
    ax_y.set_xlim(right=-10, left=10)
    ax_y.set_ylim(bottom=-10, top=10)
    ax_y2.set_xlim(right=-10, left=10)
    ax_y2.set_ylim(bottom=-10, top=10)

    y, x, y2 = simulation()
    
    ax_y.plot(x, y, "o")
    ax_y.set_xlabel('X-axis')
    ax_y.set_ylabel('Y-axis')
    ax_y.set_title('y over x')

    ax_y2.plot(x, [y2, y2, y2], "o")
    ax_y2.set_xlabel('X-axis')
    ax_y2.set_ylabel('Y2-axis')
    ax_y2.set_title('y2 over x')
            
def Graph(dt, simulation):
    ani = FuncAnimation(
        fig,
        update,
        fargs=(simulation,),
        frames=range(700),
        interval=dt * 1000,
    )
    plt.show()

