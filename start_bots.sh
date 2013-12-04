#!/bin/bash
#
# A simple script to start both the master and slave
#

buildbot start master

sleep 3

buildslave start slave
