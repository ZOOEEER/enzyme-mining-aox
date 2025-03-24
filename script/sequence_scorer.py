from typing import Union, List, Dict

def create_mapping(seq: Union[str, List[str]], first_id: int = 1) -> Dict[int, int]:
    """
    Create a mapping from id of a sequence (without "-") to id in alignment (with "-").

    """
    
    mapping = {}
    current_number = first_id  # Initialize the current identifier with the first_id

    for i, char in enumerate(seq):
        if char != "-":
            mapping[current_number] = i  # Assign the current identifier to the position
            current_number += 1  # Increment the current identifier for the next non-dash character

    return mapping


def score_seq(seq:str, score_dict:dict, id2id_align:dict):
    """
    seq_score:
        seq (str): The amino acid sequence
        score_dict (dict):  (resid, resname) -> score.
        id2id_align (dict): original-id -> MSA-id.

    """
    _score = 0
    for resid in score_dict.keys():
        resname = seq[id2id_align[resid]].upper()
        _score += score_dict[resid][resname]
    return _score