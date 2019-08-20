# INFO 3606 Cloud Computing Project
# STAIRS

Sales Trends Analysis Illustration and Recommendation Software (STAIRS) is a business analytic software as a service (SaaS) that allows organizations to graphically visualize their data in order to see growth and trends of their products based on their sales data over a past time-period.

## Getting Started

To set up this application, you need to download the file folder from above or you can run the following command in your terminal.

```
$ git clone https://github.com/Shahanaz-Alex/CCProject.git
```
If you have downloaded the file from your browser, be sure to unzip it.

### Prerequisites

1. Amazon Web Services

2. Git

To install, visit https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.

3. Virtual Environments

To install, visit https://docs.python-guide.org/dev/virtualenvs/.

4. MySQL

To install, in terminal run the command: 

```
$ sudo apt install mysql-client-core-5.7
```

### Installation

#### To deploy the CloudFormation Stack:

1. Open the terminal and navigate to the folder `CCProject`.
2. Run the following command to create and run a virtual environment:

```
$ python3 -m venv venv && . venv/bin/activate 
```

3. Run these commands to deploy the stack:

```
$ chmod +x create.sh
$ ./create.sh
```

N.B. If that does not work, open the file `create.sh`, copy its contents and paste it into the terminal window, then press Enter to run.

You should see a `StackId` returned to you. This means the creation has initiated.

### Deploy Docker Application to CloudFormation Stack

1. Visit Amazon's console at: https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks?filter=active.

2. Wait until the status of `group1Project` says "CREATE_COMPLETE".

3. Click on the stack and then `Resources`. Navigate to `DatabaseInstance` and click on the highlighted ID.

4. Scroll to the section `Connect` and copy the Endpoint address ending in "us-east-1.rds.amazonaws.com".

5. In the file folder, click on the `app` folder.

6. Open `docker-compose.yml` and paste the Endpoint information into the "DB_HOST" field, replacing the section `<Replace this with the endpoint string>` then save the file.

9. Navigate into the `app` folder via the terminal.

7. Copy the following command into terminal and replace the `<DB Instance endpoint>` section with the previously copied Endpoint from step 4 then run the command.
```
$ mysql -h <DB Instance endpoint> -P 3306 -u stairs1 -ppassword123 stairsdb < create_tables.sql
```

You should receive a Warming message.

8. Copy the following command into terminal but do not run. You will need to replace the `<EC2 IPv4 Public IP>` section with an IP address retrieved in the other steps.

```
$ sudo docker-compose -H tcp://<EC2 IPv4 Public IP>:2375 -f docker-compose.yml up -d
```

9. Return to the AWS Console and again, under Resources, navigate to `EC2Instance` and click on the highlighted ID.

10. Under `Description`, copy the IPv4 Public IP and paste it into the section to be replaced from the previous command in Step 8. Now run the command.

11. Visit the previous webpage under the `EC2 Management Console` and copy the link under `Public DNS (IPv4)"

12. Paste the link into your browser and voila! You should see the site appear.

### Terminate CloudFormation Stack/Web Application

1. In the terminal, run the following commands to delete the stack:

```
$ cd ..
$ chmod +x delete.sh
$ ./delete.sh
```
