# log-file-analysis

To run: 

1. **-n**: Number of unique IP addresses in the log file: `python3 assign5_17712081.py -l apache.log -n` or `python3 assign5_17712081.py -l apache_short.log -n`

2. **-t N**: List top N IP addresses in the log file by the number of requests (where N is an integer): `python3 assign5_17712081.py -l apache.log -n 4` or `python3 assign5_17712081.py -l apache_short.log -n 4`

3. **-v IP**: Number of visits by an IP address: `python3 assign5_17712081.py -l apache.log -v 66.249.78.114` or `python3 assign5_17712081.py -l apache_short.log -v 66.249.78.114`

4. **-L IP**: List all of the requests made by an IP address: `python3 assign5_17712081.py -l apache.log -L 92.112.13.66` or `python3 assign5_17712081.py -l apache_short.log -L 66.249.78.114`

5. **-d Date**: List number of visits of all requests on a specific date (date is in ddMMMyyyy format): `python3 assign5_17712081.py -l apache.log -d 09Feb2013` or `python3 assign5_17712081.py -l apache_short.log -d 09Feb2013`
