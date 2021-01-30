# Dual-Mag-Data
![version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![license](https://img.shields.io/badge/license-MIT-blue.svg) 

Dual-Mag-Data is a python library created to convert raw image and log data from the Dual-Mag camera into processed color images and csv files with collated image and system status data. The library currently implements the following minimal set of features:

1. color conversion and contrast enahncement of images
2. Collation of system status and ROI detector data in csv file
3. Creation of javascript files to load from [Dual-Mag-Dash](https://github.com/guatek/Dual-Mag-Dash)

Additional features as described in the "Where help is needed" section.

## Requirements

- python3 and several python modules (listed bellow)
- Data generated from a Guatek Dual-Mag plankton camera (2020 versino and up)

## Highly Recommended

- [VS Code](https://code.visualstudio.com/)
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Powershell](https://github.com/PowerShell/PowerShell) for use on Windows

## Quick Start (Windows)

1. Install Powershell
   1. Download from this link: [PowerShell-7.0.3-win-x64.msi](https://github.com/PowerShell/PowerShell/releases/download/v7.0.3/PowerShell-7.0.3-win-x64.msi)
   2. Follow setup instructions from MSI Package here: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-windows?view=powershell-7.1
2. Install Miniconda 3.8 Windows 64-bit
   1. Download from this link: https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
   2. Follow installations instructions installing into accepting defaults when prompted. Install into user’s home directory
   3. In the windows search bar (Type here to search) type in Anaconda Prompt (miniconda3)and click on the icon to open an anaconda shell
   4. At the shell type conda init powershell to setup PowerShell to use the miniconda installation
3. Test Miniconda and Powershell
   1. Type: powershell into the windows search bar and click on the PowerShell 7 (x64) icon
   2. If setup correctly after a few seconds you should see a prompt that looks like: (base) PS C:\Users\[username]> where [username] is your username
   3. Type python into the prompt to start python and record version
4. Setup Dual-Mag Virtual Environment
   1. Type exit() at the python prompt to exit back to powershell
   2. Create the dual-mag virtual environment and activate it
      1. PS C:\Users\[username]> conda create -n dual-mag python=3.9.1 
      2. PS C:\Users\[username]> conda activate dual-mag
   3. Install required python modules into the new virtual environment
      1. (dual-mag) PS C:\Users\[username]> pip install pystache
      2. (dual-mag) PS C:\Users\[username]> pip install loguru
      3. (dual-mag) PS C:\Users\[username]> pip install scikit-image
      4. (dual-mag) PS C:\Users\[username]> pip install opencv-python
      5. (dual-mag) PS C:\Users\[username]> pip install psutil
      6. (dual-mag) PS C:\Users\[username]> pip install pandas
      7. (dual-mag) PS C:\Users\[username]> pip install parse
5. Download Dual-Mag-Data Repo
   1. Download software from: https://github.com/guatek/Dual-Mag-Data/archive/master.zip
   2. Extract to a convenient location, for example: C:\Users\[username]\software

## Reporting Issues
We use GitHub Issues as the official bug tracker

## Technical Support or Questions

If you need support beyond github please use our [Contact Page](http://www.guatek.com/contact/) or reach out to us directly via email or slack.

## Licensing

- Copyright 2021 Guatek (http://www.guatek.com)
- Licensed under MIT (https://github.com/guatek/Dual-Mag-Data/blob/master/LICENSE.md)

