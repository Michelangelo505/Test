from django.db import models
import csv
# Create your models here.

class Customer(models.Model):
    username = models.CharField(max_length=25)
    spent_money = models.IntegerField()

    def __str__(self):
        return self.username

    @staticmethod
    def ParserDealsCSV(file_path):
        dict_csv = {}
        try:
            with open(file_path,'r') as ObjFile:
                reader = csv.DictReader(ObjFile, delimiter=',')
                for row in reader:
                    key = row['customer']
                    total = int(row['total'])
                    gem = row['item']

                    if dict_csv.get(key):
                        dict_csv[key][0] += total

                        if not (gem in dict_csv[key][1]):
                            dict_csv[key][1].append(gem)
                    else:
                        dict_csv.update({key: [total, [gem]]})
        except:
            return None
        else:
            return dict_csv

class Gem(models.Model):
    customer = models.ForeignKey(to='Customer',on_delete=models.CASCADE,related_name='gem')
    item = models.CharField(max_length=25)

    def __str__(self):
        return self.item

class UploadFile(models.Model):
    deals = models.FileField(blank=False,null=False)