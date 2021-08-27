import os
from urllib import request
import tarfile
import configparser
from ftplib import FTP

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
    def grab_mod(self, modulename):
        path = os.path.join(self.local_path,'mods.d',modulename+'.conf')
        
        module_info = configparser.ConfigParser()
        module_info.read(path)
        module_path = module_info[modulename.upper()]['DataPath']
        
        down_path = os.path.join(self.local_path, module_path)
        os.makedirs(down_path)
        
        url = self.default_repo+'/'+module_path
        
        ftp = FTP(self.default_repo_server)
        ftp.login()
        ftp.cwd("."+url)
        
        files = ftp.nlst()

        for file in files:
            request.urlretrieve("ftp://{}{}/{}".format(self.default_repo_server,url,file),os.path.join(down_path,file))

        return 0


repo = RepoManager("/Users/david/temporary/.sword","/pub/sword/raw","ftp.crosswire.org")
#repo.prep_local_repo()
repo.grab_mod('drc')