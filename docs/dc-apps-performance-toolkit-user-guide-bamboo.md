---
title: "Data Center App Performance Toolkit User Guide For Bamboo"
platform: platform
product: marketplace
category: devguide
subcategory: build
date: "2025-04-22"
---
# Data Center App Performance Toolkit User Guide For Bamboo

This document walks you through the process of testing your app on Bamboo using the Data Center App Performance Toolkit. 
These instructions focus on producing the required 
[performance and scale benchmarks for your Data Center app](/platform/marketplace/dc-apps-performance-and-scale-testing/).

In this document, we cover the use of the Data Center App Performance Toolkit on Enterprise-scale environment.

**Enterprise-scale environment**: Bamboo Data Center environment used to generate Data Center App Performance Toolkit 
test results for the Marketplace approval process. Preferably, use the below recommended parameters.

1. [Set up an enterprise-scale environment Bamboo Data Center on AWS](#instancesetup).
2. [App-specific actions development](#appspecificaction).   
3. [Setting up load configuration for Enterprise-scale runs](#loadconfiguration).
4. [Running the test scenarios from execution environment against enterprise-scale Bamboo Data Center](#testscenario).

---

## <a id="instancesetup"></a>1. Set up an enterprise-scale environment Bamboo Data Center on k8s

#### EC2 CPU Limit
{{% warning %}}
The installation of DC environment and execution pod requires at least **24** vCPU Cores.
Newly created AWS account often has vCPU limit set to low numbers like 5 vCPU per region.
Check your account current vCPU limit for On-Demand Standard instances by visiting [AWS Service Quotas](https://console.aws.amazon.com/servicequotas/home/services/ec2/quotas/L-1216C47A?region=us-east-2) page.
**Applied quota value** is the current CPU limit in the specific region.

Make that current region limit is large enough to deploy new cluster.
The limit can be increased by using **Request increase at account-level** button: choose a region, set a quota value which equals a required number of CPU Cores for the installation and press **Request** button.
Recommended limit is 30.
{{% /warning %}}

#### Setup Bamboo Data Center with an enterprise-scale dataset on k8s

Below process describes how to install Bamboo DC with an enterprise-scale dataset included. This configuration was created
specifically for performance testing during the DC app review process.

1. Create Access keys for AWS CLI:
   {{% warning %}}
   Do not use `root` user credentials for cluster creation.

   **Option 1** (simple): create admin user with `AdministratorAccess` permissions.

   **Option 2** (complex): create granular permission policies with  [policy1](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy1.json) and [policy2](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy2.json).

   The specific configuration relies on how you manage permissions within AWS.
   {{% /warning %}}

   **Example Option 1** with Admin user:
   1. Go to AWS Console -> IAM service -> Users
   2. Create new user -> attach policies directly -> `AdministratorAccess`
   3. Open newly created user -> Security credentials tab -> Access keys -> Create access key -> Command Line Interface (CLI) -> Create access key
   4. Use `Access key` and `Secret access key` in [aws_envs](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/aws_envs) file

   **Example Option 2** with granular Policies:
   1. Go to AWS Console -> IAM service -> Policies
   2. Create `policy1` with json content of the [policy1](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy1.json) file
      {{% warning %}}
      **Important**: change all occurrences of `123456789012` to your real AWS Account ID.
      {{% /warning %}}
   3. Create `policy2` with json content of the [policy2](https://raw.githubusercontent.com/atlassian-labs/data-center-terraform/main/permissions/policy2.json) file
      {{% warning %}}
      **Important**: change all occurrences of `123456789012` to your real AWS Account ID.
      {{% /warning %}}
   4. Go to User -> Create user -> Attach policies directly -> Attach `policy1` and `policy2`-> Click on Create user button
   5. Open newly created user -> Security credentials tab -> Access keys -> Create access key -> Command Line Interface (CLI) -> Create access key
   6. Use `Access key` and `Secret access key` in [aws_envs](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/aws_envs) file
2. Clone [Data Center App Performance Toolkit](https://github.com/atlassian/dc-app-performance-toolkit) locally.
   {{% warning %}}
   For annual review, always get the latest version of the DCAPT code from the master branch.

   DCAPT supported versions: three latest minor version [releases](https://github.com/atlassian/dc-app-performance-toolkit/releases).
   {{% /warning %}}
3. Navigate to `dc-app-performance-toolkit/app/util/k8s` folder.
4. Set AWS access keys created in step1 in `aws_envs` file:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN` (only for temporary creds)
5. Set **required** variables in `dcapt.tfvars` file:
   - `environment_name` - any name for you environment, e.g. `dcapt-bamboo`
   - `products` - `bamboo`
   - `bamboo_license` - one-liner of valid bamboo license without spaces and new line symbols
   - `region` - **Do not change default region (`us-east-2`). If specific region is required, contact support.**

   {{% note %}}
   New trial license could be generated on [my atlassian](https://my.atlassian.com/license/evaluation).
   Use `BX02-9YO1-IN86-LO5G` Server ID for generation.
   {{% /note %}}

6. From local terminal (Git Bash for Windows users) start the installation:

   ``` bash
   docker run --pull=always --env-file aws_envs \
   -v "/$PWD/dcapt.tfvars:/data-center-terraform/conf.tfvars" \
   -v "/$PWD/dcapt-snapshots.json:/data-center-terraform/dcapt-snapshots.json" \
   -v "/$PWD/logs:/data-center-terraform/logs" \
   -it atlassianlabs/terraform:2.9.8 ./install.sh -c conf.tfvars
   ```
7. Copy product URL from the console output. Product url should look like `http://a1234-54321.us-east-2.elb.amazonaws.com/bamboo`.
8. Wait for all remote agents to be started and connected. It can take up to 10 minutes. Agents can be checked in `Settings` > `Agents`.

{{% note %}}
All the datasets use the standard `admin`/`admin` credentials.
{{% /note %}}

---

Data dimensions and values for default enterprise-scale dataset uploaded are listed and described in the following table.

| Data dimensions | Value for an enterprise-scale dataset |
| --------------- | ------------------------------------- |
| Users | 2000 |
| Projects | 100 |
| Plans | 2000 |
| Remote agents | 50 |

---

{{% note %}}
You are responsible for the cost of the AWS services running during the reference deployment. For more information, 
go to [aws.amazon.com/pricing](https://aws.amazon.com/ec2/pricing/).
{{% /note %}}

To reduce costs, we recommend you to keep your deployment up and running only during the performance runs.

---

## <a id="appspecificaction"></a>2. App-specific actions development

Data Center App Performance Toolkit has its own set of default test actions: 
 - JMeter: for load at scale generation
 - Selenium: for UI timings measuring 
 - Locust: for defined parallel Bamboo plans execution     

**App-specific action** - action (performance test) you have to develop to cover main use cases of your application. 
Performance test should focus on the common usage of your application and not to cover all possible functionality of 
your app. For example, application setup screen or other one-time use cases are out of scope of performance testing.

### App specific dataset extension
If your app introduces new functionality for Bamboo entities, for example new task, it is important to extend base 
dataset with your app specific functionality.

1. Follow installation instructions described in [bamboo dataset generator README.md](https://raw.githubusercontent.com/atlassian/dc-app-performance-toolkit/master/app/util/bamboo/bamboo_dataset_generator/README.md)
1. Open `app/util/bamboo/bamboo_dataset_generator/src/main/java/bamboogenerator/Main.java` and set:
   - `BAMBOO_SERVER_URL`: url of Bamboo stack
   - `ADMIN_USER_NAME`: username of admin user (default is `admin`)
1. Login as `ADMIN_USER_NAME`, go to **Profile &gt; Personal access tokens** and create a new token with the same 
permissions as admin user.
1. Run following command:
    ``` bash
    export BAMBOO_TOKEN=newly_generarted_token  # for MacOS and Linux
    ```
    or
    ``` bash
    set BAMBOO_TOKEN=newly_generarted_token     # for Windows
    ```
1. Open `app/util/bamboo/bamboo_dataset_generator/src/main/java/bamboogenerator/service/generator/plan/PlanGenerator.java` 
file and modify plan template according to your app. e.g. add new task.
1. Navigate to `app/util/bamboo/bamboo_dataset_generator` and start generation:
    ``` bash
    ./run.sh     # for MacOS and Linux
    ```
    or
    ``` bash
    run          # for Windows
    ```
1. Login into Bamboo UI and make sure that plan configurations were updated.
1. Default duration of the plan is 60 seconds. Measure plan duration with new app-specific functionality and modify
   `default_dataset_plan_duration` value accordingly in `bamboo.yml` file.

   For example, if plan duration with app-specific task became 70 seconds, than `default_dataset_plan_duration`
   should be set to 70 seconds in `bamboo.yml` file.

### Example of app-specific Selenium action development
For example, you develop an app that adds some additional UI elements to view plan summary page. 
In this case, you should develop Selenium app-specific action:

1. Extend example of app-specific action in `dc-app-performance-toolkit/app/extension/bamboo/extension_ui.py`.  
[Code example.](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/extension/bamboo/extension_ui.py)
So, our test has to open plan summary page and measure time to load of this new app-specific element on the page.
1. If you need to run `app_specific_action` as specific user uncomment `app_specific_user_login` function in 
   [code example](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/extension/bamboo/extension_ui.py). 
   Note, that in this case `test_1_selenium_custom_action` should follow just before `test_2_selenium_z_log_out` action.
1. In `dc-app-performance-toolkit/app/selenium_ui/bamboo_ui.py`, review and uncomment the following block of code to make newly created app-specific actions executed:

   ``` python
   # def test_1_selenium_custom_action(webdriver, datasets, screen_shots):
   #     app_specific_action(webdriver, datasets)
   ```
1. Run toolkit with `bzt bamboo.yml` command to ensure that all Selenium actions including `app_specific_action` are successful.

### Example of JMeter app-specific action development

1. Check that `bamboo.yml` file has correct settings of `application_hostname`, `application_protocol`, `application_port`, `application_postfix`, etc.
1. Set desired execution percentage for `standalone_extension`. Default value is `0`, which means that `standalone_extension` action will not be executed. 
For example, for app-specific action development you could set percentage of `standalone_extension` to 100 and for all 
   other actions to 0 - this way only `login_and_view_all_builds` and `standalone_extension` actions would be executed.
1.Navigate to `dc-app-performance-toolkit/app` folder and follow [start JMeter UI README](https://github.com/atlassian/dc-app-performance-toolkit/tree/master/app/util/jmeter#start-jmeter-ui):
    
    ```python util/jmeter/start_jmeter_ui.py --app bamboo```
    
1. Open `Bamboo` thread group > `actions per login` and navigate to `standalone_extension`
1. Review existing stabs of `jmeter_app_specific_action`: 
   - example GET request
   - example POST request
   - example extraction of variables from the response - `app_id` and `app_token`
   - example assertions of GET and POST requests
1. Modify examples or add new controllers according to your app main use case.
1. Right-click on `View Results Tree` and enable this controller.
1. Click **Start** button and make sure that `login_and_view_dashboard` and `standalone_extension` are executed.
1. Right-click on `View Results Tree` and disable this controller. It is important to disable `View Results Tree` controller before full-scale results generation.
1. Click **Save** button.
1. To make `standalone_extension` executable during toolkit run edit `dc-app-performance-toolkit/app/bamboo.yml` and set 
   execution percentage of `standalone_extension` accordingly to your use case frequency.
1. App-specific tests could be run (if needed) as a specific user. In the `standalone_extension` uncomment 
   `login_as_specific_user` controller. Navigate to the `username:password` config element and update values for 
   `app_specific_username` and `app_specific_password` names with your specific user credentials. Also make sure that 
   you located your app-specific tests between `login_as_specific_user` and 
   `login_as_default_user_if_specific_user_was_loggedin` controllers.
1. Run toolkit to ensure that all JMeter actions including `standalone_extension` are successful.

###  Example of Locust app-specific action development

1. Extend example of app-specific action in `dc-app-performance-toolkit/app/extension/bamboo/extension_locust.py`, 
so that test will call the endpoint with GET request, parse response use these data to call another endpoint with POST request and measure response time.  
[Code example.](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/extension/bamboo/extension_locust.py)
2. In `dc-app-performance-toolkit/app/bamboo.yml` uncomment in `execution` section `scenario: locust_app_specific` to enable locust app-specific test execution.
3. In `dc-app-performance-toolkit/app/bamboo.yml` set `standalone_extension_locust` to `1` - app-specific action will be executed by every virtual user 
of `locust_app_specific` scenario. Default value is `0`, which means that `standalone_extension_locust` action will not be executed. 
4. App-specific tests could be run (if needed) as a specific user. Use `@run_as_specific_user(username='specific_user_username', password='specific_user_password')` decorator for that.
5. Run toolkit with `bzt bamboo.yml` command to ensure that all Locust actions including `locust_app_specific_action` are successful. 
Note, that `locust_app_specific_action` action execution will start in some time full after ramp period up is finished (in 5-6 min).

---

## <a id="loadconfiguration"></a>3. Setting up load configuration for Enterprise-scale runs

Default TerraForm deployment [configuration](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/dcapt.tfvars)
already has a dedicated execution environment pod to run tests from. For more details see `Execution Environment Settings` section in `dcapt.tfvars` file.

1. Check the `bamboo.yml` configuration file. If load configuration settings were changed for dev runs, make sure parameters
   were changed back to the defaults:

   ``` yaml
    application_hostname: bamboo_host_name or public_ip   # Bamboo DC hostname without protocol and port e.g. test-bamboo.atlassian.com or localhost
    application_protocol: http          # http or https
    application_port: 80                # 80, 443, 8080, 8085, etc
    secure: True                        # Set False to allow insecure connections, e.g. when using self-signed SSL certificate
    application_postfix: /bamboo        # e.g. /babmoo in case of url like http://localhost:8085/bamboo
    admin_login: admin
    admin_password: admin
    load_executor: jmeter            
    concurrency: 200                    # number of concurrent threads to authenticate random users
    test_duration: 45m
    ramp-up: 3m
    total_actions_per_hour: 2000        # number of total JMeter actions per hour
    number_of_agents: 50                # number of available remote agents
    parallel_plans_count: 40            # number of parallel plans execution
    start_plan_timeout: 60              # maximum timeout of plan to start
    default_dataset_plan_duration: 60   # expected plan execution duration
   ```

You'll need to run the toolkit for each [test scenario](#testscenario) in the next section.

---

## <a id="testscenario"></a>4. Running the test scenarios from execution environment against enterprise-scale Bamboo Data Center

#### <a id="testscenario1"></a> Bamboo performance regression

This scenario helps to identify basic performance issues.

##### <a id="regressionrun1"></a> Run 1 (~50 min)

To receive performance baseline results **without** an app installed and **without** app-specific actions (use code from `master` branch):

1. Before run:
   * Make sure `bamboo.yml` and toolkit code base has default configuration from the `master` branch.
   * Check load configuration parameters needed for enterprise-scale run: [Setting up load configuration for Enterprise-scale runs](#loadconfiguration).
   * Check correctness of `application_hostname`, `application_protocol`, `application_port` and `application_postfix` in .yml file.
   * `standalone_extension` set to 0. App-specific actions are not needed for Run1 and Run2.
   * `standalone_extension_locust` set to 0.
   * AWS access keys set in `./dc-app-performance-toolkit/app/util/k8s/aws_envs` file:
      - `AWS_ACCESS_KEY_ID`
      - `AWS_SECRET_ACCESS_KEY`
      - `AWS_SESSION_TOKEN` (only for temporary creds)
1. Navigate to `dc-app-performance-toolkit` folder and start tests execution:
    ``` bash
    export ENVIRONMENT_NAME=your_environment_name
    ```

    ``` bash
    docker run --pull=always --env-file ./app/util/k8s/aws_envs \
    -e REGION=us-east-2 \
    -e ENVIRONMENT_NAME=$ENVIRONMENT_NAME \
    -v "/$PWD:/data-center-terraform/dc-app-performance-toolkit" \
    -v "/$PWD/app/util/k8s/bzt_on_pod.sh:/data-center-terraform/bzt_on_pod.sh" \
    -it atlassianlabs/terraform:2.9.8 bash bzt_on_pod.sh bamboo.yml
    ```
1. View the following main results of the run in the `dc-app-performance-toolkit/app/results/bamboo/YY-MM-DD-hh-mm-ss` folder:
    - `results_summary.log`: detailed run summary
    - `results.csv`: aggregated .csv file with all actions and timings
    - `bzt.log`: logs of the Taurus tool execution
    - `jmeter.*`: logs of the JMeter tool execution
    - `locust.*`: logs of the Locust tool execution

{{% note %}}
Review `results_summary.log` file under artifacts dir location. Make sure that overall status is `OK` before moving to 
the next steps. For an enterprise-scale environment run, the acceptable success rate for actions is 95% and above.
{{% /note %}}

##### <a id="regressionrun2"></a> Run 2 (~50 min)

To receive performance results with an app installed (still use master branch):

1. Install the app you want to test.
1. Setup app license.
1. Navigate to `dc-app-performance-toolkit` folder and start tests execution:
    ``` bash
    export ENVIRONMENT_NAME=your_environment_name
    ```

    ``` bash
    docker run --pull=always --env-file ./app/util/k8s/aws_envs \
    -e REGION=us-east-2 \
    -e ENVIRONMENT_NAME=$ENVIRONMENT_NAME \
    -v "/$PWD:/data-center-terraform/dc-app-performance-toolkit" \
    -v "/$PWD/app/util/k8s/bzt_on_pod.sh:/data-center-terraform/bzt_on_pod.sh" \
    -it atlassianlabs/terraform:2.9.8 bash bzt_on_pod.sh bamboo.yml
    ```

{{% note %}}
Review `results_summary.log` file under artifacts dir location. Make sure that overall status is `OK` before moving to 
the next steps. For an enterprise-scale environment run, the acceptable success rate for actions is 95% and above.
{{% /note %}}

##### <a id="run3"></a> Run 3 (~50 min)

To receive results for Bamboo DC **with app** and **with app-specific actions**:

1. Before run:
   * Make sure `bamboo.yml` and toolkit code base has code base with your developed app-specific actions.
   * Check correctness of `application_hostname`, `application_protocol`, `application_port` and `application_postfix` in .yml file.
   * Check load configuration parameters needed for enterprise-scale run: [Setting up load configuration for Enterprise-scale runs](#loadconfiguration).
   * `standalone_extension` set to non 0 and .jmx file has standalone actions implementation in case of JMeter app-specific actions.
   * `standalone_extension_locust` set to 1 and Locust app-specific actions code base applied  in case of Locust app-specific actions.
   * [test_1_selenium_custom_action](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/selenium_ui/bamboo_ui.py#L51-L52) is uncommented and has implementation in case of Selenium app-specific actions.
   * AWS access keys set in `./dc-app-performance-toolkit/app/util/k8s/aws_envs` file:
      - `AWS_ACCESS_KEY_ID`
      - `AWS_SECRET_ACCESS_KEY`
      - `AWS_SESSION_TOKEN` (only for temporary creds)
1. Navigate to `dc-app-performance-toolkit` folder and start tests execution:
    ``` bash
    export ENVIRONMENT_NAME=your_environment_name
    ```

    ``` bash
    docker run --pull=always --env-file ./app/util/k8s/aws_envs \
    -e REGION=us-east-2 \
    -e ENVIRONMENT_NAME=$ENVIRONMENT_NAME \
    -v "/$PWD:/data-center-terraform/dc-app-performance-toolkit" \
    -v "/$PWD/app/util/k8s/bzt_on_pod.sh:/data-center-terraform/bzt_on_pod.sh" \
    -it atlassianlabs/terraform:2.9.8 bash bzt_on_pod.sh bamboo.yml
    ```

{{% note %}}
Review `results_summary.log` file under artifacts dir location. Make sure that overall status is `OK` before moving to 
the next steps. For an enterprise-scale environment run, the acceptable success rate for actions is 95% and above.
{{% /note %}}

##### Generating a Bamboo performance regression report

To generate a performance regression report:  

1. Edit the `./app/reports_generation/bamboo_profile.yml` file:
    - Under `runName: "without app"`, in the `relativePath` key, insert the relative path to results directory of [Run 1](#regressionrun1).
    - Under `runName: "with app"`, in the `relativePath` key, insert the relative path to results directory of [Run 2](#regressionrun2).
    - Under `runName: "with app and app-specific actions"`, in the `relativePath` key, insert the relative path to results directory of [Run 3](#run3).    
1. Navigate locally to `dc-app-performance-toolkit` folder and run the following command from local terminal (Git Bash for Windows users) to generate reports:
    ``` bash
    docker run --pull=always \
    -v "/$PWD:/dc-app-performance-toolkit" \
    --workdir="//dc-app-performance-toolkit/app/reports_generation" \
    --entrypoint="python" \
    -it atlassian/dcapt csv_chart_generator.py bamboo_profile.yml
    ```
1. In the `./app/results/reports/YY-MM-DD-hh-mm-ss` folder, view the `.csv` file (with consolidated scenario results), the `.png` chart file and performance scenario summary report.
   If you see an impact (>20%) on any action timing, we recommend taking a look into the app implementation to understand the root cause of this delta.

{{% warning %}}
It is recommended to terminate an enterprise-scale environment after completing all tests.
Follow [Terminate enterprise-scale environment](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#terminate-enterprise-scale-environment) instructions.
In case of any problems with uninstall use [Force terminate command](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#force-terminate-cluster).
{{% /warning %}}
   
#### Attaching testing results to ECOHELP ticket

{{% warning %}}
Do not forget to attach performance testing results to your ECOHELP ticket.
{{% /warning %}}

1. Make sure you have report folder with bamboo performance scenario results. 
   Folder should have `profile.csv`, `profile.png`, `profile_summary.log` and profile run result archives. Archives 
   should contain all raw data created during the run: `bzt.log`, selenium/jmeter/locust logs, .csv and .yml files, etc.
2. Attach report folder to your ECOHELP ticket.


## <a id="support"></a> Support
If the installation script fails on installing Helm release or any other reason, collect the logs, zip and share to [community Slack](http://bit.ly/dcapt_slack) **#data-center-app-performance-toolkit** channel.
For instructions on how to collect detailed logs, see [Collect detailed k8s logs](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#collect-detailed-k8s-logs).
For failed cluster uninstall use [Force terminate command](https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/util/k8s/README.MD#force-terminate-cluster).

In case of any technical questions or issues with DC Apps Performance Toolkit, contact us for support in the [community Slack](http://bit.ly/dcapt_slack) **#data-center-app-performance-toolkit** channel.
