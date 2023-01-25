#netmiko is a library used to establish SSH connections to network devices, getpass is a library that prevents passwords from echoing to screen
import netmiko
import getpass

#takes the file name and the credentials for the engineer running the script 
user = input("Enter your username: ")
secret = getpass.getpass("Enter you password: ")
filename = input("Enter the name of the file containing the targets: ")

#opens the file containing the target ip addresses / hostnames and stores the contents in a variable
with open(filename) as file_name:
    targets = file_name.readlines()

#takes the contents in target, removes the whitespace at the end, and adds them to a list
target_list = []
for line in targets:
    target_list.append(line.strip())

#Tries to establish SSH connection to devices in target_list then runs the "show run" command
for target in target_list:
    try:
        net_connect = netmiko.ConnectHandler(
            device_type = "cisco_ios",
            host = target,
            username = user,
            password = secret,
            conn_timeout = 30
        )
        
        show_run = net_connect.send_command("show run")
        
        #Creates a file with a unique name and adds the output of show run to the file.
        new_file = target + "_running_config.txt"
        with open(new_file, 'a') as new:
            for line in show_run:
                new.write(line)
    #IF unable to establish a connection for any reason it will the save the ip address and the error code for further investigation
    except Exception as e:
        error_file = "error_file.txt"
        with open(error_file, 'a') as err:
            err.write(f"{target} {e}\n")

