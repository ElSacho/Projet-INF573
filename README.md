**SquidinfGame**

1. **Codes**

The project we are presenting is a video game platform. On our game "SquidinfGame" you can play scary games that are derivatives of the Squid Game series. Each game uses computer vision to answer a different challenge. Of the 5 games we coded, one reimplements a "from scrach" image segmentation algorithm found in the openCV library, and the other four use computer vision from the webcam image. We have both reimplemented other methods (such as object detection and tracking in game 3), and reused existing modules to integrate them into our games and couple them with other methods. We have built a real graphical and sound interface for our game, with a menu that also uses the openCV library to detect the game the user wants to launch. At any time, the player can press "m" to return to the main menu, "r" to restart the game, or "q" to quit the game. 

2. **To launch the game**

**Changing the path to a file**

- In the document "biscuit/biscuit.py" you need to change the path of the "haarcascade_frontalface_default.xml" to the one of your device (usally, the path is in a "data" folder in the opencv librairie)

**Launch the game**

- Then, you just have to run the main function and that's it ! 
- Press "space" to skip the intro
- Press "q" to quit at any time
- Press "m" to return to the menu when your are in a game
- Press "r" to restart the game you are playing

Enjoy our game ! 

3. **To test the random walker**

We suggest that you use the file "rw/random_walk.py" instead of the game as you will have more liberty.

- You can choose the picture you want in the last line of the code.
- Then, you need to specify the number of labels you want (no more than 3 because of the colors difference)
- You can labelise the data clicking on the image. 
- To go from one label to another, you need to press "space". Sometime it doesn't work, so look at the terminal that specify if it could labelise an another data
- Press space once you labelised all your data