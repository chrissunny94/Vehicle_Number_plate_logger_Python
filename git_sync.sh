#!/bin/sh
git config --global user.email "chrissunny94@gmail.com"
git config --global user.name "chrissunny94"

#git config --global credential.helper cache
#git config --global credential.helper cache
# Set git to use the credential memory cache

git config --global credential.helper 'cache --timeout=3600'
# Set the cache to timeout after 1 hour (setting is in seconds)

git pull
git add -A

git commit -m "$1"
git push -u origin master

