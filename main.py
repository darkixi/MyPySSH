import paramiko
import time
import csv
import os
import sys

def GetConnectionInfo(inputcsv, userinputcommand):
    with open(inputcsv, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            command = userinputcommand + '\n'
            print "Connecting to %s" %  (row['ip'])
            remote_conn_pre = paramiko.SSHClient()
            remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if row['jumpbox'] == '':
                pass
            else:
                JumpBoxConnect(row['jumpbox'])
                
            try:
                remote_conn_pre.connect(row['ip'], username=row['username'], password=row['password'])
                paramiko.ssh_exception.AuthenticationException
                print "SSH Authenticated!!"

                remote_conn = remote_conn_pre.invoke_shell()
                time.sleep(1)
                nulloutput = remote_conn.recv(50000)
                remote_conn.send('\n')
                time.sleep(1)
                prompt = str(remote_conn.recv(50000)).strip()
                remote_conn.send(command)
                time.sleep(1)
                rawcommandresult = str(remote_conn.recv(50000))
                commandresult = rawcommandresult.replace(prompt, '').replace(userinputcommand, '').strip()
                print '*' * 50
                print commandresult
                print '\n'
                print '*' * 50
                print row['ip'] + " Done!"

                with open('ConnectionInfo_Output.csv', 'ab') as out:
                    writer = csv.writer(out)
                    inputtime = TimeStamp()
                    command = command.strip()
                    writer.writerow([row['ip']] + [command] + [commandresult] + [inputtime])
                    print '*' * 50
                    print "Data successfully saved!!"
                    print '\n'
                    print '\n'

            except:
                print "Connection Failed"
                print "Creating error log"
                commandresult = "SSH Fayeahiled"
                with open('errorlog.csv', 'ab') as e:
                    writer = csv.writer(e)
                    inputtime = TimeStamp()
                    command = command.strip()
                    writer.writerow([row['ip']] + [command] + [commandresult] + [inputtime])
                    
def JumpBoxConnect(jumpboxip):
    username = raw_input('Username: >> ')
    password = raw_input('Password: >> ')
    try:
        remote_conn.send("ssh %s@%s" % (username, jumpboxip) + '\n')
        remote_conn.send(password + '\n')
        time.sleep(1)
    except:
        sys.exit("Connection Failed")

def TimeStamp(epoch=None):
    if epoch == None:
        localTime = time.localtime()
    else:
        localTime = time.localtime(epoch)
    return '%04d/%02d/%02d %02d:%02d' % localTime[0:5]

def CheckFiles(check_file):
    if os.path.isfile(check_file):
        pass
    else:
        with open(check_file, 'ab') as headers:
            writer = csv.writer(headers)
            writer.writerow(['ip', 'command', 'commandresult', 'timestamp'])

if __name__ == "__main__":
    CheckFiles('ConnectionInfo_Output.csv')
    CheckFiles('ErrorLog.csv')
    GetConnectionInfo(raw_input("Enter Input File: "), raw_input("Enter commands: "))


