:: Generate a new Windows liveusb-creator release
:: Usage: `release 3.0.1`
:: Author: Luke Macken <lmacken@redhat.com>
echo Generating an exe of the liveusb-creator %1
del /Q dist
del /Q build
C:\Python27\python.exe -OO setup.py py2exe
copy *.dll dist
copy boot.7z dist
copy README.txt dist
copy data\blackpantherusb.ico dist\liveusb-creator.ico
copy data\liveusb-creator.nsi dist\liveusb-creator.nsi
rename dist blackPanther_USBMaker-%1
