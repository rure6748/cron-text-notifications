#!/usr/bin/env python3
#
"""Python module for user """
def ask_user_information(saved_info=False, filename=None) -> dict:
    if saved_info: 
            with open(f"{filename}", "r") as info:
                user_info = json.load(info)
    else:
        destination = input("Phone number or email to recieve notification: ")
        email = input("msmtp email to send notification from: ")
        user_info = {"destination": destination, "email": email}
    return user_info

def ask_user_time() -> dict:
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

def create_notification(self, message, time_fields, recurrance_rate) -> dict:
    """ALlows user to enter a notification to initialize a cron job for. 

    Example usage: 
    notif = create_notification("Hi", time_fields, recurrance_fields)
    Notification.set_notification(**notif)
    """
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
    while True: 
        message = input("Message: ")
        print(f"\n'{message}' will be delivered at {time_fields}. ")
        verify = input("Conintue? (y, n)")
        if verify == "n":
            print("Cancelling notification. ")
            return
        elif verify == "y":
            print("Message recorded. ")
            break
    date_created = 
    notification = {"message": message, 
                    "time_fields": time_fields, 
                    "recurrance_rate" : recurrance_rate}
    return notification

def remove_notification() -> None:
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
        elif verify == "y":
            break
        else:
            print("Invalid input. ")
            continue
    selection = 0
    print("Select the number by 'selection' to choose a notification to remove.")
    for key, value in self.current_jobs.items():
        print(f"""Selection:  {key}
                \rMessage:    {value[message]}
                \rTime:       {value[time_fields]}
                \rRecurrance: {value[recurrence_rate]}
                \r""")

    del current_jobs["notification to remove"]

