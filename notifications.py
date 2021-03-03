#!/usr/bin/env python3
#
"""Python module for making a cron job to send out notifications to a phone number or email at a specified time. 

This isn't quite close to being done, I need to finish initiating an 
actual job from the program. and I need to test it over the course of a few days. 

The msmtp command line tool along with an email configured for sending smtp emails with msmtp
from the command line already needs to be configured to utilize this script. I recommend
learning how to use that as well as how cronjobs work in general before using this. 

Cron job resource link: https://code.tutsplus.com/tutorials/managing-cron-jobs-using-python--cms-28231
msmtp tutorial link: https://wiki.archlinux.org/index.php/Msmtp
"""
import os
import json
import time

class CronJob:
    """Cron job parent class defining methods for 

       initializing and deploying general cron jobs. """
    def __init__(self):
        self.crontabl = os.system("crontab -l")
        self.id = str(int(time.time()))

    def schedule_job(self, minute="*", hour="*", day="*", month="*", weekday="*"):
        """Cronjobs require time to be formatted in a specific way. 

                *    *   *    *      *
               min hour day month weekday 

            This makes records the schedule for a job. 
        """
        month_end = {"*": "*", "1": 31, "2": 28, "3": 31, 
                     "4": 30, "5": 31, "6": 30, "7": 31, 
                     "8": 31, "9": 30, "10": 31, "11": 30, "21": 31} 
        for i in [minute, hour, day, month, weekday]: 
            if i.isnumeric() == False and i != "*":
                raise ValueError("Invalid time field entered.")

        for t in [minute, hour]:
            if t != "*":
                 if int(t) < 0 or 59 < int(t): 
                    raise ValueError("""Invalid time field entered. 
                                \r\t    Values for minute and hour should be between 0 and 59.""")
        # Errors regarding leap years and day fields
        # with a glob month field are handled by the system
        if day != "*":
            if 30 < int(day) or int(day) < 0:
                raise ValueError("""Invalid day field entered. 
                            \r\t    day should be between 1 and 31.""")
                
        if month not in month_end.keys():
            raise ValueError("Invalid month entered. ")

        if month != "*" and day != "*":
            for m, d in month_end.items():
                if month == m and int(d) < int(day):
                    raise ValueError("Invalid end of month entered. ")

        if weekday != "*":
            if int(weekday) < 0 or 7 < int(weekday): 
                raise ValueError("Invalid weekday entered. ")

        schedule = f"{minute} {hour} {day} {month} {weekday}"   
        self.schedule = schedule 
        return self.schedule

    def set_command(self, command: str):
        """Still not sure on how this will work"""
        self.crontable = self.crontabl + f"\n{command}"
        src = f"command-{self.id}.sh"
        os.system(f"touch {src}")
        os.system(f"chmod +x {src}")
        os.system(f"echo '{self.schedule} {self.crontabl}' > {src}")
        pass 


class User:
    """User parent class to store and user information, including: 

    smtp information, emails, phone numbers, etc. """
    def __init__(self, email, destination):
            self.email = email
            self.destination = destination
            self.user_info = {"destination": self.destination, 
                              "email": self.email}
    
    def save_user_info(self) -> dict:
        """Saves the provided user information to a json file"""
        with open("user_info.json", "w") as info:
            json.dump(self.user_info, info, indent=4)
    
    def get_user_info(self, print_info=False) -> dict:
        """Returns information about currently saved sender and reciever information"""
        if print_info == True: print(self.user_info)
        else: return self.user_info


class Notification(User, CronJob):
    """Notification class for sending SMS notification messages to user"""

    def __init__(self, email, destination):
        """Constructs based on the number of current active user jobs. """
        super().__init__(email, destination)
        try:
            with open("notification_jobs.json", "r") as jobs:
                self.current_jobs = json.load(jobs)
                self.num_jobs = len(self.current_jobs)
        except:
            self.current_jobs = {}
            self.num_jobs = 0

    def set_notification(self, message, time_fields, recurrance_rate) -> None:
        """Set the user message, recurrance fields and time fields

        and send it into the queue to allow it to be initialized. 
        """
        self.message = message
        self.time_fields = time_fields
        self.recurrance_rate = recurrance_rate      

    def remove_notification(self, message) -> None:
        """Allow a user to delete a current notification."""
        assert 0 < message
        if self.num_jobs == 0:
            print("No jobs to remove. ")
            return
        while True: 
            verify = input("Removing a notification. Continue? (y, n): ")
            if verify == "n":
                print("Canelling removal. ")
                return
            elif verify != "y":
                print("Invalid input. ")
                continue
            else:
                del self.current_jobs["notification to remove"]

    def initialize_text_cron_job(self) -> None:
        """Initilize the notification into the active cron jobs"""
        # Recording the notification as an active job in the script. 
        self.recorded["initialized"] = True
        pass

    def get_current_notifications(self) -> dict:
        return self.recorded

    def get_current_jobs(self, print_jobs=False) -> dict:
        no_jobs = len(self.current_jobs) == 0
        if print_jobs:
            if no_jobs:
                print("No current jobs. ")
            else: 
                print("Active jobs: ")
                for job in self.current_jobs.values():
                    print(f"""\tMessage:\t\t{job[0]}
                        \r\tTime to notify:\t{job[1]}
                        \r\tTimes to repeat:\t{job[2]}
                    """)
        if no_jobs: 
            return "No current jobs. "
        else: 
            return self.current_jobs
        
    def get_num_jobs(self, print_num_jobs=False) -> int:
        if print_num_jobs:
            print(f"Number of active jobs: {len(self.num_jobs)}")
        else: return self.num_jobs
