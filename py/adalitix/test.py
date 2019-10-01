from adalitix import Project, Folder, Tiff, File

new_project = Project("Fruitipy")
home_folder = Folder("v1", new_project)

# Creates a new file
example_tiff = Tiff(name="meteo_snap",
                    folder=home_folder)

# connects to an already existing file
# example_file = Tiff(id="0c42aac9-3253-4474-8d56-d25f46fff5ec")

# example_tiff.upload(
#     "../../../../data-backup/meteotn/meteotn_201906210000.tiff")
# # The second upload overwrites the previous one
# example_tiff.upload(
#     "../../../../data-backup/meteotn/meteotn_201906210005.tiff")

example_file = File(name="test", folder=home_folder)
example_file.upload("../../README.md")
example_file.save_to_file("./downloaded.md")
