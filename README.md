# Ops

This repo hosts the code and metadata of Ops TM1/PA application

#### Business Functionality


| Functionality | PRD | ERD | User Guide | Any other doc
| ------ | ------ | ---- |  ----|  ----|
| Mobility PL | [Link](https://docs.google.com/document/d/1S9hrLDB53v-fbcsY9oV6O5s8rUZdWmKc79HSQF6xQF4/edit?usp=sharing/) | [Link](https://docs.google.com/document/d/1fZqNv-IPlSBnLEMTtkrM8q50naZ8YAPTU56mCBRjDhI/edit?usp=sharing/) | [Link](https://docs.google.com/document/d/1EdeEAvtgBXAP_FaEBj2Tr7Ohg6fdnGk9GuCmqpcXep4/edit?usp=sharing)|
|  |  |

| ------ | ------ | ---- |  ----|  ----|
| Delivery PL    | [Link](https://docs.google.com/document/d/1Am-FAQJ3KEpbMBTz2D4tk6z9Kkkoe2yfwToXx9x43tw/edit?usp=sharing/) | [Link](https://docs.google.com/document/d/1o7mfOy4CS2iZbriAwAZFOfBtTeqQiX4hv0XUvKW8iqw/edit?usp=sharing/) | [Link](https://docs.google.com/document/d/1xW0eL-fW-m1j7n83spc_grhvVA3wnEgzfiWLpMrT5wg/edit?usp=sharing)        |
|               |  |


#### Ops Home Page - [Eng Wiki](https://engwiki.uberinternal.com/x/TAJ3F/)

#### Product PL Home Page - [Eng Wiki](https://engwiki.uberinternal.com/x/IoIJFg)

#### Product PL SOP's - [Eng Wiki](https://engwiki.uberinternal.com/x/04EJFg)



#### Year End Rollover Guide [Eng Wiki](https://engwiki.uberinternal.com/x/FQOoF)



#### For support
please [email](mailto:finapps-support@uber.com) us or reach out to our [FINAPPS](http://t.uber.com/finapps) JIRA queue

# EPM Code Quality Pre Commit Repo #

## After cloning the repo for first time don't forget to execute below commands ##

### 1). Go to the root folder of the repo and check if "install-pre-commit.sh" file is present
#### ls install-pre-commit.sh

### 2). Make the file "install-pre-commit.sh" executable.
#### chmod +x install-pre-commit.sh

### 3). Execute the file "install-pre-commit.sh".
#### ./install-pre-commit.sh

### 4). copy "install-pre-commit.sh" file to ".git/hooks/post-merge" file.
#### cp install-pre-commit.sh .git/hooks/post-merge

### Now everytime you will do "git pull", installed git post-merge hook will make sure to install/update the pre-commit and you should see below line at the end of the pull request.
< '**pre-commit installed at .git/hooks/pre-commit**' >



<!-- #### Above commands will install pre-commit package in your local machine which will help with code syntax and lint errors #### -->
