import requests
import json
from PIL import Image
import numpy as np
from os import remove

BASE_URL = "http://localhost:28000"


def uploadShapefile(zipPath, name, revision):
    files = {'data': open(zipPath, 'rb')}
    values = {'name': name, 'type': "shp", 'revision': revision}

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


class Revision:
    def __init__(self, name=None, project=None, tags=None, id=None):
        if id is None:
            if name is None or project is None:
                raise Exception(
                    "Name and project are required if no id is passed")

            project_id = project.id if isinstance(
                project, Project) else project
            values = {'name': name, 'project': project_id}

            if tags is not None:
                values["tags"] = tags

            r = requests.post(BASE_URL + "/apis/revisions",
                              params=values)

            self.id = r.json()["id"]


class Tiff:
    def __init__(self, id=None, name=None, revision=None):
        if id is None and (name is None or revision is None):
            raise Exception(
                "Name and revision are required if no id is passed")

        self.id = id
        self.cached_content = None
        self.name = name
        self.revision_id = revision.id if isinstance(
            revision, Revision) else revision

    def content(self):
        if self.cached_content is None:
            if self.id is None:
                raise Exception(
                    "Cannot read from a file that has not been created yet")

            url = BASE_URL + "/geoserver/adalitix/ows?service=WCS&version=2.0.0&request=GetCoverage&coverageId=adalitix:" + id
            r = requests.get(url)

            self.cached_content = r.content

        return self.cached_content

    def toNumpyArray(self):
        with open("./temporary.tiff", "wb") as f:
            f.write(self.content())

        im = Image.open("./temporary.tiff")
        arr = np.array(im)

        remove("./temporary.tiff")

        return arr

    def saveToFile(self, path):
        with open(path, "wb") as f:
            f.write(self.content())

    def upload(self, tiffPath):
        if self.id is None:
            files = {'data': open(tiffPath, 'rb')}
            values = {'name': self.name, 'type': "tiff",
                      'revision': self.revision_id}

            # TODO: check that response is successful
            r = requests.post(BASE_URL+"/apis/files",
                              files=files, params=values)
            self.id = r.json()["id"]
        else:
            files = {'data': open(tiffPath, 'rb')}

            # TODO: check that response is successful
            r = requests.post(BASE_URL + "/apis/files/" + self.id, files=files)

        return self
