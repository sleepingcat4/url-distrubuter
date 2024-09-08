from fastapi import FastAPI, HTTPException
from typing import List
import os

app = FastAPI()

FOLDER_PATH = r"E:\Computer Science\URL retriver\dump_url"
DUMP_FILE = os.path.join(FOLDER_PATH, "dump.txt")


def read_urls_from_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


def read_urls_from_folder() -> List[str]:
    all_urls = []
    for file_name in os.listdir(FOLDER_PATH):
        file_path = os.path.join(FOLDER_PATH, file_name)
        if file_name == "dump.txt" or not file_name.endswith(".txt"):
            continue
        urls = read_urls_from_file(file_path)
        all_urls.extend(urls)
    return all_urls


def read_dumped_urls() -> List[str]:
    if not os.path.exists(DUMP_FILE):
        return []
    return read_urls_from_file(DUMP_FILE)


def write_to_dump(urls: List[str]):
    with open(DUMP_FILE, "a") as dump_file:
        for url in urls:
            dump_file.write(url + "\n")


def remove_served_urls(all_urls: List[str], served_urls: List[str]) -> List[str]:
    return [url for url in all_urls if url not in served_urls]


@app.get("/get-urls/")
def get_urls(count: int):
    all_urls = read_urls_from_folder()
    served_urls = read_dumped_urls()
    available_urls = remove_served_urls(all_urls, served_urls)
    
    if count > len(available_urls):
        raise HTTPException(status_code=400, detail="Requested more URLs than available.")

    urls_to_serve = available_urls[:count]
    write_to_dump(urls_to_serve)

    return {"urls": urls_to_serve}
