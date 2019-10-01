import requests
import json
from PIL import Image
import numpy as np
from os import remove

BASE_URL = "http://localhost:28000"


def uploadShapefile(zipPath, name, folder):
    files = {'data': open(zipPath, 'rb')}
    values = {'name': name, 'type': "shp", 'folder': folder}

    r = requests.post(BASE_URL+"/apis/files",
                      files=files, params=values)
    # TODO: check that response is successful

    return r.json()


def addLayer(configPath):
    with open(configPath, 'r') as f:
        headers = {'content-type': 'application/json'}
        r = requests.post(BASE_URL + "/apis/layers",
                          data=f.read(), headers=headers)
        return r.text


class Project:
    def __init__(self, name=None, id=None):
        if id is None:
            if name is None:
                raise Exception("Name is required if no id is passed")

            r = requests.post(BASE_URL + "/apis/projects",
                              params={'name': name})

            self.id = r.json()["id"]
        else:
            self.id = id


class Folder:
    def __init__(self, name=None, project=None, parent=None, id=None):
        if id is None:
            if name is None or project is None:
                raise Exception(
                    "Name and project are required if no id is passed")

            project_id = project.id if isinstance(
                project, Project) else project
            values = {'name': name, 'project': project_id}

            if parent is not None:
                values["parent"] = parent.id if isinstance(
                    parent, Folder) else parent

            r = requests.post(BASE_URL + "/apis/folders",
                              params=values)

            self.id = r.json()["id"]


class Tiff:
    def __init__(self, id=None, name=None, folder=None):
        if id is None and (name is None or folder is None):
            raise Exception(
                "Name and folder are required if no id is passed")

        self.id = id
        self.cached_content = None
        self.name = name
        self.folder_id = folder.id if isinstance(
            folder, Folder) else folder

    def content(self):
        if self.cached_content is None:
            if self.id is None:
                raise Exception(
                    "Cannot read from a file that has not been created yet")

            r = requests.get(BASE_URL + "/apis/files/" + self.id)

            self.cached_content = r.content

        return self.cached_content

    def toNumpyArray(self):
        with open("./temporary.tiff", "wb") as f:
            f.write(self.content())

        im = Image.open("./temporary.tiff")
        arr = np.array(im)

        remove("./temporary.tiff")

        return arr

    def save_to_file(self, path):
        with open(path, "wb") as f:
            f.write(self.content())

    def upload(self, tiffPath):
        if self.id is None:
            files = {'data': open(tiffPath, 'rb')}
            values = {'name': self.name, 'type': "tiff",
                      'folder': self.folder_id}

            # TODO: check that response is successful
            r = requests.post(BASE_URL+"/apis/files",
                              files=files, params=values)
            self.id = r.json()["id"]
        else:
            files = {'data': open(tiffPath, 'rb')}

            # TODO: check that response is successful
            r = requests.post(BASE_URL + "/apis/files/" + self.id, files=files)

        return self


class File:
    def __init__(self, id=None, name=None, folder=None):
        if id is None and (name is None or folder is None):
            raise Exception(
                "Name and folder are required if no id is passed")

        self.id = id
        self.cached_content = None
        self.name = name
        self.folder_id = folder.id if isinstance(
            folder, Folder) else folder

    def content(self):
        if self.cached_content is None:
            if self.id is None:
                raise Exception(
                    "Cannot read from a file that has not been created yet")

            r = requests.get(BASE_URL + "/apis/files/" + self.id)

            self.cached_content = r.content

        return self.cached_content

    def save_to_file(self, path):
        with open(path, "wb") as f:
            f.write(self.content())

    def upload(self, filePath):
        if self.id is None:
            files = {'data': open(filePath, 'rb')}
            values = {'name': self.name, 'type': "other",
                      'folder': self.folder_id}

            # TODO: check that response is successful
            r = requests.post(BASE_URL+"/apis/files",
                              files=files, params=values)
            self.id = r.json()["id"]
        else:
            files = {'data': open(filePath, 'rb')}

            # TODO: check that response is successful
            r = requests.post(BASE_URL + "/apis/files/" + self.id, files=files)

        return self
