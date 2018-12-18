#!/bin/bash
sudo modprobe can
sudo modprobe can_raw
sudo modprobe can_dev
sudo modprobe mttcan
sudo ip link set can0 type can bitrate 500000
sudo ip link set can1 type can bitrate 500000
sudo ip link set up can0
sudo ip link set up can1
ifconfig can0 txqueuelen 2000
ifconfig can1 txqueuelen 2000
