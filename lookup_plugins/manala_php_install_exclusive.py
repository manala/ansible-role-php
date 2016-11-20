from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

class LookupModule(LookupBase):

    def _prefix(self, package, prefix):
        return prefix + package

    def _unprefix(self, package, prefix):
        return package.replace(prefix, '')

    def _sapis(self, sapis, version):
        # Intersection with available sapis (dedupe on the same occasion)
        sapis = list(set(sapis) & set(version['sapis_available']))
        # Merge with forced sapis
        sapis += version['sapis_forced']
        return sapis

    def _extensions(self, extensions, version):
        # Diff with extensions embedded and so on (dedupe on the same occasion)
        extensions = list(
            set(extensions)
            - set(version['extensions_embedded'])
            - set(version['sapis_available'])
            - set(version['sapis_forced'])
            - set(version['packages_common'])
        )
        return extensions

    def run(self, terms, variables=None, **kwargs):

        results = []

        # Version parameters
        version = terms[4]

        packagesInstalled = [self._unprefix(package, version['package_prefix']) for package in terms[5]]

        # Sapis
        # sapis = self._flatten(terms[0])
        # # Intersection with available sapis (dedupe on the same occasion)
        # sapis = list(set(sapis) & set(version['sapis_available']))
        # # Merge with forced sapis
        # sapis += version['sapis_forced']
        sapis = self._sapis(self._flatten(terms[0]), version)

        # Sapis exclusice
        sapisExclusive = terms[1]

        # Extensions
        # extensions = self._flatten(terms[2])
        # # Diff with extensions embedded and so on (dedupe on the same occasion)
        # extensions = list(
        #     set(extensions)
        #     - set(version['extensions_embedded'])
        #     - set(version['sapis_available'])
        #     - set(version['sapis_forced'])
        #     - set(version['packages_common'])
        # )
        extensions = self._extensions(self._flatten(terms[2]), version)

        # Extensions exclusice
        extensionsExclusive = terms[3]

        #print(terms)
        #print(version)
        print(packagesInstalled)

        for package in (sapis + extensions):
            results.append(
                self._prefix(package, version['package_prefix'])
            )

        return results
