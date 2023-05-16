Python interface needs to be installed using the XDA wheel file.
Make sure to have the correct version of python and pip installed on your machine.
Windows wheel files come with the SDK Windows download: MTw Awnida from
https://www.movella.com/support/software-documentation

1. Make sure to have "wheel" installed on your machine:

pip install wheel

2. Install xsensdeviceapi wheel:

Located in 
Windows: <INSTALL_FOLDER>\MTSDK\Python\x64 or Win32
Linux: <INSTALL_FOLDER>/xsens/python

pip install xsensdeviceapi-<xda version>-cp<Python version>-none-<os type>.whl

For example (MTSDK 2021.0.0 wheel for Python 3.9 on Linux):
pip install xsensdeviceapi-2021.0.0-cp39-none-linux_x86_64.whl or

For example (MTSDK 2021.0.0 wheel for Python 3.9 on Windows):
pip install xsensdeviceapi-2021.0.0-cp39-none-win_amd64.whl

------------------------------------------------------------------------------------

In case your Python IDE is unable to find the xsensdeviceapi module or if the
auto-completion does not work, try using:

import xsensdeviceapi.xsensdeviceapi_py<Python version>_64 as xda
instead of:
import xsensdeviceapi as xda

For example for Python 3.9:
import xsensdeviceapi.xsensdeviceapi_py39_64 as xda
