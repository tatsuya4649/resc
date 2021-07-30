#!/bin/bash

lsof -i:55555 | sed -n '2,$p' | cut -d' '  -f2 | while read line; do kill "$line"; done
