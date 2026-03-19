# File: models.py
# Author: Leigh Brown (ljbrown@bu.edu), 3/17/2026
# Description: create the voter model to showcase records from the csv file.

from django.db import models
import datetime #for conversion

# Create your models here.

class Voter(models.Model):
    '''
    store data for voters
    '''
    # identification
    last_name = models.TextField()
    first_name = models.TextField()

    # adress
    street_num = models.IntegerField()
    street_name = models.TextField()
    apt_num = models.CharField(max_length=10, blank=True) #not an int bc some #s have letters in them
    zip = models.IntegerField()

    #dates, allow null for placeholders. trying to not skip records
    date_of_birth = models.DateField(null=True, blank=True)
    reg_date = models.DateField(null=True, blank=True)

    #party
    party = models.CharField(max_length=2)
    prec_num = models.CharField()

    #elections
    v20 = models.BooleanField()
    v21t = models.BooleanField()
    v21p = models.BooleanField()
    v22 = models.BooleanField()
    v23 = models.BooleanField()

    score = models.IntegerField()

 
    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}, party: {self.party}, score: {self.score}'
    

# helper functions to deal with data capture (issues with boolean values and invalid dates)

def to_bool(field):
    ''' convert boolean values from the fields. to deal with this error: django.core.exceptions.ValidationError: ['“FALSE” value must be either True or False.']'''
    field = field.strip().upper()

    if field in ['TRUE', 'T', 'YES', 'Y', '1']:
        return True
    elif field in ['FALSE', 'F', 'NO', 'N', '0', '']:
        return False
    else:
        raise ValueError(f"Invalid boolean value: {field}")
    
def placeholder_date(field):
    '''convert empty/placeholder dates into none and then convert real dates in the wrong format to the right one'''
    field = field.strip()

    #invalid dates
    if field == '':
        return None

    if field == '1900-01-00':
        return None
    
    #wrong format dates
    if '-' in field:
        return field
    
    try:
        if '/' in field:
            d = datetime.datetime.strptime(field, '%m/%d/%Y').date() #convert it
        else:
            return None

        if d.year < 1700: 
            return None

        return d

    except:
        return None
    

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
 
	# delete existing records to prevent duplicates:
    Voter.objects.all().delete()
	
    filename = '/Users/leeboun/Desktop/cs412/django/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
 
    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of voter object with this record from CSV
            voter = Voter(last_name = fields[1], #0 is the voter id num
                        first_name = fields[2],

                        # adress
                        street_num = fields[3],
                        street_name = fields[4],
                        apt_num = fields[5],
                        zip = fields[6],

                        #dates
                        date_of_birth = placeholder_date(fields[7]),
                        reg_date = placeholder_date(fields[8]),

                        #party
                        party = fields[9],
                        prec_num = fields[10],

                        #elections
                        v20 = to_bool(fields[11]),
                        v21t = to_bool(fields[12]),
                        v21p = to_bool(fields[13]),
                        v22 = to_bool(fields[14]),
                        v23 = to_bool(fields[15]),

                        score = fields[16],
                        )
        


            voter.save() # commit to database
            print(f'Created voter: {voter}')
            
        except:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} voters.')

    