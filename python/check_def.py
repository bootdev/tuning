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
    return normailizing_unicode(list[0].strip('\n'))  
     
def check_CPU_usage(connection):
    command = "for x in $(seq 1 11);do sleep 5;grep -w cpu /proc/stat ; done | \
    awk '{\nprint (o2+o4-$2-$4)*100/(o2+o4+o5-$2-$4-$5)\no2=$2;o4=$4;o5=$5}\'"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    #results = map(int, list.strip('\n'))
    results = [ float(elements.strip('\n')) for elements in list ]
    average = sum(results) / float(len(results))
    return round(average,3) if (average < 1 ) else round(average,2)

def check_ulimit(connection):
    command = "ulimit -n"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    return normailizing_unicode(list[0].strip('\n'))    

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
    #print "Path = "
    #print path
    command = "ls " +  path
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    #print "Listing Path = "
    return list

def check_phpprocess_size(connection):
    #command = "for x in `ps -ef |grep php| grep -v grep | grep -v root | awk {'print $2'} `; do cat /proc/$x/status|grep VmSize|awk {'print $2'}; done"
    command = "ps -eo size,pid,user,command --sort -size | awk '{ hr=$1/1024 ; printf(\"%13.2f Mb \",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf(\"%s \",$x) } print \"\" }'| grep php| grep pool| grep -v grep| awk {'print $1'}"
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    #print list
    results = [ float(elements.strip('\n')) for elements in list ]
    average = sum(results) / float(len(results))
    return round(average,2)

def normailizing_unicode(uni):
    import unicodedata
    return unicodedata.normalize('NFKD', uni).encode('ascii','ignore')

def find(key, dictionary):
    #print "key = "
    #print key
    #print "Dictionary = "
    #print dictionary
    if (dictionary) and (key):
        if isinstance(dictionary, str):
            yield dictionary
        else:
            for k, v in dictionary.iteritems():
                #print "k = "
                #print k
                #print "v = "
                #print v
                if k == key:
                    yield v
                elif isinstance(v, dict):
                    for result in find(key, v):
                        yield result
                #elif isinstance(v, list):
                #    for d in v:
                #        for result in find(key, d):
                #            yield result

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
    #print config_value
    result['include'] = []
    #print "Inputed config values"
    #print config_value
    for k, v in config_value:
        #print "k = "
        #print k
        #print "v = "
        #print v
        # Special handle include:
        if (type(k) is unicode) and (normailizing_unicode(k) == 'include'):
            #print "v = "
            #print v
            result['include'].append(normailizing_unicode(v))
        else:
            if type(v) is unicode:
                result[normailizing_unicode(k)] = normailizing_unicode(v)
            else:
                #print "Type(v) is NOT unicode"
                if type(k) is not unicode:
                    #print "Type(k) is unicode"
                    temp_d = {}
                    #print "Value to be inserted"
                    #print v
                    for k1, v1 in v:
                        if (type(k1) is unicode) and (normailizing_unicode(k1) == 'include'):
                            #print "k1 = ",
                            #print k1
                            #print "v1 = ",
                            #print v1
                            result['include'].append(normailizing_unicode(v1))
                        if type(v1) is unicode:
                            temp_d.update({normailizing_unicode(k1):normailizing_unicode(v1)})
                            # result[k[0]] = {k1: v1}
                        else:
                            #print "v1 is not unicode"
                            if k1 is unicode:
                                for k2, v2 in v1:
                                    if type(v2) is unicode:
                                        #print "k2 = ",
                                        #print k2
                                        #print "v2 = ",
                                        #print v2
                                        pass
                                    else: 
                                        pass
                                        #print "v2 is not unicode"
                            else:
                                #print "k1 = ",
                                #print k1
                                #print "v1 = ",
                                #print v1
                                #print "third level of dictionary"
                                k1 = " ".join(k1)
                                temp_d.update({normailizing_unicode(k1):v1})
                    result[normailizing_unicode(k[0])] = temp_d
                else:
                    result[normailizing_unicode(k)] = normailizing_unicode(v)
        #print "result = "
        #print result
    if result['include'] == []:
        del result['include']
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
    print "Finishing running command to get nginx file content"
    print "Output = "
    print output
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
        output = [x.strip() for x in output]
        output = [x for x in output if not normailizing_unicode(x).startswith('#')]
        #print "remove empty lines"
        output = [x for x in output if not normailizing_unicode(x).startswith('\n')]
        #print "remove empty value"
        output = [x for x in output if normailizing_unicode(x)]
        #print "Replacing all tabs"
        #output = [x for x in output if not normailizing_unicode(x).replace("\t", "    ")]
        #print "Removing empty field"
        #output = [x for x in output if not normailizing_unicode(x)]
        #print "Printing output again"
        #print output
        #print "Output become string"
        #print ''.join(output)
        #print "Type of output"
        #print type(output)
        #print "Length of output"
        #print len(output)
        if not output:
            return False
        #print "Output = "
        #print output
        #print "Current file name = ", 
        #print filename
        config_value = {}
        try:
            config_value = nginxparser.loads(''.join(output))
        except:
            print "Please check the format of nginx config file " + filename
        #print "Print result after importing by library++++++++++++++++++++++++++++++++++++++"
        #print config_value
        #config_value = nginxparser.loads(output)
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
    #print "Reading included files"
    #included_files = find('include', nginx_config);
    included_files = nginx_config['include']
    #print "List of included Files"
    #print included_files
    included_files = get_generator_value(included_files)
    #print "included_files value"
    #print included_files

    from collections import OrderedDict
    #print "Type of included_files = "
    #print type(included_files)
    included_files = list(OrderedDict.fromkeys(included_files))
    included_config = {}
    count = 0

    # Removing /etc/nginx/mime.types
    included_files = [x for x in included_files if (x != '/etc/nginx/mime.types')]
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
            print "Running for " + file
            #print "Before running read to nginx config"
            temp = read_nginxconfig(connection, file.strip('\n'))
            #print temp
            if temp:
                included_config[count] = temp
                count = count + 1
    #print "====================================Finished ==========================================="
    #print "Included config = "
    #print included_config
    return included_config

def get_phpfpm_path(connection):
    command = 'ps -ef|grep php|grep master|grep -v grep'
    #print "Command = "
    #print command
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    #print "Output is :"
    #print list
    import re
    #print normailizing_unicode(list[0])
    result = re.search('\((.*?)\)', list[0]).group(1)
    #print result
    return result

def get_phpfpm_conf(connection, config_file_path):
    command = 'cat ' + config_file_path
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    output = list
    output = [x for x in output if not normailizing_unicode(x).startswith(';')]
    output = [x for x in output if not normailizing_unicode(x).startswith('\n')]
    primary = output
    #print output
    included_files = [x for x in output if normailizing_unicode(x).startswith('include')]
    #print included_files
    files = []
    for x in included_files:
        path = normailizing_unicode(x).strip('\n').strip('include=')
        #print "Path = ",
        #print path
        #print "Files = ",
        #print files
        listing = list_path(connection, path)
        #print "List path = "
        #print listing
        files = files + listing
        #print "Files = ",
        #print files
        #files.update();
    #print files
    
    content = []
    for filename in files:
        output = read_file(connection, filename)
        output = [x.strip() for x in output if x.strip()]
        output = [x for x in output if not normailizing_unicode(x).startswith(';')]
        output = [x for x in output if not normailizing_unicode(x).startswith('\n')]
        content = content + output
    return primary + content 


def read_file(connection, path):
    command = 'cat ' + path
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()
    if list:
        return list
    else:
        return ''

def get_phpversion(connection):
    command = 'php -r "echo phpversion();"'
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()  
    return list[0]

def get_phpini(connection):
    #command = php -r date_default_timezone_set("Africa/Lagos");phpinfo();| grep "Loaded Configuration File"
    command = ["php -r '", "date_default_timezone_set(\"", "Africa/Lagos\"", ");phpinfo();'| grep \"", "Loaded Configuration File\"|awk -F' ' 'NF>0{print $NF}'"]
    command = ''.join(command)
    #print command
    stdin, stdout, stderr = connection.exec_command(command)
    list = stdout.readlines()  
    #print list
    #return list[0]
    path = list[0]
    #print "Path = " + path
    output = read_file(connection, path)
    #print "Output = ",
    #print output
    output = [x for x in output if not normailizing_unicode(x).startswith(';')]
    output = [x for x in output if not normailizing_unicode(x).startswith('\n')]
    output = list2dict(output)
    return output

def put_recommend_value(connection, new, old_key, current_array, recommended_value):
    result = find(old_key, current_array)
    result = get_generator_value(result)
    if result:
        if len(result) == 1:
            old = result[0]
        else:
            old = result
        if old != new:
            recommended_value[old_key] = {'old': old,'new': new}
    else:
        recommended_value[old_key] = {'old': 'Null','new': new}

def list2dict(config):
    result = {}
    for item in config:
        t = result
        temp = item.split('=')
        if len(temp) > 1:
            t = t.update({normailizing_unicode(temp[0]).strip(): normailizing_unicode(temp[1]).strip()})
    return result