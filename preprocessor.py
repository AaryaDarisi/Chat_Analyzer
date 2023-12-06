import re
import pandas as pd
def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s"
    msg = re.split(pattern, data)[2:]
    msg_new = []
    indices = []
    for i in range(len(msg)):
        if (1):
            msg_new.append(msg[i])
            indices.append(i)
    dates = re.findall(pattern, data)
    new_dates = []
    for i in range(len(dates)):
        if (i in indices):
            new_dates.append(dates[i])
    df = pd.DataFrame({"message": msg_new, "date": new_dates})
    try:
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%y, %I:%M %p - ")
    except:
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%y, %I:%M %p - ")
    finally:
        users = []
        messages = []
        for m in df["message"]:
            #     print(m)
            splitted = re.split('([\w\W]+?):\s', m)
            #     print(splitted)
            if splitted[1:]:
                #         print("entered if")
                users.append(splitted[1])
                messages.append(splitted[2])
            else:
                users.append('group notification')
                messages.append(splitted[0])
        df["User"] = users
        df["message"] = messages
        new_df = pd.DataFrame({"Date": df["date"], "User": df["User"], "Message": df["message"]})
        new_df["year"] = new_df["Date"].dt.year
        new_df["month"] = new_df["Date"].dt.month_name()
        new_df["day"] = new_df["Date"].dt.day
        new_df["hour"] = new_df["Date"].dt.hour
        new_df["minute"] = new_df["Date"].dt.minute
        return new_df