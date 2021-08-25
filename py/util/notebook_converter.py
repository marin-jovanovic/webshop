import json

files = ["medium-master/items-recommender/notebooks/recommendation-MT.ipynb"]

for file in files:
    code = json.load(open(file))
    py_file = open(f"{file}.py", "w+")

    for cell in code['cells']:
        if cell['cell_type'] == 'code':
            for line in cell['source']:
                py_file.write(line)
            py_file.write("\n")
        elif cell['cell_type'] == 'markdown':
            py_file.write("\n")
            for line in cell['source']:
                if line and line[0] == "#":
                    py_file.write(line)
            py_file.write("\n")

    py_file.close()