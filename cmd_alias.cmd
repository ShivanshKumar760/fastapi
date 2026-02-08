@REM git aliases
doskey init=git init
doskey add=git add $*
doskey commit=git commit -m "$*"
doskey status=git status
doskey log=git log
doskey branch=git branch
doskey checkout=git checkout $*
doskey merge=git merge $*
doskey push=git push
doskey pull=git pull
doskey stash=git stash
doskey stashpop=git stash pop

@REM gh (GitHub CLI) aliases
doskey ghpr=gh pr $*
doskey ghprcreate=gh pr create $*
doskey repo=gh repo create --public $*

@REM git remote
doskey origin=git remote add origin $*
