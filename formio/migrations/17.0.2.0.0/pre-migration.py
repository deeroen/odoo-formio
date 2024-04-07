# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

def migrate(cr, version):
    cr.execute('ALTER TABLE formio_builder ADD COLUMN current_uuid character varying')
    cr.execute('UPDATE formio_builder SET current_uuid = public_uuid')
