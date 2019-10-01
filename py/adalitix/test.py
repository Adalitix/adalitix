from adalitix import Project, Folder, Tiff, File

new_project = Project("Fruitipy")
home_folder = Folder("v1", new_project)

# Creates a new file
example_tiff = Tiff(name="meteo_snap",
                    folder=home_folder)

# connects to an already existing file
# example_file = Tiff(id="0c42aac9-3253-4474-8d56-d25f46fff5ec")

example_tiff.upload(
    "/home/user/Code/_ADALITIX/data-backup/meteotn/meteotn_201906210000.tiff")
example_tiff.save_to_file("./downloaded.tiff")

# example_file = File(name="test", folder=home_folder)
# example_file.upload("../../README.md")
# example_file.upload("../README.md")
# example_file.save_to_file("./downloaded.md")
