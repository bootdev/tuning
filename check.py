#/usr/bin/python
import sys
import argparse

# Import self defined file
import check_def

def main():
    parser = argparse.ArgumentParser(description='BootDev tunning cli tool',epilog="Copyright 2015 by BootDev\nAll rights reserved.", add_help=False)
    parser.add_argument("-h", "--hostname", help="targte host IP or hostname to run checking")
    parser.add_argument("-u","--user", help="initialize BootDev Commandline tool")
    parser.add_argument("-p","--password", help="initialize BootDev Commandline tool")    
    parser.add_argument("-k","--key", help="initialize BootDev Commandline tool")

    args = parser.parse_args()
    #print args

    if not args.hostname:
        raise ValueError('Hostname is not privided')
        sys.exit(0)
    elif not args.user:
        raise ValueError('Username is not provided')
        sys.exit(0)
    else:
        if (not args.password) and (not args.key):
            raise ValueError('Either key file or password should be provided')
            sys.exit(0)
        elif (args.password) and (args.key):
            raise ValueError('Either Only key file or Only password should be provided')
            sys.exit(0)

    if args.key:
        connection = check_def.connect_key(args.hostname, args.user, args.key)
    elif args.password:
        connection = check_def.connect_password(args.hostname, args.user, args.password)

    #print type(connection)
    #stdin, stdout, stderr = connection.exec_command('date')
    #print stdout.readlines()

    #CPU = check_def.check_CPU(connection)
    #print "CPU Usgae = " + CPU + "%"
    #Memory = check_def.check_mem(connection)
    #print "Memory Usage = " + Memory 
    
    # READING NGINX CONFIGURATIONS
    nginx_config = check_def.read_nginxconfig(connection)
    #print nginx_config
    nginx_included_files = check_def.read_nginx_included_files(connection, nginx_config)
    #error_log_path =  check_def.get_generator_value(check_def.find('error_log', nginx_included_files))
    #print error_log_path

    if nginx_config:
    	print "Nginx config is found"
    else:
    	print "Nginx config not found"
    #php_size = check_def.check_phpprocess_size(connection)
    #print "PHP Process size = " + str(php_size) + "M"
    connection.close()

# Running Main function
if __name__ == '__main__':
    sys.exit(main())