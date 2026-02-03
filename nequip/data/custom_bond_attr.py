from typing import Dict

def dict_to_edge_attr(
        bond_dict: Dict[str, any],
        key: str
) -> Dict[str,any]:
    key_mapping = {
        'edge_density':'density',
        'edge_softness': 'softness',
        'edge_ellipticity':'ellipticity',
        'end_atoms':'end_atoms',
    }

    included_keys = ['end_atoms'] + [key]

    edge_attr_dict = {k: {y: bond_dict[k][key_mapping[y]] for y in included_keys} for k in bond_dict}
    
    return edge_attr_dict
    
