import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
from lightning.fabric.plugins.io.torch_io import TorchCheckpointIO


class HFCheckpointIO(TorchCheckpointIO):
    def __init__(self, model, suffix: str = "_huggingface"):
        self._model = model
        self._suffix = suffix

    def save_checkpoint(self, checkpoint: Dict[str, Any], path: Union[str, Path], storage_options: Optional[Any] = None) -> None:
        super().save_checkpoint(checkpoint, path, storage_options)
        base_path = os.path.splitext(path)[0] + self._suffix
        self._model.save_hf_checkpoint(base_path)
