# Python RPA Challenge

### Tasks

1. Go To [IT-Dashboard](https://itdashboard.gov/) and Click "DIVE IN" and it will show agencies and there amount spent
2. The script will scrap agencies with amount and save it into the Excel file
3. The script open one of the agency and it will go to its URL available in the scraped data
4. It will check in the Individual Investments table that if the **UII** contains link it will open that link and download the PDF file associated with **Download Business Case PDF** button into output folder  
5. Can be test on [robocorp](https://cloud.robocorp.com/)
6. All downloaded PDF's and Excel sheets will be land in **output** folder


### Instructions

1. Goto [robocorp](https://cloud.robocorp.com/taskoeneg/task/robots) create a bot
2. Add [this](https://github.com/Us-manArshad/it-dashboard.git) repo link in public GIT
3. Goto [assistants](https://cloud.robocorp.com/taskoeneg/task/assistants) and add new assistant linked with robot that you had registered above. 
4. Download and install desktop app of robocorp assistant from [there](https://cloud.robocorp.com/taskoeneg/task/assistants) by click on **Download Robocorp Assistant App**
5. Run the assistant you had created above
6. Bot will start performing the task as mentioned above
7. Your output data will be saved in output folder. click on output when task finished.

