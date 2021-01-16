import os
this_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

os.chdir(this_dir)
exec(open("./rest_mediator/dataset_resource.py").read())