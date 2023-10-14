#!/bin/bash
while ! curl -s http://selenium-chrome:4444/wd/hub/status &> /dev/null; do
    echo "Wait for selenium server up..."
    sleep 1
done

exec "$@"
