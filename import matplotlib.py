import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import random

# Simulation parameters
road_length = 100          # Length of the road (x-axis)
traffic_light_pos = 70     # Position of the traffic light on the road
car_speed = 1.0            # Car speed (units per frame)
car_safe_distance = 3.0    # Minimum safe distance between cars
new_car_probability = 0.3  # Probability of a new car entering each frame

# Traffic light cycle settings (in frames)
cycle_period = 40          # Total cycle length (frames)
green_time = 20            # Duration of green light (frames)
yellow_time = 5            # Duration of yellow light (frames)
red_time = 15             # Duration of red light (frames)

def get_traffic_light_state(frame):
    """
    Determines the current state of the traffic light based on the frame number.
    Returns: "green", "yellow", or "red".
    """
    mod = frame % cycle_period
    if mod < green_time:
        return "green"
    elif mod < green_time + yellow_time:
        return "yellow"
    else:
        return "red"

# List to hold the x positions of cars on the road
cars = []

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 3))
ax.set_xlim(0, road_length)
ax.set_ylim(-2, 2)
ax.get_yaxis().set_visible(False)
ax.set_title("Traffic Light Simulation on a One-Way Street")

# Draw the road as a horizontal line
ax.plot([0, road_length], [0, 0], color='black', linewidth=2)

# Create a patch to represent the traffic light (a circle)
traffic_light_patch = patches.Circle((traffic_light_pos, 1.5), radius=1, color='green')
ax.add_patch(traffic_light_patch)

# List to hold patches representing cars
car_patches = []

def init():
    """Initialization function for the animation."""
    global car_patches
    # Remove any existing car patches
    for patch in car_patches:
        patch.remove()
    car_patches = []
    return ax.patches

def update(frame):
    """Update function called for each frame of the animation."""
    global cars, car_patches, traffic_light_patch

    # Update the traffic light state based on the current frame
    state = get_traffic_light_state(frame)
    if state == "green":
        traffic_light_patch.set_color("green")
    elif state == "yellow":
        traffic_light_patch.set_color("yellow")
    elif state == "red":
        traffic_light_patch.set_color("red")
    
    # Randomly add a new car at position 0
    if random.random() < new_car_probability:
        cars.append(0.0)
    
    # Sort cars in descending order (car closest to the light first)
    cars.sort(reverse=True)
    
    new_positions = []
    for i, pos in enumerate(cars):
        if i == 0:
            # Lead car: if it is not yet near the traffic light, keep moving
            if pos < traffic_light_pos - car_safe_distance:
                new_pos = pos + car_speed
            else:
                # If the car is near the light, it will stop if the light is red
                if state == "red":
                    new_pos = pos
                else:
                    new_pos = pos + car_speed
        else:
            # For following cars: ensure a safe gap from the car ahead
            leader_pos = new_positions[i - 1]
            target_pos = pos + car_speed
            if target_pos > leader_pos - car_safe_distance:
                new_pos = pos  # Car stops to maintain safe distance
            else:
                new_pos = target_pos
        new_positions.append(new_pos)
    
    cars = new_positions
    
    # Remove cars that have reached the end of the road
    cars = [pos for pos in cars if pos < road_length]
    
    # Remove old car patches from the axes
    for patch in car_patches:
        patch.remove()
    car_patches = []
    
    # Draw each car as a blue rectangle on the road
    for pos in cars:
        rect = patches.Rectangle((pos - 1, -0.5), 2, 1, color='blue')
        car_patches.append(rect)
        ax.add_patch(rect)
    
    return ax.patches

# Create and start the animation
ani = animation.FuncAnimation(fig, update, init_func=init, frames=200, interval=100, blit=False)
plt.show()
