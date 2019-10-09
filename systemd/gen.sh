#! /bin/sh

cat <<EOF > firev2.service
[Unit]
Description=FireV2 Service
After=network.target
Wants=network.target

[Service]
Type=simple
Environment=V2RAY_LOCATION_ASSET=/etc/v2ray
ExecStart=/usr/bin/v2ray -config $PWD/../nodes/using.json
Restart=on-failure
RestartPreventExitStatus=23

[Install]
WantedBy=multi-user.target
EOF
