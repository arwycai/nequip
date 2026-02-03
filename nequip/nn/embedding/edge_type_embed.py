# This file is a part of the `nequip` package. Please see LICENSE and README at the root for information on using it.
import torch
import torch.nn.functional

from e3nn.o3._irreps import Irreps

from nequip.data import AtomicDataDict
from nequip.data._key_registry import _GRAPH_FIELDS
from .._graph_mixin import GraphModuleMixin
from ..utils import with_edge_vectors_, with_edge_type_
from typing import Optional, Final, List, Dict


_CATEGORICAL_FIELD_EMBED_KEYS: Final[List[str]] = [
    "field",
    "num_features",
    "min",
    "max",
]


class EdgeTypeEmbed(GraphModuleMixin, torch.nn.Module):
    """Generates node type embeddings.

    Args:
        type_names (List[str]): list of type names for atoms
        num_features (int): embedding dimension
    """

    num_types: int

    def __init__(
        self,
        type_names: List[str],
        num_features: int,
        irreps_in={},
    ):
        super().__init__()
        # === bookkeeping ===

        #possible bonds == (possible atoms)**2 (direction aware)
        self.num_types = int(len(type_names)**2)

        # === type embedding module ===
        self.embed_module = torch.nn.Embedding(
            num_embeddings=self.num_types,
            embedding_dim=num_features,
        )

        # === categorical graph field embedding ===
        total_features = num_features

        irreps_out = {AtomicDataDict.EDGE_FEATURES_KEY: Irreps([(total_features, (0, 1))])}

        self._init_irreps(irreps_in=irreps_in, irreps_out=irreps_out)

    def forward(self, data: AtomicDataDict.Type) -> AtomicDataDict.Type:
        # (2, num_bonds) -> (num_bonds, num_type_features)
        unique_bonds, edge_types = torch.unique(torch.transpose(data[AtomicDataDict.EDGE_TYPE_KEY],0,1),sorted=False, return_inverse=True, dim=0)
        embedding = self.embed_module(edge_types)
        
        data[AtomicDataDict.EDGE_FEATURES_KEY] = embedding

        return data
