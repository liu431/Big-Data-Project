#!/bin/bash
#
# This Bash script performs a data preparation for
# 	Exploring answer providers task.
#
# Main author: Dhruval, Sanittawan (Nikki)

gsutil cp gs://capp-3-stackoverflow/CSV_Files/Badges.csv /home/sanittawan/

gsutil cp gs://capp-3-stackoverflow/CSV_Files/Users.csv /home/sanittawan/

mawk -F, '{$(NF)="badges";}1' OFS=, Badges.csv > Badges_new.csv

mawk -F, '{$(NF)="users";}1' OFS=, Users.csv > Users_new.csv

cat Badges_new.csv Users_new.csv > Badges_Users.csv

gsutil -m cp Badges_Users.csv gs://capp3-nikki
