import os
from urllib import request
import tarfile

class RepoManager:
    local_path = "~/.sword"
    default_repo_server = "ftp.crosswire.org"
    default_repo = "/pub/sword/raw"
    def __init__(self,local_path,default_repo,default_repo_server):
        self.default_repo = default_repo
        self.default_repo_server = default_repo_server
        self.local_path = local_path
    def prep_local_repo(self):
        try:
            os.makedirs(self.local_path)
        except:
            print("Directory exists")
        self.grab_unpack_mod_confs()
    def grab_unpack_mod_confs(self):
        tarfile.open(self.pull_repo_mods_tar()).extractall(os.path.join(self.local_path))
        #tar gunzip bra
    def pull_repo_mods_tar(self):
        return self.pull_ftp_tar("ftp://{}{}/{}".format(self.default_repo_server,self.default_repo,"mods.d.tar.gz"))
    def pull_ftp_tar(self,uri):
        destination = os.path.join(self.local_path,"mods.d.tar.gz")
        print(uri)
        request.urlretrieve(uri, destination)
        return destination
    def grab_mod(self):
        #read mod conf
        #urlpath read ftp path based on mod conf
        #pull each file
        pass


repo = RepoManager("/Users/david/temporary/.sword","/pub/sword/raw","ftp.crosswire.org")
repo.prep_local_repo()