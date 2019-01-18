# Scripts
Scripts from different projects

# Setup
## NileCAM30
Nilecam30_TX2_install script to easily get the camera working. Basicly it extracts the archived software package, then copies the needed parts, and manages all the kernel changes and boot image writing, which is written in the official documentation in 20+ pages.
### How to:
1. Copy or download NileCAM30 compressed archive file to `/home/nvidia/`
2. Start this script as sudo!

# Services for Nvidia Jetson TX2
NOTE : Written for basic "nvidia" user! If you use it elsewhere or with other user, you need to edit the services!
## Jetson .service & .sh
Jetson clocking with the nvidia shellscript. With this service installad, it's automatically starting at boot time.
### How to get it work:
1. Shellscript must be copied to `/home/` than give permissions to read-execute
2. Copy service into `/etc/systemd/system/`
3. Add service to systemcontrol : `systemctl enable jetson_clocks.service`

## Can .service & .sh
Initializing CAN communication interfaces at boot time automatically.
### How to get it work:
1. Shellscript must be copied to `/home/` than give permissions to read-execute
2. Copy service into `/etc/systemd/system/`
3. Add service to systemcontrol : `systemctl enable can_iface_init.service`
