#!/bin/bash
tmux kill-session -t bot
tmux new -s bot -d 
tmux send-keys -t bot "source ./venv/bin/activate" C-m
tmux send-keys -t bot "python BraincellBot.py" C-m
