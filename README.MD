Used to automatically check damage at ER breakpoints. Requires you to already be on the character and have all the settings set up in Genshin Optimizer. The Energy Recharge% minimum final stat filter must be the first filter. Addtionally, due to program limitations, you must close Chrome before running this.

Requirements:
python 3.9
selenium

To install the require python modules, run ```python -m pip install -r requirements.txt```


If the included chromedriver.exe doesn't work, go to https://chromedriver.chromium.org/downloads and download the version corresponding to your chrome version, extract the .exe and put it in the same folder as this file. 

# Command Line arguments

`-er_min` specifies the starting ER. Default: 100

`-er_step` specifies the steps between ER. Default: 5

`-er_max` specifies the maximum ER. Default: 250

`-timeout` changes the timeout. Default: 120

## Example:

`python .\chart_gen.py` is equivalent to `python .\chart_gen.py -er_min 100 -er_step 5 -er_max 250 -timeout 120`