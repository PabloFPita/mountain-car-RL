# Reinforcement Learning with MountainCar

This repository contains the code and documentation for the project on reinforcement learning using the MountainCar environment from OpenAI Gym.

## Introduction

In this project, I explore the application of reinforcement learning algorithms to solve the MountainCar problem. The goal of the MountainCar problem is to train an agent to drive a car up a steep hill by applying appropriate forces. The agent receives sparse rewards and must learn to navigate the environment through trial and error.

## Installation

To run the code in this repository, you will need to have the following dependencies installed:

- Python 3.11
- OpenAI Gym
- NumPy
- Matplotlib

You can install the required dependencies by running the following command:
pip install -r requirements.txt

## Usage

To train the agent using the Q-learning algorithm, run the following command:
python q_learning.py --train

To test the agent after training, run the following command:
python q_learning.py --test
