from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        results = []

        # Version parameters
        version = terms[1]

        wantprefix = kwargs.pop('wantprefix', False)
        wantstate  = kwargs.pop('wantstate', None)
        wantmap    = kwargs.pop('wantmap', None)

        #########
        # Sapis #
        #########

        itemDefault = {
            'state': 'present'
        }

        # Exclusive
        wantexclusive = kwargs.pop('wantexclusive', False)

        if wantexclusive:
            results = [{
                'package': sapi,
                'state':   'absent'
            } for sapi in version['sapis']]

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

        # Prefix package name
        if wantprefix:
            for i, result in enumerate(results):
                result.update({
                    'package': version['package_prefix'] + result.get('package')
                })

        # Filter by state
        if wantstate:
            results = [result for result in results if result.get('state') == wantstate]

        # Map
        if wantmap:
            results = [result.get(wantmap) for result in results]

        return results
