Used to automatically check damage at ER breakpoints. Requires you to already be on the character and have all the settings set up in Genshin Optimizer. The Energy Recharge% minimum final stat filter must be the first filter. Addtionally, due to program limitations, you must close Chrome before running this.

# Requirements/Set up:
* python 3.9
* selenium

To install the require python modules, run ```python -m pip install -r requirements.txt```

Tested only on python 3.9. The code might run on python 3.7 or 3.8, but the developer doesn't know, and does not currently guarantee compatibility.

If the included chromedriver.exe doesn't work, go to https://chromedriver.chromium.org/downloads and download the version corresponding to your chrome version, extract the .exe and put it in the same folder as this file. 

[Youtube video for a video guide on the set up process](https://youtu.be/RUVZUyHQgcc)

# Command Line arguments

`-er_min` specifies the starting ER. Default: 100

`-er_step` specifies the steps between ER. Default: 5

`-er_max` specifies the maximum ER. Default: 250

`-timeout` changes the timeout. Default: 20

## Example:

`python .\chart_gen.py` is equivalent to `python .\chart_gen.py -er_min 100 -er_step 5 -er_max 250 -timeout 20`

# Recommended Build Settings:

* Generate 1 build only (option is next to the generate button)

* Choose only the relevant Goblets (The corresponding EleDMG%, maybe atk% goblets if you have good ones)

* Choose only CR/CDMG Circlets, ATK/ER/EM Sands

* For EoSF using characters, do all sets for lower ER (use the CLI to limit the scraping to 100 ER -> 150 ER, for example), then force EoSF 2 set/4 set for the higher ER (use CLI to do the remaining 150 ER -> 250 ER)

* For 4BS using characters, just force 4BS. That set is too broken.

* For characters that use both 4BS and 4EoSF, just run no set assumption until GO gives us an OR option for artifact sets

* Reminder that character level 90 and enemy level 90 are the assumed levels