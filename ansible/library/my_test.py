#!/usr/bin/python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: findstring

short_description: Return OK if string is present in a file
version_added: "1.0.0"

options:
    stringa:
      description: la stringa da ricercare
      type: str
      required: true
    file:
      description: il path del file in cui ricercare la stringa
      type: str
      required: true




author:
    - martino.vigano@kalinkanet.com
'''



from ansible.module_utils.basic import AnsibleModule
import os
def check_file_properties(path):
    
    if not os.path.exists(path):
        return False, False, "Il file non esiste"
    
    is_readable = os.access(path, os.R_OK)
    if not is_readable:
        return False, False, "Il file esiste ma non è leggibile"

    is_text = True
    try:
        with open(path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:
                is_text = False
    except Exception as e:
        return is_readable, False, f"Errore durante la lettura del file: {str(e)}"

    if is_text:
        return is_readable, is_text, "Verifica completata con successo"
    else:
        return is_readable, is_text, "Il file non è di testo"

def trova_stringa(stringa,file):
    with open(file, 'r', encoding='utf-8') as f:
        for linea in f:
            if stringa in linea:
                return True
    return False

def run_module():
    module_args = dict(
        stringa=dict(type='str', required=True),
        file=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json(**result)

    result['stringa'] = module.params['stringa']
    result['file'] = module.params['file']

    
    leggibile, ditesto, messaggio = check_file_properties(module.params['file'])

    if not (leggibile and ditesto):
        module.fail_json(msg=messaggio)

    # Arrivato qui il file esiste ed èsano
    # Controllo se la stringa è presente

    
    if not trova_stringa(module.params['stringa'],module.params['file']):
        module.exit_json(**result,output='Stringa non trovata')
    else:
        result['changed']=True
        module.exit_json(**result,output='Stringa PRESENTE!')


def main():
    run_module()


if __name__ == '__main__':
    main()
