#!/bin/sh
set -ex
cd ProBot/ProBot_BeagleBone/encoders
sudo cp bone_eqep0-00A0.dtbo /lib/firmware
sudo cp bone_eqep1-00A0.dtbo /lib/firmware
sudo cp bone_eqep2-00A0.dtbo /lib/firmware
sudo cp bone_eqep2b-00A0.dtbo /lib/firmware
