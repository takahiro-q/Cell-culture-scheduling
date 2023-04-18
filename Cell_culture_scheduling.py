import streamlit as st
import pandas as pd
import datetime as dt 
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


# tab1:create_experiment_
tab1, tab2, tab3 = st.tabs(["Data_input_form", "Schedule", "Cell_count"])

with tab1:
    EXPERIMENT_STEPS = pd.DataFrame(columns=[
    "Step",
    "Duration",
    "Medium",
    "Compounds"
])
    
    count_key = 1
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    while True:
        with col1:
            step = st.text_input("Step", key=f"step{count_key}")
        with col2:
            duration = st.number_input("Duration", key=f"duration{count_key}",
                                       min_value=0, value=1, step=1)
        with col3:
            medium = st.text_input("Medium", key=f"medium{count_key}")
        with col4:
            compounds = st.text_input("Compounds", key=f"compounds{count_key}")
        
        # データフレームにデータを追加
        EXPERIMENT_STEPS = EXPERIMENT_STEPS.append({
            "Step": step,
            "Duration": duration,
            "Medium": medium,
            "Compounds": compounds},
            ignore_index = True)
        
        with col5:
            # 続けるかどうかの確認
            answer = st.radio("continue?", ("Yes", "No"), index=1, key=f"answer{count_key}")
            if answer == 'No':
                break
    
        count_key += 1
            
    col6, col7, col8= st.columns(3)
    
    # 年、月、日の入力ボックスを作成
    with col6:
        year = st.number_input('年', value=2023, min_value=2000, max_value=2099)
    with col7:
        month = st.number_input('月', value=4, min_value=1, max_value=12)
    with col8:
        day = st.number_input('日', value=5, min_value=1, max_value=31)

with tab2:
    with st.container():

        def create_experiment_schedule(start_date):
            days = []
            end_days = []
            curr_date = start_date
        
            for data in step_list:
                #List of start dates and end dates
                days.append(curr_date.strftime("%Y-%m-%d"))
                end_days.append((curr_date + dt.timedelta(days=data[1])).strftime("%Y-%m-%d"))
        
                #Increment current date by duration of step
                curr_date += dt.timedelta(days=data[1])
        
            #Create a Dataframe
            df = pd.DataFrame({"step":EXPERIMENT_STEPS["Step"].values,"start_date": days, "end_date": end_days})
        
            #Convert dates to datetime format
            df["start_date"] = pd.to_datetime(df["start_date"])
            df["end_date"] = pd.to_datetime(df["end_date"])
        
            #Calculate additional columns
            df['days_to_start'] = (df['start_date'] - df['start_date'].min()).dt.days
            df['days_to_end'] = (df['end_date'] - df['start_date'].min()).dt.days
            df['task_duration'] = df['days_to_end'] - df['days_to_start']   
            return df
    
        
        
        def plot_experiment_schedule(schedule):
            figure = plt.figure(figsize=(10, 6))
            ax = figure.add_subplot(111)
            ax.set_title(" Differentiation Schedule")
            ax.set_xlabel("Day")
            ax.set_ylabel("Step")
        
            for i, row in schedule.iterrows():
                step = i
                task = row["task_duration"]
                start_date = row["days_to_start"]
                duration = EXPERIMENT_STEPS["Duration"]
                ax.barh(y = step, width = task, left = start_date, height=0.6, alpha=0.8, 
                        label=EXPERIMENT_STEPS.iloc[i, 0], color=f"C{i}")
                ax.xaxis.grid(True, alpha=0.5)
                xticks = np.arange(0, schedule.days_to_end.max()+1, 3)
                xticks_labels = pd.date_range(schedule.start_date.min(), end = schedule.end_date.max()).strftime("%m-%d")
                xticks_minor = np.arange(0, schedule.days_to_end.max()+1, 1)
                ax.set_xticks(xticks)
                ax.set_xticks(xticks_minor, minor=True)
                ax.set_xticklabels(xticks_labels[::3])
                
            ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
            st.pyplot(figure)
        
        # 数値型の年、月、日を結合して日付を作成
        start_date = dt.date(year, month, day)
        
        # 作業工程(データフレーム)表示
        """
        作業工程(表)
        """
        st.dataframe(EXPERIMENT_STEPS, width=1000)
        
        step_list = EXPERIMENT_STEPS[["Step", "Duration"]].values.tolist()
               
        st.header("Schedule")
        # Calculate schedule 
        schedule = create_experiment_schedule(start_date)
        st.write(schedule)
    
        st.header("Schedule_chart")
        schedule_plot = plot_experiment_schedule(schedule)
        st.write(schedule_plot)
    
    with tab3:

        st.title("Cell Count Calculator")

        # データフレームの初期化
        count_data = pd.DataFrame(columns=[
            "date",
            "measured_cells", 
            "suspension_volume",
            "required_cells",
            "Cell name",
            "Cell type",
            "Passage number",
            "method",
            "Total cell count",
            "Seeding cell count"])
        
        
        count_key = 1
        
        while True:
            # 実験を行った日付
            date = dt.date.today()
        
            # 測定した細胞数の入力
            measured_cells = st.number_input("Measured cell count (cell/mL)", key=f"measured{count_key}",
                                             min_value=0.0, value=1e+3, step=1e+3, format="%e")
        
            # 測定した細胞懸濁液のml(容量)の入力
            suspension_volume = st.number_input("Cell suspension volume (mL)", min_value=0.0, value=1.0, step=0.5,
                                                key=f"volume{count_key}")
        
            # トータルの細胞量の算出
            total_cells = measured_cells * suspension_volume
        
            # 必要細胞量
            required_cells = st.number_input("Required number of cells (cell/well) ",key=f"required{count_key}",
                                             min_value=0.0, value=1e+3, step=1e+3,  format="%e")
            
            # 細胞の名前
            cell_name = st.text_input("Cell name", key=f"name{count_key}")
            
            # 細胞の継代数
            passage = st.number_input("Passage number", key=f"passage{count_key}", min_value=0, step=1)
        
            # 播種細胞数
            seeding_cells_volume = required_cells / measured_cells
        
            # 細胞の種類の選択
            cell_type = st.selectbox("Select cell type", options=['iPS cells', 'Neural Progenitor Cells', 'Neurons'],key=f"type{count_key}")
        
            # subtype
            select_method = st.radio("What are the experimental methods used?", ("Passage", "Differentiation"), index=1, key=f"method{count_key}")
        
            # データフレームにデータを追加
            count_data = count_data.append({
                "date":date,
                "measured_cells": measured_cells, 
                "suspension_volume":suspension_volume,
                "required_cells":required_cells,
                "Cell name":cell_name,
                "Cell type":cell_type,
                "Passage number":passage,
                "method":select_method,
                "Total cell count":total_cells,
                "Seeding cell count": seeding_cells_volume},
                ignore_index = True)
            
            # 続けるかどうかの確認
            count_answer = st.radio("Do you want to continue?", ("Yes", "No"), index=1, key=f"Count_answer{count_key}")
            if count_answer == 'No':
                break
        
            count_key += 1
        
        # 最終的なデータフレームの表示
        st.write(count_data)

        count_data.to_excel(buf := BytesIO(), index=False)
        st.download_button(
            "Download",
            buf.getvalue(),
            "sample.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )