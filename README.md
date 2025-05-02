# Slide Game

A Python implementation of a single-player game called **Slide**, developed as part of the CSCA08H course at the University of Toronto Scarborough.

## 📜 Description

This is a text-based board game where players slide colored squares across a 2D grid to form matching sequences. The main game logic is divided between two files:

- `slide_functions.py`: Contains core logic and utility functions for manipulating the game board.
- `slide_game.py`: Contains the main game loop, user interaction, and game mechanics.

## 🧩 Features

- Board representation using a string-based grid
- Sliding mechanics for rows (left and right)
- Win condition checks for connected squares
- Input validation and error handling
- Constants for easy modification of board dimensions and gameplay rules

## 🗂️ File Overview

| File              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `slide_game.py`   | The main script for running the Slide game. Handles user inputs and game flow. |
| `slide_functions.py` | Contains helper functions to manage the game board, including sliding mechanics and board queries. |

## 🕹️ How to Play

1. Run `slide_game.py` in a Python environment.
2. Input the color of the square you want to slide.
3. Choose the direction (left or right).
4. Select the row where you'd like to make your move.
5. Try to connect 3 or more same-colored squares to win.
