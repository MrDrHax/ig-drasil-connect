import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('3.85.93.55', username='ec2-user', key_filename='ec2DocDB.pem')

stdin, stdout, stderr = ssh.exec_command('ls')
print(stdout.read().decode())
ssh.close()
