import carla
import numpy as np

class Transform:
    '''Convenience class wrapping carla.libcarla.Transform, wrapping the information into
    numpy arrays:
    '''
    def __init__(self, transform):
        forward_vector = transform.get_forward_vector()
        right_vector   = transform.get_right_vector()
        up_vector      = transform.get_up_vector()
        self.forward_vector = np.array([forward_vector.x, forward_vector.y, forward_vector.z])
        self.right_vector   = np.array([right_vector.x, right_vector.y, right_vector.z])
        self.up_vector      = np.array([up_vector.x, up_vector.y, up_vector.z])
        
        self.inverse_matrix = np.array(transform.get_inverse_matrix())
        self.matrix         = np.array(transform.get_matrix())
        
        location      = transform.location
        self.location = np.array([location.x, location.y, location.z])
        
        rotation      = transform.rotation
        self.rotation = np.array([rotation.pitch, rotation.yaw, rotation.roll])

        self.x, self.y, self.z = self.location
        self.pitch, self.yaw, self.roll = self.rotation

# 1. Load the map you want
print("Connecting to CARLA...")
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

print("... Loading Town06 ...")
world = client.load_world('Town06')

# 2. Some settings
print("... Setting world...")
settings = world.get_settings()
settings.fixed_delta_seconds = 0.10
settings.synchronous_mode = True
world.apply_settings(settings)

# 3. Get spawnpoints
print("... Exporting spawnpoints...")
spawnpoints = [Transform(spawnpoint) for spawnpoint in world.get_map().get_spawn_points()]

with open("raw_spawn_data.js", "w+") as ff:
  # Start JS, and write header.
  ff.write("export var town06_csv = `x,y,z,pitch,yaw,roll\n")#,formatted\n")

  # For each row...
  for sp in spawnpoints:
    # ... write the first six entries...
    ff.write(
      f"{sp.x}, {sp.y}, {sp.z}, {sp.pitch}, {sp.yaw}, {sp.roll}\n"#, "
    )
    # ... and add the 'formatted' string.
    #ff.write(
      # quote each comma:
      #f"[{sp.x:.3f}\",\" {sp.y:.3f}\",\" {sp.z:.3f}\",\" {sp.pitch:.3f}\",\" {sp.yaw:.3f}\",\" {sp.roll:.3f}]\n"

      # quote the field
    #  f"\"[{sp.x:.3f}, {sp.y:.3f}, {sp.z:.3f}, {sp.pitch:.3f}, {sp.yaw:.3f}, {sp.roll:.3f}]\"\n"
    #)
  # Finish off by closing our backtick
  ff.write("`")

print("... Done!")