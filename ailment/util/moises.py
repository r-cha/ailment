import os
from pathlib import Path
from time import sleep
from typing import Self

import requests
import shutil

MOISES_API_TOKEN = os.environ.get("MOISES_API_TOKEN")


class MoisesClient:
    workflow_name: str
    data: bytes
    download_directory: Path
    download_url: str
    job_id: str
    files: list[str]

    def __init__(self, name: str, data: bytes, download_directory: Path):
        self.workflow_name = name
        self.data = data
        self.download_directory = download_directory

    def upload_file(self) -> Self:
        """https://developer.moises.ai/docs/file-upload"""

        # Request a url
        url = "https://developer-api.moises.ai/api/upload"
        headers = {"Authorization": MOISES_API_TOKEN}
        url_response = requests.request("GET", url, headers=headers)

        # Upload the file
        upload_url = url_response.json()["uploadUrl"]
        headers = {"content-type": "multipart/form-data"}
        _ = requests.request("PUT", upload_url, data=self.data, headers=headers)

        # Use it for workflows
        self.download_url = url_response.json()["downloadUrl"]
        return self

    def start_workflow(self) -> Self:
        workflow = "moises/stems-vocals-drums-bass-other"
        # "moises/transcription-beats"

        url = "https://developer-api.moises.ai/api/job"

        payload = {
            "name": self.workflow_name,
            "workflow": workflow,
            "params": {"inputUrl": self.download_url},
        }

        headers = {
            "Authorization": MOISES_API_TOKEN,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, json=payload, headers=headers)

        self.job_id = response.json()["id"]
        return self

    def check_status(self) -> bool:
        url = f"https://developer-api.moises.ai/api/job/{self.job_id}"
        headers = {"Authorization": MOISES_API_TOKEN}
        response = requests.request("GET", url, headers=headers)
        succeeded = response.json()["status"] == "SUCCEEDED"
        if succeeded:
            self.files = [url for url in response.json()["result"].values()]
        return succeeded

    def await_result(self) -> Self:
        while not self.check_status():
            sleep(5)
        return self

    def download_files(self):
        for url in self.files:
            local_filename = url.split("/")[-1]
            download_to = self.download_directory / local_filename
            with requests.get(url, stream=True) as r:
                with download_to.open("wb") as f:
                    shutil.copyfileobj(r.raw, f)
