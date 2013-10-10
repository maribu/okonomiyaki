from ..bundled.traitlets import HasTraits, Instance
from ..errors import OkonomiyakiError

from .epd_platform import EPDPlatform

# This data representation is a bit stupid, but we keep it as is from
# buildware/epd_repo to make it easier to sync.
_SUBDIR = [
    # short     subdir                 arch     platform  osdist
    ('win-64', 'Windows/amd64', 'amd64', 'win32', None),
    ('win-32', 'Windows/x86', 'x86', 'win32', None),
    ('osx-64', 'MacOSX/amd64', 'amd64', 'darwin', None),
    ('osx-32', 'MacOSX/x86', 'x86', 'darwin', None),
    ('rh3-64', 'RedHat/RH3_amd64', 'amd64', 'linux2', 'RedHat_3'),
    ('rh3-32', 'RedHat/RH3_x86', 'x86', 'linux2', 'RedHat_3'),
    ('rh5-64', 'RedHat/RH5_amd64', 'amd64', 'linux2', 'RedHat_5'),
    ('rh5-32', 'RedHat/RH5_x86', 'x86', 'linux2', 'RedHat_5'),
    ('rh6-64', 'RedHat/RH6_amd64', 'amd64', 'linux2', 'RedHat_6'),
    ('sol-64', 'Solaris/Sol10_amd64', 'amd64', 'sunos5', 'Solaris_10'),
    ('sol-32', 'Solaris/Sol10_x86', 'x86', 'sunos5', 'Solaris_10'),
]


class LegacyEPDPlatform(HasTraits):
    _epd_platform = Instance(EPDPlatform)

    @classmethod
    def from_epd_platform_string(cls, epd_platform_string):
        _epd_platform = EPDPlatform.from_epd_string(epd_platform_string)
        return cls(_epd_platform)

    def __init__(self, _epd_platform, **kw):
        super(LegacyEPDPlatform, self).__init__(_epd_platform=_epd_platform,
                                                **kw)

    @property
    def arch(self):
        return self._epd_platform.arch

    @property
    def osdist(self):
        entry = self._get_entry(self.short)
        return entry[4]

    @property
    def platform(self):
        entry = self._get_entry(self.short)
        return entry[3]

    @property
    def short(self):
        return self._epd_platform.short

    @property
    def subdir(self):
        entry = self._get_entry(self.short)
        return entry[1]

    def _get_entry(self, short):
        for entry in _SUBDIR:
            if entry[0] == short:
                return entry
        raise OkonomiyakiError("Invalid short epd string: {0}".format(short))
