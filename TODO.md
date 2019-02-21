Copying sshkey for root user:

```
#!/usr/bin/expect -f
spawn ssh-copy-id cloudran@$argv
expect "password:"
send "cloudran\n"
expect eof
```
Then, 
```
ssh -t cloudran@argv "sudo mkdir /root/.ssh" 
ssh -t cloudran@argv "sudo cp ~/.ssh/authorized_keys /root/.ssh" 
```