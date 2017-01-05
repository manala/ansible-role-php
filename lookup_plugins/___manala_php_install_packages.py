from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        results = []

        # Version parameters
        version = terms[2]

        # Sapis
        sapis = self._flatten(terms[0])
        # Intersection with available sapis (dedupe on the same occasion)
        sapis = list(set(sapis) & set(version['sapis']))

        # Extensions
        extensions = self._flatten(terms[1])
        # Diff with embedded extensions and so on (dedupe on the same occasion)
        extensions = list(
            set(extensions)
            - set(version['extensions'])
            - set(version['sapis'])
        )

        # Packages
        packages = sapis + extensions

        for package in packages:
            results.append(
                version['package_prefix'] + package
            )

        return results
