About
======
<!-- TOC -->

- [Preview:](#preview)
    - [User input](#user-input)
    - [Four operational quadrants](#four-operational-quadrants)
- [Running the code](#running-the-code)
    - [Python setup](#python-setup)

<!-- /TOC -->

This is a simplistic tool for viewing the space vector diagrams of an induction machine in different __static__ operational modes. Unlike in a regular textbook diagram, the modes can be continuously changed by the viewer. This might help build a better intuition of the relationship between different values.

The value relationships are calculated using a conventional transformer equivalent circuit of the asynchronous machine.

A full description of the tool and the background equations can be found in:
[M. Stunda, "A Space Vector Based Tool for the Visualisation of Induction Machine Operation Modes," _2019 IEEE 60th International Scientific Conference on Power and Electrical Engineering of Riga Technical University (RTUCON)_, Riga, Latvia, 2019, pp. 1-5.][link.ieee]

It should be noted that the animated movement doesn't represent transient dynamics as the transient components are eliminated from the model for lightweight operation.

## Preview:

### User input
The user has access to two sliders:
- The (internally regulated) quadrature component of the stator current
- The (externally enforced) actual rotor speed.

The output vector diagram and operational quadrant diagram only represent steady state operation in the base speed range.

### Four operational quadrants
This is a recording of cycling through all four quadrants using the two sliders.

The slip frequency is displayed as a vector on the right side to simbolyze the direction of the slip.

![Full range operation preview][gif.complete]



## Running the code
The graphical interface is built using _Python 3.7_ and the _TkInter_ library.

### Python setup
For a quick and easy isolated _Python 3.x_ setup the [_Miniconda_][link.conda] installer (not full _Anaconda_) and the [_Spyder_][link.spyder] IDE can be recommended. 
After installing miniconda _Spyder_ can be installed through the [_Anaconda Prompt_][link.prompt] by running: 
```
conda install spyder
```

If not yet installed, the following Python packages will be required: 
* _math_ for calculating the rotating Hexagon 
* _tk_ for building the GUI.






[link.ieee]:https://ieeexplore.ieee.org/document/8982320
[gif.complete]:images/Complete_movement.gif
[link.conda]: https://docs.conda.io/en/latest/miniconda.html
[link.spyder]: https://www.spyder-ide.org/
[link.prompt]: https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf

