import os
import shutil
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
            os.makedirs(os.path.join(self.local_path,"mods.d"))
        except:
            print("Directory exists")
        self.grab_unpack_mod_confs(self.default_repo_server, self.default_repo)
    def grab_unpack_mod_confs(self,repo_server,repo):
        repo_path = os.path.join(self.local_path,"Repositories",repo_server,*repo.split('/'))
        print(repo_path)
        os.makedirs(repo_path)
        tarfile.open(self.pull_repo_mods_tar(repo_server,repo)).extractall(repo_path)
        #tar gunzip bra
    def pull_repo_mods_tar(self,repo_server,repo):
        return self.pull_ftp_tar("ftp://{}{}/{}".format(repo_server, repo,"mods.d.tar.gz"))
    def pull_ftp_tar(self,uri):
        destination = os.path.join(self.local_path,"mods.d.tar.gz")
        print(uri)
        request.urlretrieve(uri, destination)
        return destination
    def grab_mod(self, repo_server, repo, modulename):
        path = os.path.join(self.local_path,'mods.d',modulename+'.conf')
        source_path = os.path.join(self.local_path,"Repositories",repo_server,*repo.split('/'),'mods.d',modulename+'.conf')
        module_info = configparser.ConfigParser()
        print(source_path)
        module_info.read(source_path)
        print(module_info)
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
        shutil.copyfile(source_path,path)
        return 0


repo = RepoManager("/Users/david/temporary/.sword","/pub/sword/raw","ftp.crosswire.org")
repo.prep_local_repo()
repo.grab_mod("ftp.crosswire.org","/pub/sword/raw",'drc')