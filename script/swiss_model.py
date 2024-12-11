import os
import sys
import time
import json
from tqdm import tqdm
import requests
import logging
import pandas as pd
from typing import List, Tuple, Optional, Union
import hashlib


#########
#
# util function
#
#########

from imp import reload

def log_main(debug:bool = False):

    reload(logging)
    if debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("run.log"),
        ],
    )
    logging.debug(f"Logging level: {logging_level}")

def md5(key: str) -> str:
    """md5.

    Args:
        key (str): string to be hasehd
    Returns:
        Hashed encoding of str
    """
    return hashlib.md5(key.encode()).hexdigest()

#########
#
# swiss-model API
# Ref: https://swissmodel.expasy.org/api-docs/
#
#########

def get_swiss_model_configs():
    # token_str = "a6d3689739f68a77cb1c70646ac01e10c5293648" # A mock, won't work
    token_str = "" # register at swiss-model and Post to api-token-auth API to get the Authorization Token
    return {
        "host": "https://swissmodel.expasy.org/",
        "username": "",
        "password": "", 
        "headers": {
            "Authorization": f"Token  {token_str}",
            "Content-Type": 'application/json',
        },
        "urls": {
            'api-token-auth': 'api-token-auth',
            'automodel': 'automodel',
            'full-details' : '/project/{}/models/full-details/', # project_id
        }
    }

def submit_project(sequence: Union[str, List[str]] = "", *args, **kwargs):
    """
    Submit a project to Swiss-Model and return the project information.

    Args:
        sequence (Union[str, List[str]]): A single protein sequence (str) or a list of sequences (List[str]).
        *args: Optional positional arguments.
        **kwargs: Optional keyword arguments.

    Returns:
        dict or None: A dictionary containing project information or None if the request fails.

    Example:
        # Submit a single protein sequence
        project_info = submit_project("MNPQRK...")
        
        # Submit multiple protein sequences
        sequences = ["MNPQRK...", "ABCDE..."]
        project_info = submit_project(sequences)

    """

    configs = get_swiss_model_configs()

    if isinstance(sequence, str):
        data = {
            "target_sequences": sequence,
            "project_title": f"{md5(sequence + str(time.time))}"
        }
    elif isinstance(sequence, list):
        data = {
            "target_sequences": sequence,
            "project_title": f"{md5(sequence[0] + str(time.time))}"
        }

    url = configs["host"] + configs["urls"]["automodel"]

    project_info = None
    body = _requests_post(url, data, *args, **kwargs)

    if body and body.status_code in [200, 202]:
        project_info = json.loads(body.text)

    return project_info


def get_project_result(project_id: str, *args, **kwargs) -> dict:
    """
    Retrieve the result information for a specified project.

    Args:
        project_id (str): The unique identifier for the project.
        *args: Optional positional arguments.
        **kwargs: Optional keyword arguments.

    Returns:
        dict or None: A dictionary containing the project result information, or None if the request fails.

    Example:
        # Retrieve result information for a specific project
        result_info = get_project_result("123456")

    """
    configs = get_swiss_model_configs()

    url = configs["host"] + configs["urls"]["full-details"].format(project_id)

    project_info = None
    body = _requests_get(url, *args, **kwargs)

    if body.status_code in [200]:
        project_info = json.loads(body.text)

    return project_info



def dump_project_info(path: str, project_info: dict, verbose: bool = False, *args, **kwargs) -> None:
    """
    Save project information to a JSON file at the specified path.

    Args:
        path (str): The path where the JSON file will be saved.
        project_info (dict): A dictionary containing project information.
        verbose (bool): Whether to enable detailed logging (default is False).
        *args: Optional positional arguments.
        **kwargs: Optional keyword arguments.

    Returns:
        str or None: The file path where the project info is saved, or None if project_info is empty.

    Example:
        # Save project info to a JSON file
        dump_project_info("project_info.json", {"project_id": "123456", "status": "completed"}, verbose=True)

    """
    if project_info:
        with open(path, 'w') as f:
            json.dump(project_info, f, ensure_ascii=True, indent=4)

        status = project_info.get("status", "")

        if verbose:
            logging.info(f'Saved project ({project_info["project_id"]}, {status}) info to {path}.')
    else:
        path = None

    return path


def download_model(path: str, project_id: str, model_id: int = 1, verbose: bool = False, *args, **kwargs) -> None:
    """
    Download the model data for a specified project and save it to the given path.

    Args:
        path (str): The file path where the model data will be saved.
        project_id (str): The unique identifier for the project.
        model_id (int): The identifier for the model (default is 1).
        verbose (bool): Whether to enable detailed logging (default is False).
        *args: Optional positional arguments.
        **kwargs: Optional keyword arguments.

    Returns:
        str or None: The file path where the model is saved, or None if the download fails.

    Example:
        # Download model data and save it to a file
        download_model("model_1.pdb", "12345", model_id=1, verbose=True)

    """
    configs = get_swiss_model_configs()

    url = f'{configs["host"]}/project/{project_id}/models/0{model_id}.pdb'

    body = _requests_get(url, verbose, *args, **kwargs)

    if body and body.status_code in [200]:
        with open(path, 'w') as f:
            f.write(body.text)

        if verbose:
            logging.info(f"Saved model {model_id} to {path}.")
    else:
        path = None

    return path

def _requests_post(url: str, data: dict, verbose: bool = False, *args, **kwargs) -> requests.models.Response:
    """
    Send a POST request to the specified URL and return the response object.

    Args:
        url (str): The URL for the POST request.
        data (dict): The data to send in the POST request, provided as a dictionary.
        verbose (bool): Whether to enable detailed logging (default is False).
        *args: Optional positional arguments.
        **kwargs: Optional keyword arguments.

    Returns:
        requests.models.Response: The response object containing the response information.

    Example:
        # Send a POST request
        response = _requests_post("https://example.com/api", {"key": "value"}, verbose=True)

    """
    configs = get_swiss_model_configs()
    body = None
    try:
        body = requests.post(url, json.dumps(data), headers=configs["headers"])
        if verbose:
            logging.info(f"Requests.post: {url}, {data}")

    except requests.exceptions.ConnectionError:
        if verbose:
            logging.info("Connection error.")

    except Exception as e:
        if verbose:
            logging.info(f"Unknown error: {e}")

    return body


def _requests_get(url: str, verbose: bool = False, *args, **kwargs) -> requests.models.Response:
    """
    Send a GET request to the specified URL and return the response object.

    Args:
        url (str): The URL for the GET request.
        verbose (bool): Whether to enable detailed logging (default is False).
        *args: Optional positional arguments.
        **kwargs: Optional keyword arguments.

    Returns:
        requests.models.Response: The response object containing the response information.

    Example:
        # Send a GET request
        response = _requests_get("https://example.com/api", verbose=True)

    """
    configs = get_swiss_model_configs()
    body = None
    try:
        body = requests.get(url, headers=configs["headers"])
        if verbose:
            logging.info(f"Requests.get: (url={url})")

    except requests.exceptions.ConnectionError:
        if verbose:
            logging.info("Connection error.")

    except Exception as e:
        if verbose:
            logging.info(f"Unknown error: {e}")

    return body


def query_enzymes(
    enzymes: pd.DataFrame,
    pdbdir: Optional[str] = None,
    sec_sleep: int = 3,
    *args, **kwargs
):
    """
    Perform homology modeling using Swiss-Model and save the results as PDB files.

    - Use this ONE function for task submission, querying and data downloading
    - Since the completion of multiple predictions for the server is not synchronized, 
        the behavior needs to be determined based on the progress of each work.
    - For a submitted task, the model (pdb) and metadata (json) can be downloaded.
    - And multiple predictions are given. Here the first prediction is downloaded by default.

    Args:
        enzymes (pd.DataFrame): DataFrame containing enzyme information, must include at least "Name" and "Sequence" columns.
        pdbdir (Optional[str]): Directory to save the PDB files (default is the current working directory).
        sec_sleep (int): Time to wait (in seconds) between requests (default is 3 seconds).
        *args: Optional positional arguments.
        **kwargs: Optional keyword arguments.

    Returns:
        None

    Example:
        # Submit the homology modeling works
        query_enzymes(enzymes_df, pdbdir="/path/to/pdb_directory", sec_sleep=5)

        # Query homology modeling results for enzymes and save as PDB files
        query_enzymes(enzymes_df, pdbdir="/path/to/pdb_directory", sec_sleep=5)
    
    """

    assert "Name" in enzymes.columns
    assert "Sequence" in enzymes.columns

    # Use current working directory if no PDB directory is specified
    if pdbdir is None:
        pdbdir = os.getcwd()

    # Add columns for project information and file paths if they don't exist
    for column in ["project_id", "json", "pdb"]:
        if column not in enzymes.columns:
            enzymes[column] = ""

    model_id = 1 # Download the first prediction by default

    # Iterate through the enzymes and perform homology modeling
    for i in tqdm(range(len(enzymes))):
        sequence = enzymes.loc[i, "Sequence"]
        project_id = enzymes.loc[i, "project_id"]
        json_path = enzymes.loc[i, "json"]  # Path to save the full project JSON
        pdb_path = enzymes.loc[i, "pdb"]  # Path to save the PDB file

        # If project_id is missing, submit a new homology modeling request
        if not project_id:
            project_info = submit_project(sequence=sequence, *args, **kwargs)
            time.sleep(sec_sleep)

            if project_info and "project_id" in project_info.keys():
                enzymes.loc[i, "project_id"] = project_info["project_id"]
        else:
            path = json_path if json_path else os.path.join(pdbdir, f"{i}.json")

            # If JSON file does not exist, fetch project information
            if not os.path.exists(path):
                project_info = get_project_result(project_id=project_id, *args, **kwargs)
                time.sleep(sec_sleep)

                # If project contains models, save the JSON file
                if project_info:
                    if "models" in project_info:
                        if project_info["models"]:
                            if len(project_info["models"]):
                                path = dump_project_info(path=path, project_info=project_info, *args, **kwargs)
                                enzymes.loc[i, "json"] = path
            else:
                enzymes.loc[i, "json"] = path

            if enzymes.loc[i, "json"]:
                path = pdb_path if pdb_path else os.path.join(pdbdir, f"{i}.pdb")
                # If PDB file does not exist, download the model
                if not os.path.exists(path):
                    path = download_model(path=path, project_id=project_id, model_id=model_id, *args, **kwargs)
                    time.sleep(sec_sleep)
                    enzymes.loc[i, "pdb"] = path
                else:
                    enzymes.loc[i, "pdb"] = path

