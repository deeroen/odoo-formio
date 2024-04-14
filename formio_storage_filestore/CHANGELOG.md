# Changelog

## 17.0.1.1.0

Improve the data for `formio.builder.js.options`:\
Record xmlid: `formio.formio_builder_js_options_storage_filestore`

## 17.0.1.0.0

Fixed (multi) file upload retrieval for backend, portal and public forms (request context/env).\
This applies to `GET /formio/storage/filestore` requests immediately after the upload, e.g. to preview images, that resulted in HTTP 403 Forbidden errors.\
This required to fixing and improving the URL/route authentication checks.\
Also done another security audit, so uploaded files cannot be retrieved without proper access/permission.

## 17.0.0.1

Initial release.
