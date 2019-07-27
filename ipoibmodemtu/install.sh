#!/bin/bash
set -x
cp ipoibmodemtu /usr/bin/ipoibmodemtu
cp ipoibmodemtu.conf /etc/ipoibmodemtu.conf
cp ipoibmodemtu.service /usr/lib/systemd/system/ipoibmodemtu.service
systemctl daemon-reload
systemctl enable ipoibmodemtu.service
