from ofxstatement.parser import CsvStatementParser
import csv
from io import StringIO

from . import TRANSACTION_TYPES

# The bank for some reason has varied the column labeling a lot.
# By collecting first lines of known CSV exports as signatures
# we catch any future changes to the CSV export format.

SIGNATURES = (
"Kirjauspäivä;Arvopäivä;Määrä  EUROA;\"Laji\";Selitys;\
Saaja/Maksaja;Saajan tilinumero ja pankin BIC;Viite;Viesti;Arkistointitunnus;",
"Kirjauspäivä;Arvopäivä;Määrä  ;\"Laji\";Selitys;Saaja/Maksaja;\
Saajan tilinumero ja pankin BIC;Viite;Viesti;Arkistointitunnus;",
"Kirjauspäivä;Arvopäivä;Määrä EUROA;Tapahtumalajikoodi;Selitys;\
Saaja/Maksaja;Saajan tilinumero;Viite;Viesti;Arkistotunnus;",
"Kirjauspäivä;Arvopäivä;Määrä EUROA;Laji;Selitys;Saaja/Maksaja;\
Saajan tilinumero ja pankin BIC;Viite;Viesti;Arkistointitunnus;",
"Kirjauspäivä;Arvopäivä;Määrä EUROA;Laji;Selitys;Saaja/Maksaja;\
Saajan tilinumero ja pankin BIC;Viite;Viesti;Arkistointitunnus",
)

class OPCsvStatementParser(CsvStatementParser):
    "parser for various variations with common field semantics"
    
    mappings = {
       "date":1, "amount":2, "trntype":4, "payee":5,
       "refnum":7, "memo":8, "id":9
       # "bank_account_to":6, 
    }

    date_format = "%d.%m.%Y"

    def __init__(self, fin):
        sin=StringIO()
        for l in fin:
           # Some versions from 2011 have broken CSV...
           sin.write(l.replace("&amp;amp;", "&"))
        sin.seek(0)
        super().__init__(sin)

    def split_records(self):
        return csv.reader(self.fin, delimiter=';', quotechar='"')
    
    def convert_transaction_type(self, op_tx_type, amount):
        return "DEBIT" if amount < 0 else "CREDIT"
    
    def parse_record(self, line):
        #Free Headerline
        if self.cur_record <= 1:
            return None

        # Change decimalsign from , to .
        # TODO: check if this needs (need a big transfer to test...)
        #       .replace('.','').replace(',','.')
        line[2] = line[2].replace(',', '.')

        # Set transaction type
        line[4] = self.convert_transaction_type(line[4], float(line[2]))

        # fill statement line according to mappings
        sl = super(OPCsvStatementParser, self).parse_record(line)
        
        return sl
