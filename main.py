import time
import requests
import gspread
import pytz
import pandas as pd

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from configs import LOYVERSE_URL, LOYVERSE_TOKEN, API_PATH, GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_SHEET_URL

class LoyverseReport:
    def __init__(self):
        self.url = LOYVERSE_URL
        self.token = LOYVERSE_TOKEN
        self.api_path = API_PATH
        self.created_at_min, self.created_at_max = self.find_back_to_six_month()
        self.header = {
            "Authorization" : f"Bearer {LOYVERSE_TOKEN}"
        }
    
    def get_pos_devices_data(self):
        url = f"""{self.url}{self.api_path["GET_POST_DEVICES"]}"""
        response = requests.get(url, headers=self.header)
        data = response.json()
        
        return { item["id"]: item["name"] for item in data["pos_devices"]}
    
    def get_stores_data(self):
        url = f"""{self.url}{self.api_path["GET_STORES"]}"""
        response = requests.get(url, headers=self.header)
        data = response.json()
        
        return { item["id"]: item["name"] for item in data["stores"]}
    
    def get_receipts_data(self, cursor=""):
        url = f"""{self.url}{self.api_path["GET_RECEIPTS"]}?cursor={cursor}&created_at_max={self.created_at_max}&created_at_min={self.created_at_min}"""
        response = requests.get(url, headers=self.header)
        data = response.json()
        
        next_items = []
        
        if "cursor" in data.keys():
            time.sleep(1)
            next_items = self.get_receipts_data(cursor=data["cursor"])
            
        return data["receipts"] + next_items
    
    def get_customers_data(self, cursor=""):
        url = f"""{self.url}{self.api_path["GET_CUSTOMERS"]}?cursor={cursor}"""
        response = requests.get(url, headers=self.header)
        data = response.json()
        
        next_items = []
        
        if "cursor" in data.keys():
            time.sleep(1)
            next_items = self.get_customers_data(cursor=data["cursor"])
            
        return data["customers"] + next_items
    
    def get_employees_data(self, cursor=""):
        url = f"""{self.url}{self.api_path["GET_EMPLOYEES"]}?cursor={cursor}"""
        response = requests.get(url, headers=self.header)
        data = response.json()
        
        next_items = []
        
        if "cursor" in data.keys():
            time.sleep(1)
            next_items = self.get_employees_data(cursor=data["cursor"])
            
        return data["employees"] + next_items
    
    def get_catagories_data(self, cursor=""):
        url = f"""{self.url}{self.api_path["GET_CATEGORIES"]}?cursor={cursor}"""
        response = requests.get(url, headers=self.header)
        data = response.json()
        
        next_items = []
        
        if "cursor" in data.keys():
            time.sleep(1)
            next_items = self.get_catagories_data(cursor=data["cursor"])
            
        return data["categories"] + next_items
    
    def get_items_data(self, cursor=""):
        url = f"""{self.url}{self.api_path["GET_ITEMS"]}?cursor={cursor}"""
        response = requests.get(url, headers=self.header)
        data = response.json()
        
        next_items = []
        
        if "cursor" in data.keys():
            time.sleep(1)
            next_items = self.get_items_data(cursor=data["cursor"])
            
        return data["items"] + next_items
    
    def format_customers(self, customers):
        return { item["id"]: {"name": item["name"], "phone_number": item["phone_number"]} for item in customers}
    
    def format_items(self, items):
        return { item["id"]: {"item_name": item["item_name"], "category_id": item["category_id"]} for item in items}
    
    def format_employees(self, employees):
        return { item["id"]: item["name"] for item in employees}
    
    def format_categories(self, categories):
        return { item["id"]: item["name"] for item in categories}
    
    def get_datetime_format(self, datetime_string):
        date = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        date = date + timedelta(hours=7)
        return date.strftime("%d/%m/%y %H:%M")
    
    def reformat_receipts(self, receipts, items, categories, pos_devices, stores, employees, customers):
        new_receipts = []
        for receipt in receipts:
            for item in receipt["line_items"]:
                if item["item_id"] not in items.keys():
                    category = None
                elif items[item["item_id"]] is None:
                    category = None
                elif items[item["item_id"]]["category_id"] is None:
                    category = None
                else:
                    category = categories[items[item["item_id"]]["category_id"]]
                    
                if receipt["customer_id"] is None:
                    customer_name = None
                    customer_phone = None
                else:
                    customer_name = customers[receipt["customer_id"]]["name"]
                    customer_phone = str(customers[receipt["customer_id"]]["phone_number"]) if customers[receipt["customer_id"]]["phone_number"] else None
                    
                new_receipts_item =({
                    "วันที่": self.get_datetime_format(receipt["receipt_date"]),
                    "เลขที่ใบเสร็จ": receipt["receipt_number"],
                    "ประเภทใบเสร็จ": receipt["receipt_type"],
                    "ประเภท": category,
                    "รหัส sku สินค้า": item["sku"],
                    "รายการ": item["item_name"],
                    "ตัวแปร": item["variant_name"],
                    "ปรับเปลี่ยนการใช้งาน": None,
                    "จำนวน": item["quantity"],
                    "ยอดขายรวม": item["total_money"],
                    "ส่วนลด": item["total_discount"],
                    "ยอดขายสุทธิ": item["gross_total_money"],
                    "ต้นทุนของสินค้า": item["cost_total"],
                    "กำไรรวม": item["gross_total_money"] - item["cost_total"],
                    "ภาษี": receipt["total_tax"],
                    "ระบบขายหน้าร้าน": pos_devices[receipt["pos_device_id"]],
                    "ร้านค้า": stores[receipt["store_id"]],
                    "ชื่อแคชเชียร์": employees[receipt["employee_id"]],
                    "ชื่อลูกค้า": customer_name,
                    "รายชื่อติดต่อลูกค้า": customer_phone,
                    "ความคิดเห็น": item["line_note"] if item["line_note"] else "",
                    "สถานะ": "ยกเลิกแล้ว" if receipt["cancelled_at"] else "ปิด"
                })
                
                new_receipts.append(new_receipts_item)
                
        return new_receipts
    
    def find_back_to_six_month(self):
        date = datetime.today().replace(day=1)
        end_of_month = date + relativedelta(months=+1)
        before_six_month = date - relativedelta(months=+5)
        return before_six_month.strftime("%Y-%m-%dT00:00:00.000Z"), end_of_month.strftime("%Y-%m-%dT00:00:00.000Z")
    
    def generate_report(self):
        receipts = self.get_receipts_data()
        print(f"""Detected {len(receipts)} receipts """)
        items = self.format_items(self.get_items_data())
        print(f"""Detected {len(items.keys())} items """)
        categories = self.format_categories(self.get_catagories_data())
        print(f"""Detected {len(categories.keys())} categories """)
        pos_devices = self.get_pos_devices_data()
        print(f"""Detected {len(pos_devices.keys())} pos_devices """)
        stores = self.get_stores_data()
        print(f"""Detected {len(stores.keys())} stores """)
        employees = self.format_employees(self.get_employees_data())
        print(f"""Detected {len(employees.keys())} employees """)
        customers = self.format_customers(self.get_customers_data())
        print(f"""Detected {len(customers.keys())} customers """)
        report = self.reformat_receipts(receipts, items, categories, pos_devices, stores, employees, customers)
        print(f"""Generating.. {len(report)} records """)
        
        df = pd.DataFrame(report)
        gc = gspread.service_account(filename=GOOGLE_APPLICATION_CREDENTIALS)
        sh = gc.open_by_url(GOOGLE_SHEET_URL)
        worksheet = sh.get_worksheet(0)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def main() -> None:
    print("Starting ...")
    LoyverseReport().generate_report()
    print("Done ...")
    
    
if __name__ == "__main__":
    main()