# WorldGeneration
Code accompanying the paper ["Bringing Stories Alive: Generating Interactive Fiction Worlds"](http://arxiv.org/abs/2001.10161).

Neural PCG model (including AskBERT) is found in ```neural-based```, Rule-based PCG model is found in ```rule-based```, Evennia game generation framework is found in ```evennia-engine```.

Each folder has its own README, follow the instructions in ```rule-based``` and ```neural-based``` to generate a ```*.dot``` file that can then be passed in the Evennia framework to create a playable game.

# Dataset

The data used for finetuning fairytale and mystery models can be collected through ```/neural-based/scrape-wikipedia```

BibTex
```
@article{ammanabrolu20world,
  title={Bringing Stories Alive: Generating Interactive Fiction Worlds},
  author={Ammanabrolu, Prithviraj and Cheung, Wesley and Tu, Dan and Broniec, William and Riedl, Mark O.},
  journal={CoRR},
  year={2020},
  url={http://arxiv.org/abs/2001.10161},
  volume={abs/2001.10161}
}
```
