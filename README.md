# Project - PyNest

This repository is for the semester project. For each milestone, you should update the corresponding
section with information about your project status. Do not complete README sections for future milestones or
the final submission when we still have not gotten to an earlier milestone. This is likely to cause
confusion for peer code reviewers. Doing so may result in the loss of points, up to and including
an award of 0 points as determined by the instructor.

## Milestone 1

As of milestone 1, PyNest is still intended to be a TUI (via Textual) based Python IDE 
with integrated text editor, project explorer, file tabs, terminal window, output window, git 
integration, and easy navigation via intuitive keybinds and shortcuts. Future updates will allow users to select themes
and color profiles along with customizing shortcuts to their liking.

### Current Progress

As of now, the first release of the text editor portion is complete. I have written the beginnings of a backend (service) for the
project functionality, and plan to implement it on my next release. I have a functional text selection system and clipboard,
with the only change required being a new shortcut. The first implementation of an auto-indent feature is complete as well,
however it is very basic and only indents if the line before it ends with ":", and copies the indentation of the line before it as well.

### Challenges

The biggest issues I had while writing this program up to this point came almost entirely when adding functionality for indentation.
It was very unexpected, as I had expected this to be quick and easy, however ended up requiring multiple hours of research and writing
helper functions to get everything working. As it turned out, implementing tab expansion to make the interface more user-friendly
threw off alignment when moving the cursor vertically, so I had to implement an entirely different way of calculating positions to account for tabs;
resulting in the logical cursor position (where the cursor actually is at in the file), and the visual cursor position (where the user sees the cursor).
This crowded my EditorService quite a bit, however not to the extent of requiring a complete refactor.

My only persisting issues stem from keybinds being "eaten" by the terminal window. Due to the program being based around a TUI,
key inputs are often lost to being already owned by the terminal and performing terminal actions. This limits my available
keybinds quite significantly, however I am sure I will be able to figure out a working bind map that is still intuitive. Either this,
or I will have to find a workaround for forcing the binds through.

### Future Directions

For the next milestone, I plan on implementing all features I have planned for the editor such as automatically
adding closing characters (auto-parenthesis, auto-quotes, etc.), undo, redo, and navigation by words. I also plan to have
a functional tab system and explorer completed, with hopes of having a working terminal window as well. Essentially, almost
everything should be completed besides git integration and implementation of the project system.



## Milestone 2

Milestone 2 has not seen any major design-altering changes since milestone 1, however many features have been implented.
As there were many bugs in the milestone 1 release, I had a lot of fixes and patches to do, however the application seems to
run very well at this time.


### Current Progress

As of milestone 2, PyNest's editor features have grown significantly. For instance, auto-closing characters, scrolling, 
selection highlighting, and many bug fixes have been fully implemented. A togglable help menu is also partially implemented,
however I ran out of time while writing it. Once the editor portion is fully implemented, due to the modular design of the
application, multiple tabs and a file explorer will be relatively straightforward. The application is coming along nicely
and I am excited to continue working on it.

### Challenges

The biggest challenge I faced while working on this milestone stemmed from selection highlighting. More specifically,
the visual alignment of the highlights to the actual cursor position due to tabs. I am still fighting keybinds, however hope
to figure out another solution by the final release. If i cannot, I will have to use unconventional shortcuts, which the user
could still adapt to with use of the application. For the time being, to view keybinds and what key does what, please view instructions.txt

### Future Directions

The final submission will effectively be buttoning up the keybinds, implementing a tab system for multiple editors, a project explorer,
git integration, finishing the help menu, and adding a terminal/stdout widget as well. Essentially, the final update will be 
directed toward turning this from a text editor into a full ide. With my recent independent research in mind, I am considering integrating
a small LLM for tab completion.



## Final Submission

### Overview

PyNest is a terminal-based, keyboard-first Python IDE written in Python.
It features a built-in text editor, file explorer, and project management system. 
While I had planned to have a working interactive terminal emulator completed for this build,
I was unable to do so in the allotted time. Still, I am happy with the program's current state as it is comfortable and
intuitive to use without being too complex and even used it to write some of itself.
With such a short timeframe, I am disappointed I was unable to get all the major components finished, but
I am excited to continue development even after this class comes to an end.

### Tutorial

To get started with PyNest, a user should install all dependencies using the *requirements.txt* file. They should then
create a virtual environment via *python3 -m venv .venv* in the project root directory. They should then enter the 
virtual environment by running *source .venv/bin/activate* and, finally, run *src/main.py*  
Once running, a user is greeted with a welcome screen asking them whether they'd like to create a new project, or open an existing one.
You'd likely want to create a new project. They will then be brought to a new screen that asks for a projects folder and a name.
If the default location works for you, leave it as that. Tab down to the create button (or click, most of PyNest works via mouse
as well). Finally, you are brought to the project screen! View the help menu on the bottom for any further assistance!

### Installation Instructions

Step 1: Run *pip install -r requirements.txt* in your terminal  
Step 2: View *instructions.txt* for further step instructions to get this prototype up and running on your machine.

### Citation, Sources, and References

I created ascii art for the logo in this project and most of the styling elemnents were done in CSS via my own knowledge
and generative AI. I did not download any assets for this project, only used the libraries listed in *requirements.txt*


> [!note]
> Any assets and resources you use need to be verifiable that they are licenced for you to use. If you made your
own assets or used generative AI, you must indicate that you did so. Include a link to any assets that you
downloaded and used. 

> [!important]
> Leaving the "Citation, Sources, and References" section unedited will count as not having completed it.
