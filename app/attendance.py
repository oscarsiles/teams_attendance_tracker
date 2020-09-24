import pandas as pd
from datetime import datetime

def calculate_attendance(df, end_time):
    #Remove Duplicates
    students_present = df['Full Name']
    students_present = list(dict.fromkeys(students_present))

    df2 = pd.DataFrame(columns = ['Name', 'Time Attended']) 
    df2['Name'] = students_present

    student_attendance = []
    time_format = '%m/%d/%Y, %I:%M:%S %p'

    #Every browser has a different time format
    browser_time_format = '%H:%M'

    #Convert time returned from browser into format similar to MS Teams attendance sheet
    time2 = datetime.strptime(end_time, browser_time_format).strftime('%I:%M:%S %p')

    

    # get meeting start time from first row in attendance sheet
    meeting_start_time = df['Timestamp'][0]

    # get meeting date by separating date and time into lists
    time_split = meeting_start_time.split(',')
    meeting_date = time_split[0]

    print(f' END TIME:{end_time}')

    meeting_end_time = meeting_date + ", " + time2
    print(f'MEETING END TIME:{meeting_end_time}')
    meeting_start_time = datetime.strptime(meeting_start_time, time_format)
    meeting_end_time = datetime.strptime(meeting_end_time, time_format)
    time_attended = meeting_end_time - meeting_start_time

    for i in df2.index:
        student_join_time = meeting_start_time
        student_leave_time = meeting_end_time
        time_attended = meeting_end_time - meeting_end_time
        for j in df.index:
            if df2['Name'][i] == df['Full Name'][j]:
                if df['User Action'][j] == "Joined before":
                    student_join_time = meeting_start_time
                    time_attended = meeting_end_time - student_join_time
                if df['User Action'][j] == 'Left':
                    student_leave_time = datetime.strptime(df['Timestamp'][j], time_format)
                    time_attended = time_attended - (meeting_end_time - student_leave_time)
                if df['User Action'][j] == "Joined":
                    student_join_time = datetime.strptime(df['Timestamp'][j], time_format)
                    time_attended = time_attended + (meeting_end_time - student_join_time)
            df2['Time Attended'][i] = time_attended

    return df2