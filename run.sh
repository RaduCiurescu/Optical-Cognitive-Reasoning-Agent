#!/bin/bash

# Activeaza virtual environment
source venv/bin/activate

while true; do
    echo "Pornesc detection_module.py..."
    sudo python3 detection_module.py
    
    echo "Detection module terminat, pornesc main_app.py..."
    python3 main_app.py
    
    echo "Main app terminat, repornesc ciclul..."
    sleep 1
done