#/usr/bin/python

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)

def connect_key(hostname, username, filename):
    import paramiko
    import os.path

    my_hostname = hostname
    my_username = username
    my_keyfile = filename

    if "~" in my_keyfile: 
        from os.path import expanduser
        import re
        home = expanduser("~")
        my_keyfile = re.sub('~', home, my_keyfile.rstrip())

    if "$HOME" in my_keyfile: 
        from os.path import expanduser
        import re
        home = expanduser("$HOME")
        my_keyfile = re.sub('$HOME', home, my_keyfile.rstrip())

    if not os.path.isfile(my_keyfile):
        raise ValueError('Key file not found')
        sys.exit(0)
    sshcon = paramiko.SSHClient()
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # no known_hosts error
    sshcon.connect(my_hostname,username=my_username,key_filename=my_keyfile)

    return sshcon

def connect_password(hostname, username, password):
    import paramiko
    import os.path

    my_hostname = hostname
    my_username = username
    my_password = password
    
    sshcon = paramiko.SSHClient()
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # no known_hosts error
    sshcon.connect(my_hostname,username=my_username,password=my_password)

    return sshcon

def check_CPU_core(connection):
    command = "cat /proc/cpuinfo|grep MHz|wc -l"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    return list[0]  
     
def check_CPU_usage(connection):
    command = "for x in $(seq 1 11);do sleep 5;grep -w cpu /proc/stat ; done | \
    awk '{\nprint (o2+o4-$2-$4)*100/(o2+o4+o5-$2-$4-$5)\no2=$2;o4=$4;o5=$5}\'"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    #results = map(int, list.strip('\n'))
    results = [ float(elements.strip('\n')) for elements in list ]
    average = sum(results) / float(len(results))
    return round(average,3) if (average < 1 ) else round(average,2)

def check_mem_amount(connection):
    command = "free -m | awk 'NR==2'|awk '{ print $2 }'"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    return list[0]

def check_mem_swap(connection):
    command = "free -m | awk 'NR==4'|awk '{ print $2 }'"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    return list[0]

def check_mem_usage(connection):
    command = "free -m| grep Mem|awk {'print $3*100/$2'}"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    return list[0]

def check_disk(connection):
    command = "(dd if=/dev/zero of=test_$$ bs=64k count=16k conv=fdatasync &&rm -f test_$$) 2>&1 | tail -1| awk '{ print $(NF-1) $NF }'"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    return list[0]

def list_path(connection, path):
    command = "ls " +  path
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    #print "Listing Path = "
    return list

def check_phpprocess_size(connection):
    command = "for x in `ps -ef |grep php| grep -v grep | grep -v root | awk {'print $2'} `; do cat /proc/$x/status|grep VmSize|awk {'print $2'}; done"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    #print list
    results = [ float(elements.strip('\n')) for elements in list ]
    average = sum(results) / float(len(results))
    return round(average/1000,2)

def normailizing_unicode(uni):
    import unicodedata
    return unicodedata.normalize('NFKD', uni).encode('ascii','ignore')

def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

def check_generator(value):
    for i in value:
        return True
    return False    

def get_generator_value(value):
    output = []
    check = True
    for i in value:
        for j in output:
            if i==j:
                check = False
        if check and (type(i) is list):
            output = output + i
        else:
            output = output + [i]
    return output

def transform_config(config_value):
    from collections import defaultdict
    import itertools
    result = {}
    for k, v in config_value:
        #print "k = "
        #print k
        #print "v = "
        #print v
        if type(v) is unicode:
            #print "Type(v) is unicode"
            if check_generator(find(normailizing_unicode(k),result)):
                duplicated = get_generator_value(find(normailizing_unicode(k),result))
                write = True
                for i in duplicated:
                    if i == normailizing_unicode(v):
                        write = False
                if write:
                    resultant_value = duplicated + [ normailizing_unicode(v) ]
                #print "Resultant Value = "
                #print resultant_value
                result[normailizing_unicode(k)] = resultant_value
            else:
                result[normailizing_unicode(k)] = normailizing_unicode(v)
        else:
            if type(k) is not unicode:
                temp_d = {}
                for k1, v1 in v:
                    if type(v1) is unicode:
                        temp_d.update({normailizing_unicode(k1):normailizing_unicode(v1)})
                        # result[k[0]] = {k1: v1}
                    else:
                        for k2, v2 in v1:
                            pass
                            #print "third level of dictionary"
                result[normailizing_unicode(k[0])] = temp_d
            else:
                result[normailizing_unicode(k)] = normailizing_unicode(v)
        #print "result = "
        #print result
    return result

def read_nginxsite(nginxconf, connection):
    value = find('fuck', nginxconf)
    check_generator(value)

def read_nginxconfig(connection, filename = '/etc/nginx/nginx.conf'):

    command = "if [ -f '" + filename + "' ]; then cat " + filename + "; elif [ -h '" + filename + "' ]; then  cat `file " + filename + " | awk '{print $5}'`; else echo 'not_found'; fi"
    #print "Command = "
    #print command
    #print "Before running the command"
    stdin, stdout, stderr = connection.exec_command(command)
    #print "Right after running the command"
    output = stdout.readlines()
    #print "Finishing running command to get nginx file content"
    #print "Output = "
    #print output
    if output[0].strip('\n') == 'not_found':
        return False
    else:
        import os, sys
        lib_path = os.path.abspath(os.path.join("./nginxparser"))
        sys.path.append(lib_path)
        import nginxparser
        #print "Result of the file READ"
        #print output
        #print "remove line with hash"
        output = [x for x in output if not normailizing_unicode(x).startswith('#')]
        #print "remove empty lines"
        output = [x for x in output if not normailizing_unicode(x).startswith('\n')]
        #print "Printing output again"
        #print output
        if not output:
            return False
        config_value = nginxparser.loads(''.join(output))
        #print "********************************************************************"
        nginxconf = transform_config(config_value)
        # nginxsite = read_nginxsite(nginxconf, connection)
        #print "NGINX Config ====================================================="
        #print nginxconf
        #print "\n"
        # print "NGINX Sites  ====================================================="
        # print nginxsite
        return nginxconf
    #print "Total finish of read_nginxconfig"

def read_nginx_included_files(connection, nginx_config):
    included_files = find('include', nginx_config);
    #print "List of included Files"
    #print included_files
    included_files = get_generator_value(included_files)

    from collections import OrderedDict
    included_files = list(OrderedDict.fromkeys(included_files))
    included_config = {}
    count = 0

    #print "included_files list = "
    #print included_files
    #print "===========================GETTING included VALUES======================================"
    for config in included_files:
        #print "File Number " + str(count) + "==========================================================="
        #print "File name = ",
        #print config
        #print "After running list path"
        files =  list_path(connection, config)
        #print "Files = "
        #print files
        for file in files:
            #print "Before running read to nginx config"
            temp = read_nginxconfig(connection, file.strip('\n'))
            if temp:
                included_config[count] = temp
                count = count + 1
    #print "====================================Finished ==========================================="
    #print "Included config = "
    #print included_config
    return included_config