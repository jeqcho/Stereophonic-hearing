# Stereophonic hearing
This neural network program models how humans or animals determine the direction of the source of a sound using two ears. The sensory information fed into the network is the intensity of sound in each ear and the time delay between each ear. The model is trained using NEAT (NeuroEvolution of Augmenting Topologies).

## Getting Started

Download all the Python files.
You should only run the integrate_lab.py which is the main file of the program. A user should only modify the config.py file.

### Prerequisites

External python modules used are
```
import random
import copy
import pygame
import json
import shelve
```

### Installing

After downloading the files, you can take a look at the config.py file. These can be set by the user to experiment with different variables.

1. Download all Python files.
2. Run integrate_lab.py to check if the program is running smoothly.
3. After training the networks,  a report of statistics and animation of the best network will be played.
4. Press enter to see through the animation.
5. After (default: 6) animations, you will be prompted to save by entering S. Enter S.
6. Stop the program.

Then, you should change some of the variables in config.py. For example,

1. Change the population_limit to 50.
2. Run integrate_lab.py.
3. Review if changes are present during the reports after the network training. The field "Current population" should be 30.
4. Stop the program.

The program comes with a data logging and retrieval system using shelve module.

1. Run integrate_lab.py
2. After training the networks and (default: 6) animations, note that the report shows that this is generation 1.
3. You will be prompted to save by entering S. Enter S.
4. After saving, a new round is started. Stop the program.
5. 3 files with the name (default: network_data) of different extensions should be created.
6. In config.py, set `load_data=True`. Then save and run integrate_lab.py.
7. Confirm the prompt to load data.
8. The first report after training should be titled generation 2.


## Contributing

You can email me at chooijqweb@gmail.com regarding the future of this project.

## Versioning

Currently, this is the first version of the program.

## Authors

* **Chooi Je Qin** - *Initial work* - [Biaural-model](https://github.com/Biaural-model)

See also the list of [contributors](https://github.com/jeqinchooi/jeqinchooi/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This program implements the NEAT algorithm developed by Kenneth O. Stanley and Risto Miikkulainen from the University of Texas.
