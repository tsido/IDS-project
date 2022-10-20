#!/bin/sh
jupyter nbconvert --to HTML GameCrashPost.ipynb --embed-images --template lab --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags hide_code --output-dir pub
