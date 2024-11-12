import csv
from django.db import models
from datetime import datetime

class Voter(models.Model):
    # Personal Information
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=10)  # Keeping it flexible for varying party abbreviations

    # Address Information
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=5)
    
    # Precinct Information
    precinct_number = models.CharField(max_length=5)

    # Voting History
    v20state = models.BooleanField(default=False)    # Participation in 2020 state election
    v21town = models.BooleanField(default=False)     # Participation in 2021 town election
    v21primary = models.BooleanField(default=False)  # Participation in 2021 primary election
    v22general = models.BooleanField(default=False)  # Participation in 2022 general election
    v23town = models.BooleanField(default=False)     # Participation in 2023 town election

    # Voter Score
    voter_score = models.IntegerField(default=0)     # Number of elections participated in

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}, Score: {self.voter_score}"

def load_data():
    '''Function to load voter data records from CSV file into Django model instances.'''
    
    filename = '/Users/evaromero/Desktop/newton_voters.csv'
    
    with open(filename, encoding='utf-8') as f:
        f.readline()  # Discard headers
        
        for line in f:
            fields = line.strip().split(',')
            
            # Create a new instance of Voter object with this record from CSV
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5] if fields[5] else None,
                zip_code=fields[6],
                date_of_birth=datetime.strptime(fields[7], '%Y-%m-%d').date(),
                date_of_registration=datetime.strptime(fields[8], '%Y-%m-%d').date(),
                party_affiliation=fields[9],
                precinct_number=fields[10].strip(),
                v20state=fields[11].strip().upper() == 'TRUE',
                v21town=fields[12].strip().upper() == 'TRUE',
                v21primary=fields[13].strip().upper() == 'TRUE',
                v22general=fields[14].strip().upper() == 'TRUE',
                v23town=fields[15].strip().upper() == 'TRUE',
                voter_score=int(fields[16])
            )
            
            # Save the voter instance to the database
            voter.save()
            print(f'Created voter: {voter}')
