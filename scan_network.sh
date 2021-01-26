#!/bin/bash

nmap -sn "10.0.0.*" | grep "MAC Address"
