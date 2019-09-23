from adalitix import Project, Revision, Tiff

new_project = Project("Fruitipy")
new_revision = Revision("v1", new_project)

# Creates a new file
example_file = Tiff(name="meteo_snap",
                    revision=new_revision)

# connects to an already existing file
# example_file = Tiff(id="0c42aac9-3253-4474-8d56-d25f46fff5ec")

example_file.upload("../data-backup/meteotn/meteotn_201906210000.tiff")
# The second upload overwrites the previous one
example_file.upload("../data-backup/meteotn/meteotn_201906210005.tiff")
