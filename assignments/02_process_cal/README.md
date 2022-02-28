# Assignment 2 (A#2)

## Updating provided files

To get the latest version of the provided files for A#2 without replacing the content that might be already present in your process_cal2.py, you can use the following commands:

In any folder outside your a2 folder in your local repository (to avoid replacing potential existing work in process_cal2.py):

    scp NETLINKID@seng265.seng.uvic.ca:/seng265work/2022-spring/a2/* .

    cp *.xml ~/NETLINKID/a2

    cp *.yaml ~/NETLINKID/a2

    cp *.md ~/NETLINKID/a2

The commands above assume you have cloned your repository in the home folder and that you're executing them inside Senjhalla. An analogous process (by replacing the paths) can be followed by students with M1 Macbooks.

## Installing additional modules for tester.py

To use tester.py inside Senjhalla  or in the analogous environment for M1 MacBoocks, you need to execute the following command

    pip3 install deepdiff --no-warn-script-location
    
