import cv2
import numpy as np
import pyautogui
import asyncio
import keyboard as kb

# takes the to-click.png and checks if it can be seen on the screen
class RecNClick():
    ### interrupt_key   - keyboard hotkey recognizable by keyboard.is_pressed(hotkey)
    ### click_interval  - how often the recognized image is clicked
    ### image_path      - path to image acceptable by cv2.imread
    def __init__(self, *, interrupt_key = 'k', click_interval = .5, image_path = 'to-click.png'):
        self.click_interval = click_interval
        self.interrupt_key = interrupt_key
        self.program_ended = False
        
        self.source = np.array(pyautogui.screenshot())
        self.template = cv2.imread(image_path)
        self.w, self.h = self.template.shape[:-1]

        self.res = cv2.matchTemplate(self.source, self.template, cv2.TM_CCOEFF_NORMED)
        self.threshold = 0.9
        self.pos = np.where(self.res >= self.threshold)
        
    # start the program
    def run(self):
        try:
            asyncio.run(self.check_interrupt())
        except Exception as e:
            with open("log.log", "w+") as file:
                file.write(str(e))
                print(e)
                input()
    
    # check if user pressed the exit key
    async def check_interrupt(self):
        main = asyncio.create_task(self.main_loop())
        while not self.program_ended:
            await asyncio.sleep(0.01)
            if kb.is_pressed(self.interrupt_key): # not using keyboard.wait since it's not an async func
                main.cancel()
                self.program_ended = True
   
   # recognize and click
    async def main_loop(self):
        try:
            while True:
                await asyncio.sleep(self.click_interval)
                self.source = np.array(pyautogui.screenshot())
                self.res = cv2.matchTemplate(self.source, self.template, cv2.TM_CCOEFF_NORMED)
                self.pos = np.where(self.res >= self.threshold)

                if self.pos[0].size > 0:
                    pt = (self.pos[1][0], self.pos[0][0])
                    pyautogui.click(pt[0] + self.h/2, pt[1] + self.w/2)

        except Exception as e:
            with open("log.log", "w+") as file:
                file.write(e)
                print(e)
                input()

        self.program_ended = True


if __name__ == "__main__":
    RecNClick().run()