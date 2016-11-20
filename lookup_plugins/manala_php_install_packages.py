from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        results = []

        # Version parameters
        version = variables['manala_php_versions'][terms[0]]

        # Sapis
        sapis = self._flatten(terms[1])
        # Intersection with available sapis (dedupe on the same occasion)
        sapis = list(set(sapis) & set(version['sapis_available']))
        # Merge with forced sapis
        sapis += version['sapis_forced']

        # Extensions
        extensions = self._flatten(terms[2])
        # Diff with extensions embedded and so on (dedupe on the same occasion)
        extensions = list(
            set(extensions)
            - set(version['extensions_embedded'])
            - set(version['sapis_available'])
            - set(version['sapis_forced'])
            - set(version['packages_common'])
        )

        for package in (sapis + extensions):
            results.append(
                version['package_template'].format(package=package)
            )

        return results
