import pandas as pd
from datetime import datetime

def calculate_attendance(df):
    #Remove Duplicates
    students_present = df['Full Name']
    students_present = list(dict.fromkeys(students_present))

    df2 = pd.DataFrame(columns = ['Name', 'Time Attended']) 
    df2['Name'] = students_present

    student_attendance = []
    time_format = '%m/%d/%Y, %I:%M:%S %p'
    meeting_start_time = datetime.strptime('9/3/2020, 8:56:06 AM', time_format)
    meeting_end_time = datetime.strptime('9/3/2020, 10:00:00 AM', time_format)
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