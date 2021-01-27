# Project Goals:

- allow people to get push notifications when vaccine supply is available in their area

### Ideas 

- want to help? <todo add airtable form>


### About the underlying data

- pulled from Texas Division of Emergency Management (TDEM)


### Contributing

##### Feature Branches
<pre>
# creating a new feature branch
$ git branch issue-number-short-description-of-feature
$ git checkout issue-number-short-description-of-feature
$ git push --set-upstream origin issue-number-short-description-of-feature
</pre>

#### Finshing your feature branch

Once you finish your feature branch:

<pre>
# do a final rebase
$ git add .
$ git commit -m "Your commit description"
$ git pull --rebase origin develop
$ git push -f
</pre>

#### Request a pull request to develop

- Log into Github
- Go to "Pull Requests"
- Click "New pull request"
- Choose `develop` as the "base"
- Select your feature branch
- Verify "Able to merge"... if not, please resolve conflicts on your local machine.
- Create pull Request. NOTE: PLEASE BE VERY DESCRIPTIVE OF THE PULL REQUEST
- Submit pull request (You may also select specific reviewers)

#### Switching back to develop and removing the branch from your local

<pre>
# Switch back to the develop branch
$ git checkout develop
$ git pull --rebase origin develop
# you can optionally remove the local feature branch
$ git branch -d issue-number-short-description-of-feature
</pre>