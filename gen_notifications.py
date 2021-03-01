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
from datetime import datetime

def user_information(saved_info=False, filename=None):
    if saved_info: 
            with open(f"{filename}", "r") as info:
                user_info = json.load(info)
    else:
        destination = input("Phone number or email to recieve notification: ")
        email = input("msmtp email to send notification from: ")
        user_info = {"destination": destination, "email": email}
    return user_info

class User:
    """Notification subclass to generate and deploy the actual cron job"""

    def __init__(self, email, destination):
            self.email = email
            self.destination = destination
            self.user_info = {"destination": self.destination, 
                              "email": self.email}
    
    def save_user_info(self) -> dict:
        """Saves the provided user information to a json file"""
        with open("user_info.json", "w") as info:
            json.dump(user_info, indent=4)
    
    def get_user_info(self, print_info=False) -> dict:
        """Returns information about currently saved sender and reciever information"""
        if print_info == True: print(user_info)
        else: return self.user_info


class Notification(User):
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

    @staticmethod
    def crontab_time_fields() -> dict:
        """Cronjobs require time to be formatted in a specific way. 

                        *    *   *    *      *
                       min hour day month weekday
        
        Weekday will typically default to *
        This funciton verifies user time entry and convert it 
        into the appropriate user_time fields,converts time in 
        HH:MMp format to valid time. Otherwise prompts reentry.  
        """
        while True:
            user_time = input("""
              \rWhat time should this be executed?
            \r\tEnter as 'HH:MMp'
            \r\tEnter 'n' to cancel
            \r\tTime of day to execute: """)
            if user_time == "n":
                print("Exiting. ")
                return
            try:
                user_time = datetime.strptime(user_time, "%I:%M%p")
                break
            except ValueError:
                print("Invalid time format entered. ")
                continue
        return {"min": user_time.minute, "hour": user_time.hour}

    @staticmethod
    def cron_recurrance_fields() -> dict:
        """Determine what day(s) the notification should be sent out.
        
        Returns a dictionary containing the cronjob date fields. 
        """
        while True:
            recurring = input("""
                  \rWhen should this notification by executed?
                \r\tEnter 'everyday' for everyday until turned off. 
                \r\tEnter 'specific day' to be propmpted a date to execute. 
                \r\tEnter 'n' to cancel. 
                \r\tTimes to repeat: """)

            if recurring == "everyday":
                day, month = "*" * 2
                break
            elif recurring == "specific day":
                day   = input("Day of month: ")
                month = input("Month: ")
                break
            elif recurring == "n":
                print("Exiting. ")
                return False
            else: 
                print("Enter a valid input. ")
        return {"day": day, "month": month, "weekday": "*"}

    @staticmethod
    def record_message(current_jobs) -> dict:
        """Record a message to be sent during a notification"""
        message = input("Message: ")
        len_message = len(message)
        title =  message[0:(len(message)//4)] + datetime.now().strftime("%d-%m")
        if title in current_jobs.keys():
            overwrite = input(title, " is already a notification. Overwrite? (y, n)")
            if overwrite == "n":
                print("Exiting. ")
                return 
        print(f"Notification title: {title}")
        recorded = {"title": title, "message": message, "initialized": False}
        return recorded

    def create_notification(self) -> None:
        """ALlows user to enter a notification to initialize a cron job for. """
        while True: 
            verify = input("Creating a notification. Continue? (y, n): ")
            if verify == "n": 
                cancel = "Cancelling notification. "
                print(cancel)
                return
            elif verify != "y":
                print("Invalid input. ")
                continue
            else: 
                break
        
        self.recorded = self.record_message(self.current_jobs)
        self.title = self.recorded["title"]
        self.message = self.recorded["message"]
        self.time_fields = self.crontab_time_fields()
        self.recurrance_rate = self.cron_recurrance_fields()       

    def remove_notification(self) -> None:
        """Allow a user to delete a current notification."""
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
        command = f"echo {self.message} | msmtp -a default {self.from_email} {self.destination}"
        echo = "{ crontab -l; echo" # Escaping the additional curly braces
        crontab = "} | crontab -"
        job = f"{min_field} {hour_field} {day_of_month} {month_field} {day_of_week} {command}"
        os.system(f'{echo} "{job}"; {crontab}')
        self.recorded["initialized"] = True

    def get_current_notifications(self) -> dict:
        return self.recorded

    def get_current_jobs(self, print_jobs=False) -> dict:
        no_jobs = len(self.current_jobs) == 0
        if print_jobs:
            if no_jobs:
                print("No current jobs. ")
            else: 
                print("Active jobs: ")
                for job in current_jobs.values():
                    print(f"""\tMessage:\t\t{job[0]}
                        \r\tTime to notify:\t{job[1]}
                        \r\tTimes to repeat:\t{job[2]}
                    """)
        if no_jobs: return "No current jobs. "
        else: return self.current_jobs
        
    def get_num_jobs(self, print_num_jobs=False) -> int:
        if print_num_jobs:
            print(f"Number of active jobs: {len(self.num_jobs)}")
        else: return self.num_jobs


# Testing
if __name__ == '__main__':
    user_info = user_information()

    destination = user_info["destination"]
    email = user_info["email"]

    notification = Notification(email, destination)
    notification.create_notification()

    print(notification.get_current_notifications())