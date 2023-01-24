#imports the python library necessary for establishing SSH connections
import netmiko

#takes the file name and the credentials for the engineer running the script 
user = input("Enter your elevated username: ")
secret = input("Enter your elveated password: ")
filename = input("Enter the name of the file containing the targets: ")

#opens the file containing the target ip addresses / hostnames and stores the contents in a variable
with open(filename) as file_name:
    targets = file_name.readlines()

#takes the contents in target, removes the extra text at the end, and adds them to a list
target_list = []
for line in targets:
    target_list.append(line.strip())

#established the ssh connection to each device in the target list and runs the show commands. If any error occurs, the ip address is logged
for target in target_list:
    try:
        net_connect = netmiko.ConnectHandler(
            device_type = "cisco_ios",
            host = target,
            username = user,
            password = secret,
        )
        cdp_neighbors = net_connect.send_command("show cdp neighbors")
        interface_descriptions = net_connect.send_command("show int desc")
        ip_int_brief = net_connect.send_command("show ip int brief")
        
        #Creates a file with a unique name and add the contents to the file.
        new_file = target + "output.txt"
        with open(new_file, 'a') as new:
            for line in cdp_neighbors:
                new.write(line)
            for line in interface_descriptions:
                new.write(line)
            for line in ip_int_brief:
                new.write(line)
    except Exception:
        error_file = "error_file.txt"
        with open(error_file, 'a') as err:
            err.write(f"{target}\n")

