import serial
import numpy as np
from math import atan2, degrees
from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight

# Panda3D window settings
loadPrcFileData('', 'window-title IMU 3D Viewer')
loadPrcFileData('', 'win-size 800 600')

# === IMU Setup ===
def setup_serial():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM3'
    ser.timeout = 1
    ser.open()
    return ser

def read_imu_data(ser):
    try:
        if not ser.is_open:
            ser.open()
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("#"):
            parts = line[1:].split(',')
            if len(parts) == 9:
                ax, ay, az = map(float, parts[0:3])
                return ax, ay, az
    except Exception as e:
        print("IMU read error:", e)
    return None, None, None

def get_lean_angles(ax, ay, az):
    # Calculate lean using simple tilt math
    try:
        roll = atan2(ay, az)
        pitch = atan2(-ax, np.sqrt(ay**2 + az**2))
        return degrees(roll), degrees(pitch)
    except:
        return 0.0, 0.0

# === Panda3D Game ===
class IMUGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        self.camera.setPos(0, -20, 5)
        self.setBackgroundColor(0.1, 0.1, 0.1, 1)

        # Lighting
        ambient = AmbientLight("ambient")
        ambient.setColor((0.4, 0.4, 0.4, 1))
        directional = DirectionalLight("directional")
        directional.setColor((0.8, 0.8, 0.8, 1))
        self.render.setLight(self.render.attachNewNode(ambient))
        self.render.setLight(self.render.attachNewNode(directional))

        # Load 3D model
        self.model = self.loader.loadModel("pirate.obj")  # Replace with actual filename
        self.model.reparentTo(self.render)
        self.model.setScale(1.0)
        # Position and orientation tweaks
        self.model.setPos(0, 0, 5)  # Move model up so it's visible
        self.model.setHpr(0, 0, 180)  # Rotate to stand upright

        # Setup serial
        self.ser = setup_serial()

        # Update loop
        self.taskMgr.add(self.update_model_task, "UpdateModelTask")

    def update_model_task(self, task):
        ax, ay, az = read_imu_data(self.ser)
        if ax is not None:
            roll, pitch = get_lean_angles(ax, ay, az)
            self.model.setHpr(0, pitch, -roll)  # Apply pitch (forward) and roll (side)
            print(f"Roll: {roll:.2f}, Pitch: {pitch:.2f}")
        return task.cont

if __name__ == "__main__":
    app = IMUGame()
    app.run()
