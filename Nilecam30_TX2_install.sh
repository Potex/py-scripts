#Nilecam30 - Jetson TX2 install script
#How to use:
#Step 1 : Copy or download nilecam compressed archive file to /home/nvidia/
#Step 2 : start this script as sudo!

mkdir top_dir/ -p
export TOP_DIR=/home/nvidia/top_dir/
export RELEASE_PACK_DIR=/home/nvidia/top_dir/NileCAM30_TX2_JETSON_TX2_L4T28.2.1_08-AUG-2018_R01
cp NileCAM30_TX2_JETSON_TX2_L4T28.2.1_08-AUG-2018_R01.tar.gz $TOP_DIR/
cd $TOP_DIR
tar -xaf NileCAM30_TX2_JETSON_TX2_L4T28.2.1_08-AUG-2018_R01.tar.gz
sudo cp $RELEASE_PACK_DIR/Kernel/Binaries/Image /boot/Image -f
sudo tar xjpmf $RELEASE_PACK_DIR/Kernel/Binaries/kernel_supplements.tar.bz2 -C /
sudo cp $RELEASE_PACK_DIR/Rootfs/modules /etc/modules -f
sudo cp $RELEASE_PACK_DIR/Rootfs/xorg.conf /etc/X11/xorg.conf -f
sudo dd if=$RELEASE_PACK_DIR/Kernel/Binaries/tegra186-quill-p3310-1000-c03-00-base_sigheader.dtb.encrypt of=/dev/mmcblk0p26 bs=1M
cd ..
rm NileCAM30_TX2_JETSON_TX2_L4T28.2.1_08-AUG-2018_R01.tar.gz
sudo reboot
