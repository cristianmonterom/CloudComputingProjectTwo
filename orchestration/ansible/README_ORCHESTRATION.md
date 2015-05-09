**To ping every host stored in Hosts file

ansible all -i hosts -m ping

execute a command in VM that belongs to test group
ansible test -a "lsb_release -a" -i hosts

how to execute playbooks
ansible-playbook -i hosts test.yml

ansible-playbook -i hosts ansible-instance.yml