install_mcedit:
	git clone https://github.com/Podshot/MCEdit-Unified.git
	mv MCEdit-Unified mcedit

generate_example_map:
	python2.7 generateMapTerrain.py \
	    "/Users/leifgehrmann/Library/Application Support/minecraft/saves/Rogaland" \
	    "info/e.txt" \
	    "info/t.txt" \
	    "info/d.txt" \
        "maps/E.59.005.png" \
        "maps/T.59.005.png" \
        -1202 \
        -2402 \
        false
	python2.7 generateMapTerrain.py \
	    "/Users/leifgehrmann/Library/Application Support/minecraft/saves/Rogaland" \
	    "info/e.txt" \
	    "info/t.txt" \
	    "info/d.txt" \
        "maps/E.58.005.png" \
        "maps/T.58.005.png" \
        -1202 \
        0 \
        false
	python2.7 generateMapTerrain.py \
	    "/Users/leifgehrmann/Library/Application Support/minecraft/saves/Rogaland" \
	    "info/e.txt" \
	    "info/t.txt" \
	    "info/d.txt" \
        "maps/E.59.006.png" \
        "maps/T.59.006.png" \
        0 \
        -2402 \
        false
	python2.7 generateMapTerrain.py \
	    "/Users/leifgehrmann/Library/Application Support/minecraft/saves/Rogaland" \
	    "info/e.txt" \
	    "info/t.txt" \
	    "info/d.txt" \
        "maps/E.58.006.png" \
        "maps/T.58.006.png" \
        0 \
        0 \
        false
