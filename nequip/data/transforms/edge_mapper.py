import torch
from nequip.data import AtomicDataDict

class EdgeMappingTransformer(torch.nn.Module):
    """
    map edge custom key

    args: custom_key_name
    """

    def __init__(
        self,
        key_name: str
    ):
        super().__init__()

        key_mapping_bond = {
        'edge_density': AtomicDataDict.EDGE_DENSITY_KEY,
        'edge_ellipticity': AtomicDataDict.EDGE_ELLIPTICITY_KEY,
        'edge_softness': AtomicDataDict.EDGE_SOFTNESS_KEY
    }
        self.key_name = key_mapping_bond[key_name]

    def forward(self, data: AtomicDataDict.Type) -> AtomicDataDict.Type:
        attr_list=[]
        for i in range(data[AtomicDataDict.EDGE_INDEX_KEY].shape[1]):
            end_atoms = data[AtomicDataDict.EDGE_INDEX_KEY][:,i]
            for key, value in data[self.key_name].items():
                if set(value['end_atoms'])==set(end_atoms.tolist()):
                    attr_list.append(float(value[self.key_name]))
            try:
                test = attr_list[i]
            except:
                attr_list.append(0)

        data[self.key_name] = torch.tensor(attr_list).contiguous()
        
        return data
