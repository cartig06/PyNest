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

Update this section to describe your project for milestone 2 and complete the following sections. If your project is
using assets, be sure to keep the citations, sources, and resources section updated.

### Current Progress

Update this section to describe the current progress of your project.

### Challenges

Update this section to describe the challenges for your project at this stage.

### Future Directions

What are your plans for the final submission?



## Final Submission

### Overview

The overview should be at least a paragraph and describe what your project is about.

### Tutorial

The tutorial should at least be 2 paragraphs long and describe how to get started using the program. For example, if it
is a game then you might want to introduce how to start playing and what the basic controls are. If it is a web
application, you might want to indicate how to navigate the application and interact with different components.

### Installation Instructions

Write instructions here for running your program and any files required to do so as appropriate for your programming
language**. For Python projects, this typically means having a `requirements.txt` file that you create using
`pip freeze > requirements.txt`.

### Citation, Sources, and References

Complete this section to include citations for assets and resources that you used for your project. For example, you could
write this section like in the following example:


[UI-Pack Sci-FI from kenney.nl](https://kenney.nl/assets/ui-pack-sci-fi)

[Digital Audio Pack from kenny.nl](https://kenney.nl/assets/digital-audio)

I created by own ASCII art using the [asciiflow web application](https://asciiflow.com/#/ ) and generative AI.


> [!note]
> Any assets and resources you use need to be verifiable that they are licenced for you to use. If you made your
own assets or used generative AI, you must indicate that you did so. Include a link to any assets that you
downloaded and used. 

> [!important]
> Leaving the "Citation, Sources, and References" section unedited will count as not having completed it.
