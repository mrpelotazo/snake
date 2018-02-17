Snake Game
==========

A simple, sweet snake game with sound effects. Created by Adrian Antonana
using Python and pygame. Published 01-Aug-2012 on [The Linux Chronicles](
http://thelinuxchronicles.blogspot.com/2012/08/python-snake-game.html) blog.

Instructions
------------

This program requires the [pygame library](http://www.pygame.org/). You may install it like this:
```
python3 -m pip install pygame --user
```

Clone this repository to your local disk using Git, e.g.
```
git clone https://github.com/mrpelotazo/snake.git
cd snake
```

Then run the Snake game from your terminal using Python, e.g.
```
python3 -m game
```

How To Contribute
-----------------

Please, run [Flake8](http://flake8.pycqa.org/) and [Pylint](
http://pylint.readthedocs.io/) before committing changes and opening a PR:
```
$ flake8
$ pylint colors food snake game
```
