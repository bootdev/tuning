#/usr/bin/python
import sys
import argparse

# For mathematical operation
import math

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


    # Session 1, Gathering current configuration values
    #---------------------------------------------------------------------------------------------------------
    ##########################################################################################################
    # CHECKING if connection works
    #print type(connection)
    #stdin, stdout, stderr = connection.exec_command('date')
    #print stdout.readlines()

    ##########################################################################################################
    # GETTING CPU and memory values
    #CPU = check_def.check_CPU(connection)
    #print "CPU Usgae = " + CPU + "%"
    Total_Memory = check_def.check_mem_amount(connection)
    Memory = check_def.check_mem_usage(connection)
    #print "Memory Usage = " + Memory 
    
    ##########################################################################################################
    # READING NGINX CONFIGURATIONS
    nginx_config = check_def.read_nginxconfig(connection)
    #print "Reading Nginx config"
    #print nginx_config
    nginx_included_files = check_def.read_nginx_included_files(connection, nginx_config)
    #error_log_path =  check_def.get_generator_value(check_def.find('error_log', nginx_included_files))
    #print error_log_path
    #print nginx_config
    #print "Sub-Config files content = "
    #print nginx_included_files

    #if nginx_config:
    # 	print "Nginx config is found"
    #else:
    #	print "Nginx config not found"

    ##########################################################################################################
    # Gettting current PHP-fpm process size
    php_size = check_def.check_phpprocess_size(connection)
    #print "PHP Process size = " + str(php_size) + "M"
    
    ##########################################################################################################
    # Read php-fpm conf file
    # First get file name
    phpfpm_conf_file = check_def.get_phpfpm_path(connection)
    #print phpfpm_conf_file
    # Read content
    phpfpm_conf = check_def.get_phpfpm_conf(connection, phpfpm_conf_file)
    #print "php-fpm configuration"
    #print phpfpm_conf

    ##########################################################################################################
    # get php version
    #print check_def.get_phpversion(connection)

    # Session 2, compare current config to recommended values
    #---------------------------------------------------------------------------------------------------------
    ##########################################################################################################
    #print ""
    #print "Recommended value generation"
    # Calculate the recommended NGINX webserver values
    nginx_recommend = {}

    # Check worker processes
    new = check_def.check_CPU_core(connection)
    check_def.put_recommend_value(connection, new, 'worker_processes',nginx_config, nginx_recommend);
    result = check_def.find('events', nginx_config)
    result = check_def.get_generator_value(result)
    # Massaging data
    result = [x for x in result if not isinstance(x, str)]
    if result:
        new = check_def.check_ulimit(connection)
        check_def.put_recommend_value(connection, new, 'worker_connections', result[0], nginx_recommend);
        check_def.put_recommend_value(connection, 'on', 'multi_accept', result[0], nginx_recommend);
        check_def.put_recommend_value(connection, 'epoll', 'use', result[0], nginx_recommend);
    
    #print "Finding keepalive_timeout"
    check_def.put_recommend_value(connection, '60', 'keepalive_timeout',nginx_config, nginx_recommend);
    #print "Finding server_tokens"
    check_def.put_recommend_value(connection, 'off', 'server_tokens',nginx_config, nginx_recommend);
    #print "Finding client_max_body_size"
    check_def.put_recommend_value(connection, '20m', 'client_max_body_size',nginx_config, nginx_recommend);
    #print "Finding client_body_buffer_size"
    check_def.put_recommend_value(connection, '128k', 'client_body_buffer_size',nginx_config, nginx_recommend);
    #print "Getting access_log config"
    check_def.put_recommend_value(connection, 'off', 'access_log',nginx_config, nginx_recommend);
    #print "gzip value "
    check_def.put_recommend_value(connection, 'on' ,'gzip', nginx_config, nginx_recommend);
    check_def.put_recommend_value(connection, 'on' ,'gzip_vary',nginx_config, nginx_recommend);
    check_def.put_recommend_value(connection, '10240' ,'gzip_min_length',nginx_config, nginx_recommend);
    check_def.put_recommend_value(connection, 'expired no-cache no-store private auth' ,'gzip_proxied',nginx_config, nginx_recommend);
    check_def.put_recommend_value(connection, 'text/plain text/css text/xml text/javascript application/x-javascript application/xml' ,'gzip_types',nginx_config, nginx_recommend);
    check_def.put_recommend_value(connection, '"MSIE [1-6]\."' ,'gzip_disable',nginx_config, nginx_recommend);

    #result = check_def.find('access_log',nginx_included_files)
    #print check_def.get_generator_value(result)
    print "----------------------------------------------------"
    print ""
    print "Finalized nginx web server recommendation"
    print nginx_recommend

    #print ""
    #print "Recommended value generation"
    # Calculate the recommended NGINX Site specific values
    print "----------------------------------------------------"
    print ""
    print "Finalized nginx site specific recommendation"
    #print nginx_included_files
    site_recommend = {}
    check_def.put_recommend_value(connection, 'off', 'access_log',nginx_included_files, site_recommend);
    check_def.put_recommend_value(connection, 'Use Socket', 'fastcgi_pass', nginx_included_files, site_recommend);
    #print "----------------------------------------------------"
    print site_recommend

    print "----------------------------------------------------"
    print ""
    print "Recommended value generation"
    # Calculate the recommended php webserver values
    phpfpm_recommend = {}
    print phpfpm_conf
    print "----------------------------------------------------"
    #print ""
    # Transform to dictionary
    phpfpm_conf = check_def.list2dict(phpfpm_conf)

    #print "Total_Memory = " + str(Total_Memory)
    #print "Memory Usage = " + Memory 
    #print "PHP Process size = " + str(php_size) + "M"
    # Save 50MB for other processes
    pm_max_children = int(int(int(Total_Memory) - 50)/php_size)
    #print "pm_max_children = " + str(pm_max_children)
    pm_max_spare_servers = int(math.ceil(float(pm_max_children)/2))
    #print "pm_max_spare_servers = " + str(int(pm_max_spare_servers))
    pm_start_servers = int(math.ceil(float(pm_max_spare_servers) * 0.75))
    #print "pm_start_servers = " + str(pm_start_servers)
    pm_min_spare_servers = int(pm_max_spare_servers / 2)
    #print "pm_min_spare_servers = " + str(pm_min_spare_servers)
    
    check_def.put_recommend_value(connection, 'dynamic', 'pm', phpfpm_conf, phpfpm_recommend)
    check_def.put_recommend_value(connection, str(pm_max_children), 'pm.max_children', phpfpm_conf, phpfpm_recommend)
    check_def.put_recommend_value(connection, str(pm_max_spare_servers), 'pm.max_spare_servers', phpfpm_conf, phpfpm_recommend)
    check_def.put_recommend_value(connection, str(pm_start_servers), 'pm.start_servers', phpfpm_conf, phpfpm_recommend)
    check_def.put_recommend_value(connection, str(pm_min_spare_servers), 'pm.min_spare_servers', phpfpm_conf, phpfpm_recommend)
    check_def.put_recommend_value(connection, str(500), 'pm.max_requests', phpfpm_conf, phpfpm_recommend)
    print "PHP fpm recommendation result"
    print phpfpm_recommend
    print "----------------------------------------------------"
    php_ini = check_def.get_phpini(connection)
    #print php_ini
    
    php_ini_recommend = {}
    check_def.put_recommend_value(connection, '512M', 'memory_limit', php_ini, php_ini_recommend)
    check_def.put_recommend_value(connection, '-1', 'max_input_time', php_ini, php_ini_recommend)
    check_def.put_recommend_value(connection, '300', 'max_execution_time', php_ini, php_ini_recommend)
    check_def.put_recommend_value(connection, '20M', 'upload_max_filesize', php_ini, php_ini_recommend)
    check_def.put_recommend_value(connection, '20M', 'post_max_size', php_ini, php_ini_recommend)
    check_def.put_recommend_value(connection, '3000', 'max_input_vars', php_ini, php_ini_recommend)
    check_def.put_recommend_value(connection, 'On', 'short_open_tag', php_ini, php_ini_recommend)
    check_def.put_recommend_value(connection, 'Off', 'register_globals', php_ini, php_ini_recommend)
    check_def.put_recommend_value(connection, 'Off', 'expose_php', php_ini, php_ini_recommend)
    print "PHP ini recommended values"
    print php_ini_recommend
    # END of program
    print "----------------------------------------------------"
    connection.close()

# Running Main function
if __name__ == '__main__':
    sys.exit(main())