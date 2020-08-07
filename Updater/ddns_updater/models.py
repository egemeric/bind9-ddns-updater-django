import random, string, re
from django.db import models
from django.utils import timezone
from django.conf import settings
from .errors import RootRecordChange , RecordNotFound


class Domain(models.Model):
    Domain_Name = models.CharField(max_length=100, unique=True,)
    Client_Ip4 = models.CharField(max_length=16)
    Domain_Secret = models.CharField(max_length=50, blank=True)
    Last_Change = models.DateTimeField(blank=True, null=True)
    Client_Type = models.CharField(max_length=500, null=True, blank=True)
    Client_LAN = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.Domain_Name

    def save(self, *args, **kwargs):
        if not self.Domain_Secret:
            letters_and_digits = string.ascii_letters + string.digits
            self.Domain_Secret = ''.join((random.choice(letters_and_digits) for i in range(50)))
        self.Last_Change = timezone.now()
        splited_domain=self.Domain_Name.split('.')
        if len(splited_domain) <= 3:
            raise RootRecordChange('RootRecord')
        else:
            self.save_config(splited_domain[0])
            super(Domain, self).save(*args, **kwargs)

    def save_config(self,splited_domain):
        regex_query=('((' + splited_domain + ')\s+A\s+)([0-9]|[.])+([\n]|$)')
        replaced_line=(splited_domain+'\t\t\t'+'A\t'+self.Client_Ip4 + '\n')
        bind9_file = open(settings.BIND9_FILE, 'r')
        regex_org = bind9_file.read()
        is_found=bool(re.search(regex_query,regex_org))
        if is_found:
            regex = re.sub(regex_query,  # Find the domain record line
                           replaced_line,  # replace with new ip
                           regex_org,
                           re.M)
            bind9_file.close()
            bind9_file_out = open(settings.BIND9_FILE, 'w')
            bind9_file_out.write(regex)
            bind9_file_out.close()
            file=open(settings.BIND9_FILE+'.log','a')
            file.write(self.Client_Ip4  + ',' + str(timezone.now().isoformat()) + ',ok\n')
            file.close()
        else:
            file = open(settings.BIND9_FILE + '.log', 'a')
            file.write(self.Client_Ip4 + ',' + str(timezone.now().isoformat()) + ',fail\n')
            file.close()
            raise RecordNotFound('Requested update record is not found you can add manually')



