from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        #return ['php7.0-cli', 'php7.0-fpm']

        results = []

        # Version parameters
        version = terms[2]

        #########
        # Sapis #
        #########

        itemDefault = {
            'state': 'present'
        }

        for term in self._flatten(terms[0]):

            items = []

            if isinstance(term, basestring):
                # Short syntax
                item = itemDefault.copy()
                item.update({
                    'package': term
                })
            else:
                # Must be a dict
                if not isinstance(term, dict):
                    raise AnsibleError('Expect a dict')
                if not term.has_key('sapi'):
                    raise AnsibleError('Expect "sapi" key')
                item = itemDefault.copy()
                item.update(term)
                item.update({
                    'package': item.get('sapi')
                })
                item.pop('sapi', None)

            # Known sapi ?
            if item.get('package') not in version['sapis']:
                raise AnsibleError('Unknown sapi "' + item.get('package') + '"')

            # Prefix package name
            item.update({
                'package': version['package_prefix'] + item.get('package')
            })

            items.append(item)

            # Merge by index key
            for item in items:
                itemFound = False
                for i, result in enumerate(results):
                    if result['package'] == item['package']:
                        results[i] = item
                        itemFound = True
                        break

                if not itemFound:
                    results.append(item)

        ##############
        # Extensions #
        ##############

        itemDefault = {
            'state': 'present'
        }

        for term in self._flatten(terms[1]):

            items = []

            if isinstance(term, basestring):
                # Short syntax
                item = itemDefault.copy()
                item.update({
                    'package': term
                })
            else:
                # Must be a dict
                if not isinstance(term, dict):
                    raise AnsibleError('Expect a dict')
                if not term.has_key('extension'):
                    raise AnsibleError('Expect "extension" key')
                item = itemDefault.copy()
                item.update(term)
                item.update({
                    'package': item.get('extension')
                })
                item.pop('extension', None)

            # Known as a sapi ?
            if item.get('package') in version['sapis']:
                raise AnsibleError('Extension "' + item.get('package') + '" is known as a sapi')

            # Already embedded extension ?
            if item.get('package') in version['extensions']:
                continue

            # Prefix package name
            item.update({
                'package': version['package_prefix'] + item.get('package')
            })

            items.append(item)

            # Merge by index key
            for item in items:
                itemFound = False
                for i, result in enumerate(results):
                    if result['package'] == item['package']:
                        results[i] = item
                        itemFound = True
                        break

                if not itemFound:
                    results.append(item)

        return results







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
