#!/bin/bash

for i in $(seq 1 254); do
  (ping -c 1 192.168.0.$i | grep "bytes from" | awk -F: '{print $1}' | awk '{print $4}' &) 
done
