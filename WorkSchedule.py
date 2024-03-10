import streamlit as st
import pandas as pd

class WorkScheduleApp:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = pd.read_csv(data_file)

    def add_work(self, name, description, day, month):
        new_entry = {'Name': name, 'Description': description, 'Day': day, 'Month': month}
        new_df = pd.DataFrame([new_entry])
        self.df = pd.concat([self.df, new_df], ignore_index=True)
        self.df.to_csv(self.data_file, index=False)

    def remove_work(self, index):
        if not self.df.empty:
            self.df.drop(index, inplace=True)
            self.df.to_csv(self.data_file, index=False)

    def sort_by_month_and_day(self):
        months_map = {
            "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
            "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
        }
        self.df['Month'] = self.df['Month'].map(months_map)
        self.df = self.df.sort_values(by=['Month', 'Day'])  # Sort by month and then by day
        self.df['Month'] = self.df['Month'].map({v: k for k, v in months_map.items()})
        self.df.to_csv(self.data_file, index=False)

    def show_database(self):
        st.write(self.df)

def main():
    st.title("Work Schedule : ตารางงาน")
    app = WorkScheduleApp("workscheduledata.csv")
    name = st.text_input("ชื่องาน")
    description = st.text_input("รายละเอียดงาน")
    day = st.number_input("วันที่", min_value=1, max_value=31)
    months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", 
              "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    month = st.selectbox("เดือน", months)
    
    if st.button("Add Work"):
        if name == "":
            st.warning("กรุณาใส่ชื่องานให้ครบ" ,icon="⚠️")
        if description == "":
            st.warning("กรุณาใส่รายละเอียดงาน", icon="⚠️")
        else:
            app.add_work(name, description, day, month)
            st.success("เพิ่มงานสำเร็จ!")
    

    st.subheader("ตาราง")
    app.sort_by_month_and_day()
    app.show_database()

    if not app.df.empty:
        if st.button("Remove Work"):
            selected_index = st.number_input("ใส่ลำดับงานที่ต้องการลบ", min_value=0, max_value=len(app.df)-1)
            app.remove_work(selected_index)
            st.success("ลบงานเสร็จเรียบร้อย")
    else:
        st.write("")

if __name__ == "__main__":
    main()
