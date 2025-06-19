#!/bin/bash

grep Si.castep -e "GA: gen" | awk '{ print $4, $5, $7, $22, $18, $10, $28, $25}' > out.put

