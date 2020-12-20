from github import Github
import os, subprocess
import iterm2

# VARIABLES
rootdir = "/users/Vince/Code" # Root directory for github repos
itermcd = 1 # cd into the new repo directory at the end?
github_username = "vinceblake"
github_token = os.environ.get('GITHUB')

# GITHUB AUTHENTICATION
g = Github(github_token)
user = g.get_user()

# METHODS
## Validate inputs
def validate(response):
    if "Y" in response.upper() or response == 1:
        return True
    else:
        return False

## Use iterm2 API to cd into new directory
async def main(connection):
    app = await iterm2.async_get_app(connection)
    term = app.current_terminal_window.current_tab.current_session
    cmd = f'cd {rootdir}/{name};clear\n'
    await term.async_send_text(cmd)    

# MAIN PROCESS
if __name__ == '__main__':
    try:
        os.chdir(rootdir)
        name = ''
        while not name: 
            name = input("Repo Name: ").strip()
        name = name.lower().replace(" ", "-")

        desc = input("\nRepo description (Leave blank for none):\n")
        desc = desc.strip()
        if len(desc) < 1:
            desc = "I couldn't be bothered."
            
        privacy = input("\nMake repo private?\nY/N (or leave blank for 'no'): ")
        privacy = validate(privacy)

        autoinit = input("\nInitialize the repository with a minimal README?\nY/N (or leave blank for 'no'): ")
        autoinit = validate(autoinit)

        gitignore = input("\nUse a .gitignore template?\nSee https://github.com/github/gitignore or leave blank): ")
        gitignore = gitignore.capitalize()

        # Create the repo
        repo = user.create_repo(
            name,
            description = desc,
            private = privacy,
            auto_init = autoinit,
            gitignore_template = gitignore
            )

        # Clone new repo?
        start = input("\nGithub repository created. Ready to go? (Default = Yes)\n")
        start = start.strip()
        if "Y" in start.upper() or len(start.upper()) < 1 or start == 1:
            print()
            clone = f"git@github.com:{github_username}}/{name}.git"
            subprocess.run(["git", "clone", clone])
            if itermcd == 1:
                iterm2.run_until_complete(main)   

    except KeyboardInterrupt:
        print("\n\nIt's treason, then.")
        pass