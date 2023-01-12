from asciimatics.effects import Cycle, Stars, BannerText, Print
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from time import sleep

def loading(screen):
		effects = [
			Stars(screen, 200),
			Cycle(
				screen,
				FigletText("YATAGE", font='big'),
				int(screen.height / 2 - 8)),
			Print(
				screen,
				FigletText("Yet Another Text Adventure Game Engine.", font='small'),
				int(screen.height / 2 )),
			BannerText(
				screen,
				FigletText("Press 'q' to continue", font='small'),
				int(screen.height / 2 + 8),
				4),
		]
		screen.play([Scene(effects,0)])

# Screen.wrapper(intro)