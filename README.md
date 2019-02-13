# back3Sup

Library for uploading and downloading files to the 3S Amazon service.

## Prerequisites

- Setup dependencies using command `pip install -r requirements.txt`.
- Get keys from the Amazon Web service. 
You need AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN keys.
- Pass the keys to the program by setting them as environment variable or modify the source code.
- Create bucket for the backups. Default name is *backup* bucket.
- Set BACK3SUP_BUCKET env variable or modify the source code to set different bucket.

## Usage

`back3Sup.py up|down directory`

Use `up` for uploading files to the 3S bucket and `down` for downloading last version of the files.

Directory specify which directory to backup. 
You can backup different directories into single bucket.
The downloading depends on the directory path.

## History

You can keep history of the files by activating Versioning property on the bucket,
viz. https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-versioning.html.

----------------------------
Author: Patrik Valkovič  
Licence: MIT
