# Slotspy - Simple, Easy Bandit Algorithms

As far as I am aware, there is not a simple python package for running bandit algorithms (from epsilon-greedy to contextual bandits and more!). [Vowpal Wabbit](https://vowpalwabbit.org/) is a powerful, industrial strength package that might solve your problems! To get an idea of how slotspy works, check out the `examples` directory.

Two problems I am trying to solve with slotspy that one encounters when running a bandit algorithm in production are:

 1. Keeping track of actions that have not yet received rewards
 2. Adding/removing arms [slotspy can't help you here yet]


### Disclaimer
I wrote this on a plane and am jetlagged as I am publishing this. I plan to keep working on this project. If you find any issues or want to collaborate, please reach out! (you can find my email in `setup.py`)

This is not yet suitable for production but I hope that changes soon!
