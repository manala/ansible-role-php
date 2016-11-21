from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        results = []

        # Packages
        packages = self._flatten(terms[0])

        # Packages dependencies
        packagesDependencies = self._flatten(terms[1])

        # Packages installed
        packagesInstalled = self._flatten(terms[2])

        # Compute lists difference
        packagesExclusive = list(set(packagesInstalled) - set(packages + packagesDependencies))

        for package in packagesExclusive:
            results.append(package)

        return results
