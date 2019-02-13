#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 13.02.2019 14:21
:Licence MIT
Part of back3Sup

"""
import os
import sys
from hashlib import sha3_256

import boto3 as aws

AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_SESSION_TOKEN = 'AWS_SESSION_TOKEN'
BACK3SUP_BUCKET = 'backup'


def print_usage():
    print('Usage: back3Sup up|down directory')
    print('up|down:     up for upload, down for download')
    print('directory:   directory to backup')


def get_hash(path):
    engine = sha3_256()
    engine.update(path.encode('UTF8'))
    return engine.hexdigest()


def get_files(path, recursive_path=None):
    recursive_path = recursive_path or ''
    for filename in os.listdir(path):
        file = '/' + filename
        if os.path.isfile(path + file):
            yield recursive_path + filename
        elif os.path.isdir(path + file):
            yield from get_files(path + file, filename + '/')


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3 or (args[1] != 'up' and args[1] != 'down'):
        print_usage()
        exit(1)
    upload = args[1] == 'up'
    path = os.path.abspath('./' + args[2])
    if not os.path.isdir(path):
        print_usage()
        exit(1)
    print(('Upload from ' if upload else 'Download to ') + path)
    hash = get_hash(path)

    session = aws.setup_default_session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN', AWS_SESSION_TOKEN)
    )
    s3 = aws.resource('s3')
    backup = s3.Bucket(os.getenv('BACK3SUP_BUCKET', BACK3SUP_BUCKET))

    if upload:
        for f in get_files(path):
            print('Uploading ' + f)
            try:
                backup.upload_file(
                    os.path.abspath(path + '/' + f),
                    str(hash) + '/' + f
                )
            except Exception as e:
                print('Couldn\'t upload ' + f)
                print(e)

    if not upload:
        handled = False
        for f in backup.objects.all():
            if not f.key.startswith(hash):
                continue
            handled = True
            key = f.key  # type: str
            filename = key[64:]
            dest = os.path.abspath(path + filename)
            print('Downloading ' + filename)
            try:
                if not os.path.exists(os.path.dirname(dest)):
                    os.makedirs(os.path.dirname(dest))
                backup.download_file(f.key, dest)
            except Exception as e:
                print('Couldn\'t download ' + filename)
                print(e)
        if not handled:
            print('No such directory found')
