# This file is a part of the `nequip` package. Please see LICENSE and README at the root for information on using it.
import torch
import ase
import ase.io
import json

from .. import AtomicDataDict
from ..ase import from_ase_withbond, from_ase
from .base_datasets import AtomicDataset

from typing import Union, Dict, List, Optional, Callable, Any


class ASEBondDataset(AtomicDataset):
    """:class:`~nequip.data.dataset.AtomicDataset` for `ASE <https://wiki.fysik.dtu.dk/ase/ase/io/io.html>`_-readable file formats.

    Args:
        file_path (str): path to ASE-readable file
        bond_json_path (str): path to bond json (in same order as file_path)
        transforms (List[Callable]): list of data transforms
        ase_args (Dict[str, Any]): arguments for :func:`ase.io.iread`
        include_keys (List[str]): the keys that needs to be parsed into dataset in addition to standard keys (see :doc:`../../../api/data_fields`). The data stored in :attr:`ase.atoms.Atoms.array` has the lowest priority, and it will be overrided by data in :attr:`ase.atoms.Atoms.info` and :attr:`ase.atoms.Atoms.calc.results`
        exclude_keys (List[str]): list of keys that may be present in the ASE-readable file but the user wishes to exclude
        key_mapping (Dict[str, str]): mapping of ``ase`` keys to ``AtomicDataDict`` keys
    """

    def __init__(
        self,
        file_path: str,
        bond_json_path: str,
        transforms: List[Callable] = [],
        ase_args: Dict[str, Any] = {},
        include_keys: Optional[List[str]] = [],
        exclude_keys: Optional[List[str]] = [],
        key_mapping: Optional[Dict[str, str]] = {},
    ):
        super().__init__(transforms=transforms)
        self.file_path = file_path
        self.bond_json_path = bond_json_path
        # process ase_args
        self.ase_args = {}
        self.ase_args.update(ase_args)
        assert "index" not in self.ase_args
        assert "filename" not in self.ase_args
        self.ase_args.update({"filename": self.file_path})

        # read json and construct list of dicts to feed into next step
        with open(self.bond_json_path, 'r') as file:
            bond_dicts = json.load(file)

        # read file and construct list of AtomicDataDicts
        self.data_list: List[AtomicDataDict.Type] = []
        for index, atoms in enumerate(ase.io.iread(**self.ase_args, parallel=False)):
            bond_dict = bond_dicts[index]
            self.data_list.append(
                from_ase_withbond(
                    atoms=atoms,
                    bond_dict=bond_dict,
                    key_mapping=key_mapping,
                    include_keys=include_keys,
                    exclude_keys=exclude_keys,
                )
            )

    def __len__(self) -> int:
        return len(self.data_list)

    def _get_data_list(
        self,
        indices: Union[List[int], torch.Tensor, slice],
    ) -> List[AtomicDataDict.Type]:
        if isinstance(indices, slice):
            return self.data_list[indices]
        else:
            return [self.data_list[index] for index in indices]
