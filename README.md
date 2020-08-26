# py4e-Project-Coursera-

This is a simple project to complement the Python for Everybody course offered on Coursera. I decided to also share it on Github as a means of starting to use this platform as well.

My experience with programming is very limited. I am not a Software Developer or Engineer. I am a Mechanical Engineer with a great interest in programming.

That said, this project is not too complicated. I intend to keep adding features as I gain more knowledge in different programming languages and software.
* * *

## What does it do?

As a big astronomy fan, I had to use my newly acquired skills to do something with stars and planets. And so this monstrosity was born.
The various files in this project allow for one to create a local database of the stars catalogued in the *Henry Draper Catalogue* and do some statistical analysis of their magnitude, position, analysis of constellations and other stuff I come up with.

## How it works?

The data is gathered from *Wikisky*'s API, (that can be found [here](http://server7.wikisky.org/XML_API_V1.0.html)) and stored in a "preliminary" local database with only the XML and respective URL. This data is then cleaned and parsed onto a new local database with the star's ID in the *Henry Draper* Catalogue, its respective right ascension, declination, magnitude and constellation. This data is then used for various statistical analysis. 

To succesfully run the project, the following steps have to be done in order:

1. Run *getstar.py* to create a local database of the information gathered from the API stated above.
2. Run *starinfo.py* to clean the data and organize the information gathered.
3. Run the various Python files to get the intended analysis (***Not yet implemented***)


* * *
***Please Note:*** 
* Because it gathers data from the Web, an Internet connection is needed. Note that it might get costly if you do not have unlimited broadband! I accept no responsibility for any additional expense associated with this project.
* Unfortunately, Wikisky does not have information on every star listed in the catalogue, and this is an issue I only ran into after commiting some hours into the project, so I decided to run with it as is. In the future, I may try to add the missing information from a different data source.
* The project is not complete! I have not yet implemented all the funcionalities I intend this to have.
