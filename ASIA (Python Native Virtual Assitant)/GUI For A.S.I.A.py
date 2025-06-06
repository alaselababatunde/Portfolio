import time
import pyttsx3
import pygame
import os
import sys
import threading
import multiprocessing

#initialize the pyttsx3 engine
def speak(text):
    global is_talking
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 190)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    is_talking = True
    print("A.S.I.A:" +text+"\n")
    engine.say(text)
    engine.runAndWait()
    is_talking = False


# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Load GIF frames from a folder
def load_gif_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".gif"):
            frame = pygame.image.load(os.path.join(folder_path, filename))
            frames.append(frame)
    return frames

# Load GIF frames for talking and not talking states
talking_frames = load_gif_frames(r"/home/alash-studios/Documents/Python_Scripts/PythonProject/A.S.I.A/Not Talking")  # Replace with your folder path
not_talking_frames = load_gif_frames(r"/home/alash-studios/Documents/Python_Scripts/PythonProject/A.S.I.A/Not Talking")  # Replace with your folder path

# Frame rate for GIF
FPS = 20
clock = pygame.time.Clock()

# Animation state
is_talking = False

def pygame_animation():
    global is_talking
    frame_index = 0
    running = True

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GIF Animation")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_talking = not is_talking

        # Select frames based on talking state
        if is_talking:
            current_frames = talking_frames
        else:
            current_frames = not_talking_frames

        # Display the current frame
        screen.fill((255, 255, 255))
        screen.blit(current_frames[frame_index], (0, 0))

        # Update frame index
        frame_index = (frame_index + 1) % len(current_frames)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    # Start the Pygame animation in a separate thread
    pygame_thread = threading.Thread(target=pygame_animation)
    pygame_thread.start()


speak("Hello, boss")


time.sleep(5)



speak("Hello, boss")


time.sleep(5)



speak("Hello, boss")


time.sleep(5)
