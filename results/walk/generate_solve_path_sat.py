# Plotting based off of example found here:
# https://towardsdatascience.com/animations-with-matplotlib-d96375c5442c
# "Animations with matplotlib" by Parul Pandey (2019)

#importing libraries
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Isaac Rowe'), bitrate=1800)

fig = plt.figure()
#creating a subplot 
ax1 = fig.add_subplot(1,1,1)

data = open('uf20-0156.log','r').read()
xs = []
ys = []
lines = data.splitlines()
max_c = [0]
max_rd = 0
t1 = ax1.text(5, 84.5, "Max clauses satisfied: " + str(max_c),bbox=dict(facecolor='red', alpha=0.5))
t2 = ax1.text(5, 82.5, "Flips: 0\nClauses satisfied: 0", bbox=dict(facecolor='red', alpha=0.5))

print("Reading data from file (this could take a while).")
for line in lines:
    x, y = line.split(',') # Delimiter is comma    
    xs.append(int(x))
    ys.append(int(y))
        
plt.xlabel('Flips')
plt.ylabel('Clauses Matched')
plt.title('WalkSAT Solving Path')

ax1.set_xlim(min(xs), max(xs))
ax1.set_ylim(min(ys), max(ys))

def animate(i, max_c):
    if ys[i] > max_c[0]:
        max_c[0] = ys[i]
    t1.set_text("Max clauses satisfied: " + str(max_c[0]) + "/91" )
    t2.set_text("Flips: " +  str(xs[i]) +
        "\nClauses satisfied: " + str(ys[i]))
    if(i > 1):
        for line in ax1.lines:
            alpha = line.get_alpha()
            if(alpha > 0.01):
                line.set_alpha(0.99*alpha)
        ax1.plot(xs[i-1:i+1], ys[i-1:i+1], 'bo-', alpha = 1)
    return t1, t2
ani = animation.FuncAnimation(fig, animate, fargs=(max_c,), frames=len(xs), interval=1) 
#plt.show()
ani.save('walk_sat_example.mp4', writer=writer)