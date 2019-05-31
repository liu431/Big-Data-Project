'''
Creates csv files for PostHistory and PostLinks
'''
from xml.etree.ElementTree import iterparse
import csv

#Reference: 
# https://stackoverflow.com/questions/50010843/iterate-through-huge-xml-file-and-get-the-value

#-------------------------------
'''
Post History CSV
'''
count = 1

with open('sample_PostHistory.csv', 'w') as write_file:
    posthistory_data = [['Id', 'PostHistoryTypeId', 'PostId', \
                'RevisionGUID', 'CreationDate', 'UserId', 'Text']]
    for evt, elem in iterparse('PostHistory.xml', events=('end',)):   
        if elem.tag == 'row':
            ph_data = elem.attrib
            Id = ph_data.get('Id')
            PostHistoryTypeId = ph_data.get('PostHistoryTypeId')
            PostId = ph_data.get('PostId')
            RevisionGUID = ph_data.get('RevisionGUID')
            CreationDate = ph_data.get('CreationDate')
            UserId = ph_data.get('UserId')
            Text = ph_data.get('Text')

            posthistory_data.append([Id, PostHistoryTypeId, PostId, RevisionGUID, \
                CreationDate, UserId, Text])

        count += 1
        if count > 500:
            break

    writer = csv.writer(write_file)
    for row in posthistory_data:
        writer.writerow(row)

write_file.close()

#----------------------------------------
'''
Post Links 
'''
count = 1

with open('sample_PostLinks.csv', 'w') as write_file:
    posthistory_data = [['Id', 'CreationDate', 'PostId', 'RelatedPostId', 'LinkTypeId']]
    for evt, elem in iterparse('PostLinks.xml', events=('end',)):   
        if elem.tag == 'row':
            pl_data = elem.attrib
            Id = pl_data.get('Id')
            CreationDate = pl_data.get('CreationDate')
            PostId = pl_data.get('PostId')
            RelatedPostId = pl_data.get('RelatedPostId')
            LinkTypeId = pl_data.get('LinkTypeId')

            posthistory_data.append([Id, CreationDate, PostId, RelatedPostId, LinkTypeId])

        count += 1
        if count > 500:
            break

    writer = csv.writer(write_file)
    for row in posthistory_data:
        writer.writerow(row)

write_file.close()
