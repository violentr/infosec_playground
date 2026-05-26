#!/usr/bin/env bash
# Dump Mongo db, will save JSON and BSON files to dump folder
# mongodump --uri="mongodb+srv://$USER:$PASS/?appName=educative" --db sample_mflix
#
echo -e "Importing Bson files"
db="sample_mflix"
for bson_file in $(ls |grep bson)
do
  name=$(echo $bson_file | cut -d "." -f1)
  mongorestore --db $db --collection $name $bson_file
don
