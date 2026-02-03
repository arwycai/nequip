# This file is a part of the `nequip` package. Please see LICENSE and README at the root for information on using it.
import torch

from nequip.data import AtomicDataDict

from typing import List, Dict, Optional


class FeatureScalerTransformer(torch.nn.Module):

    def __init__(
        self,
        scaling_dict: Dict[str, str] ,
    ):
        super().__init__()

        self.scaling_dict = scaling_dict

    def forward(self, data: AtomicDataDict.Type) -> AtomicDataDict.Type:
        for field, scale_factor in self.scaling_dict.items():
            old_field = data[field]
            new_field = scale_factor * old_field
            data[field] = new_field

        return data
