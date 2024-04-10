# Changelog

## 16.0.2.2.1

Fix Access Denied for portal users upon form submit, which has file(s) linked/uploaded.

PS File upload by public users was not affected.

The specific error message:
```
Access Denied by ACLs for operation: read, uid: ?, model: ir.attachment
You are not allowed to access 'Attachment' (ir.attachment) records.
This operation is allowed for the following groups:
	- User types/Internal User
```

This required to change the `formio.form` method `_process_storage_filestore_ir_attachments`.\
The query (search) on the `ir.attachment` model is now executed by `sudo`, which is safe in this (internal) method.

## 16.0.2.2.0

Fixed (multi) file upload retrieval for backend, portal and public forms (request context/env).\
This applies to `GET /formio/storage/filestore` requests immediately after the upload, e.g. to preview images, that resulted in HTTP 403 Forbidden errors.\
This required to fixing and improving the URL/route authentication checks.\
Also done another security audit, so uploaded files cannot be retrieved without proper access/permission.

## 16.0.2.1

Improve public user check, by checking either:
- no user in request.env, or ...
- the request user has the public user group (the added check).
This change isn't solving a vulnerability, but a public GET request was too restrictive and could be denied too quickly.

## 16.0.2.0

Fix security vulnerability for GET (file) request.\
The form access-check was missing here, which determines whether the (file) request is allowed or forbidden.\
Even though those file requests are obscured by a UUID (unique randomized) string in the file name, those were still publicly accessible before this fix.

## 16.0.1.0

Release.
