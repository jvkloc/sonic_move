Python interface can be installed using an XDA wheel file:
`pip install xsensdeviceapi-"xda version"-cp"Python version"-none-"os type".whl`

For example
`pip install xsensdeviceapi-2022.0.0-cp39-none-linux_x86_64.whl`
(MTSDK 2022.0.0 wheel for Python 3.9 on Linux)
or
`pip install xsensdeviceapi-2022.0.0-cp39-none-win_amd64.whl`
(MTSDK 2022.0.0 wheel for Python 3.9 on Windows)

------------------------------------------------------------------------------------

In case your Python IDE is unable to find the xsensdeviceapi module or if the
auto-completion does not work, try using
`import xsensdeviceapi.xsensdeviceapi_py<Python version>_64 as xda`
instead of
`import xsensdeviceapi as xda`

Example for Python 3.9:
`import xsensdeviceapi.xsensdeviceapi_py39_64 as xda`
