import git
import sys
import psutil
import subprocess
from nextcord.ext import commands


class bot_reload:
    def setup(self,bot):
        if self.type == 'git':
            bot.add_cog(self.restarts(bot,self))
        else:
            bot.add_cog(self.restart(bot,self))
    
    
    def __init__(self,type="git",code_editor="vscode", file=__file__,gitlink=None):
        self.type = type
        if type=="git":
            self.git(gitlink,code_editor, file)
        else:
            self.normal(code_editor, file)
        

    
    
    def normal(self,code_editor,file):
        self.code_editor = code_editor
        self.restart_file = file
       
    
    def git(self,gitLink,code_editor,file):
        self.repo_link = gitLink
        self.code_editor = code_editor
        self.restart_file = file
        try:
            self.repo = git.Repo(gitLink)
        except git.InvalidGitRepositoryError:
            sys.exit(f"Resp link : {gitLink} is not a valid resp")







    
    
    class restarts(commands.cog,name="restarts"):
        def __init__(self,bot,self2):
            self.self2 = self2
            self.code_editor = self.self2.code_editor
            self.bot = bot
        @commands.command()
        async def reload(self,ctx,data:bool):
            await ctx.send('downloading Git Resp')
            ret = await git.pull(self.self2.repo_link)
            code_editor_open = "someProgram" in (p.name() for p in psutil.process_iter())
            if not code_editor_open:
                if data:        
                    await ctx.send(f'downloading done : Data : {ret}')
                else:
                    await ctx.senf(f'downloading done : Data : {"NULL"}')
                    spawn_program_and_die(['python3',str(self.self2.restart_file)])
            else:
                ctx.send("dev env Open , refuseing to liveswap From GH")
    
    
    
    class restart(commands.cog,name="restarts"):
        def __init__(self,bot,self2):
            self.self2 = self2
            self.code_editor = self.self2.code_editor
            self.bot = bot
        
        @commands.command()
        async def reload(self,ctx,data):
            ctx.send('reloading')
            spawn_program_and_die(['python3',str(self.self2.restart_file)])
            
                








def spawn_program_and_die(program, exit_code=0):
    """
    Start an external program and exit the script 
    with the specified return code.

    Takes the parameter program, which is a list 
    that corresponds to the argv of your command.
    """
    # Start the external program
    subprocess.Popen(program)
    # We have started the program, and can suspend this interpreter
    sys.exit(exit_code)






if __name__ == "__main__":
    sys.exit(1)