# start at root of CircuitPython build folders
# 
# ATTENTION!
# Before running this script, 
# press and hold the boot button on the dn_key,
# then while holding the boot button down, 
# press and release the reset button.

# remove any old espressif files to avoid conflicts
rm -rf ~/.espressif

# change over to a temporary directory
mkdir temp
cd temp

# grab the specific release required.
git clone -b v5.1.1 --recursive https://github.com/espressif/esp-idf.git esp-idf-v5.1.1

# jump into that folder
cd esp-idf-v5.1.1

# install esp-idf
./install.sh esp32s3 #,esp32s2  # add or remove other esp chips as needed

# then export to use in the current terminal
. ./export.sh

# change directy back to clone the tinyuf2 folders
cd ../

#grab the tinyuf2 repo
git clone https://github.com/adafruit/tinyuf2.git --recurse-submodules

# change directory into the espressif port in tinyuf2
cd tinyuf2/ports/espressif

# copy over the board files required to build tinyuf2
cp -r ../../../../boards/deepnet_key_s3/ boards/deepnet_key_s3/

# now do all the make steps, clean first, then build. (fullclean is optional but helpful)
make BOARD=deepnet_key_s3 fullclean
make BOARD=deepnet_key_s3 all
make BOARD=deepnet_key_s3 flash

echo "
Press reset on the DN_Key to start up with the newly flashed bootloader
then run this command:
cp ../../../../../dn_key_s3_circuitpython_20240803.uf2 /Volumes/DN_BOOT
"

echo "** FINISHED!! **"
