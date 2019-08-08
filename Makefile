install_mcedit:
	git clone https://github.com/Podshot/MCEdit-Unified.git
	mv MCEdit-Unified mcedit
	echo 'from .pymclevel import *' >> mcedit/__init__.py

generate_example_map:
	python2.7 generateMapTerrain.py
