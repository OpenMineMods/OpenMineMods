from CurseAPI import CurseAPI
import curses

motd = """
  _|_|    _|      _|  _|      _|  
_|    _|  _|_|  _|_|  _|_|  _|_|  
_|    _|  _|  _|  _|  _|  _|  _|  
_|    _|  _|      _|  _|      _|  
  _|_|    _|      _|  _|      _|  

        OpenMineMods V1.0
"""

screen = curses.initscr()

screen.border(1)
screen.addstr(0, 0, motd)
screen.refresh()
c = screen.getch()

curse = CurseAPI()

curses.endwin()

print(c)