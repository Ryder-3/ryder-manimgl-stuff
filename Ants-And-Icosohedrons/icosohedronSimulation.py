from manimlib import *

# Add parent directory to Python path to import customMobject
sys.path.insert(0, str(Path(__file__).parent.parent))
import customMobject as cm


class MainSim(ThreeDScene):
    def construct(self):
        self.titleSequence(self)


    def titleSequence(self):
        title = TexText("")
    
    def mainSim(self):
        pass