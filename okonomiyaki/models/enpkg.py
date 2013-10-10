"""Traitlets-based models for enpkg-related metadata."""
import json
import os
import zipfile

import os.path as op

from ..bundled.traitlets import HasTraits, Enum, Float, \
    Instance, List, Long, Unicode
from ..utils import compute_md5
from .common import _decode_none_values, _encode_none_values, info_from_z, \
    split_egg_name
from .egg import Dependency

_CAN_BE_NONE_KEYS = ["osdist", "platform", "python"]


class EnpkgS3IndexEntry(HasTraits):
    """
    Model an S3 legacy index entry.

    Note
    ----
    S3 legacy indexes are the ones generated by our s3 scripts inside
    buildsystem/buildware/scripts/s3, NOT the ones generated by epd_repo.
    """
    build = Long()
    md5 = Unicode()
    mtime = Float()
    egg_basename = Unicode()
    packages = List(Instance(Dependency))
    product = Enum(["pypi", "commercial", "free"], "commercial")
    python = Unicode()
    size = Long()
    type = Enum(["egg"])
    version = Unicode()

    @classmethod
    def from_data(cls, data):
        """Create a new EnpkgS3IndexEntry instance from a raw dict.

        A raw dict may be a decoded entry from our legacy enpkg S3 index.json

        Note: the passed in dictionary may be modified.
        """
        data = _decode_none_values(data, _CAN_BE_NONE_KEYS)
        data["packages"] = [
            Dependency.from_spec_string(s) for s in data["packages"]
        ]
        return cls(**data)

    @classmethod
    def from_egg(cls, path, product="commercial"):
        kw = {}
        with zipfile.ZipFile(path) as fp:
            data = info_from_z(fp)
            for k in ["build", "python", "type", "version"]:
                kw[k] = data[k]
            kw["packages"] = data.get("packages", [])
            kw["product"] = product
            kw["egg_basename"] = split_egg_name(op.basename(path))[0]

            st = os.stat(path)
            kw["mtime"] = st.st_mtime
            kw["size"] = st.st_size

            kw["md5"] = compute_md5(path)

        return cls.from_data(kw)

    @property
    def name(self):
        return self.egg_basename.lower()

    def to_dict(self):
        data = {"build": self.build,
                "egg_basename": self.egg_basename,
                "md5": self.md5,
                "mtime": self.mtime,
                "name": self.name,
                "packages": [str(p) for p in self.packages],
                "product": self.product,
                "python": self.python,
                "size": self.size,
                "type": self.type,
                "version": self.version}
        data = _encode_none_values(data, _CAN_BE_NONE_KEYS)
        return data

    def to_json(self):
        return json.dumps(self.to_dict())
