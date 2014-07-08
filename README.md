# hpfeeds-collector

This is a skeleton program meant people to fork and extend in order to make generic hpfeeds log collectors.

The function in `collector.py` named `parse` should be extended.  It should take a log line and produce a python dict that can be 
serialized into JSON (i.e. only strings, primitives, lists, and dicts as field values). If the line cannot be parsed for some reason, return `None`.

    def parse(line):
        # TODO: extend this
        return {}


Example:

    2004-01-07-14:36:58.7132 tcp(6) - 252.214.169.203 2064 192.168.27.180 21: 48 S [MacOS 8.0-8.6 OTTCP]
    2004-01-07-15:26:40.0209 tcp(6) - 244.233.22.102 61891 172.162.8.180 21: 60 S [FreeBSD 5.0-5.1 ]
    2004-01-07-16:48:30.1212 tcp(6) S 192.168.21.135 33395 172.162.8.91 80 [Linux 2.6 ]
    2004-01-07-16:48:41.4929 tcp(6) S 10.173.240.67 22110 192.168.14.178 81 [Windows XP SP1]

Parse function:

    def parse(line):
        import re
        regex = r'(?P<timestamp>\S+) (?P<proto>\S+)\(\d+\) (?P<flag>\S+) (?P<source_ip>\S+) (?P<source_port>\d+) (?P<dest_ip>\S+) (?P<dest_port>\d+)(: (?P<packet_size>\S+) (?P<tcp_flags>\S+))? \[(?P<osfp>.*)\]'                            
        mat = re.match(regex, line)
        if mat:
            rec = mat.groupdict()
            for name in rec.keys():
                if not rec[name]:
                    del rec[name]
            return rec
        return None

