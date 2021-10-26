#!/bin/bash
sn=Telegram
tmux new-session -s "$sn" -d
tmux split-window -h

tmux select-pane -t 0
tmux send-keys -t 0 C-z 'python3 telegrambot.py' Enter

sleep 5

tmux select-pane -t 1
tmux send-keys -t 1 C-z 'echo "Welcome to Telegram Bot: "' Enter

tmux -2 attach-session -t "$sn"