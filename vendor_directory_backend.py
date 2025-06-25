import pandas as pd
from datetime import datetime, timedelta

def load_vendors(filepath="Directory_Of_Prequalified and Registered Contractors.rtf.xlsx - Sheet1.csv"):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    vendors = []
    vendor = {
        "Vendor Number": "",
        "Vendor Name": "",
        "Contact Person": "",
        "Status": "",
        "Shipping Address": "",
        "Phone": "",
        "Email": "",
        "Expiry Date": "",
        "Work Classes": []
    }

    for line in lines:
        if "," in line and line.split(",")[0].strip().isdigit(): 
            if vendor["Vendor Number"]:  
                vendors.append(vendor.copy())
                vendor["Work Classes"] = []
            parts = [p.strip() for p in line.split(",")]
            vendor["Vendor Number"] = parts[0]
            vendor["Vendor Name"] = parts[1] if len(parts) > 1 else ""
            vendor["Contact Person"] = parts[2] if len(parts) > 2 else ""
            vendor["Status"] = parts[3] if len(parts) > 3 else ""

        elif "Shipping Address:" in line:
            vendor["Shipping Address"] = line.split("Shipping Address:")[-1].strip()

        elif "Phone Number:" in line:
            vendor["Phone"] = line.split("Phone Number:")[-1].strip()

        elif "Email:" in line:
            vendor["Email"] = line.split("Email:")[-1].strip()

        elif "Prequalification Expiration Date:" in line:
            vendor["Expiry Date"] = line.split("Prequalification Expiration Date:")[-1].strip()

        elif "Work Class:" in line:
            work_class = line.split("Work Class:")[-1].strip()
            vendor["Work Classes"].append(work_class)

    if vendor["Vendor Number"]:
        vendors.append(vendor)

    df = pd.DataFrame(vendors)
    return df


df = load_vendors("Directory_Of_Prequalified and Registered Contractors.rtf.xlsx - Sheet1.csv")


def get_vendor_by_name(name):
    return df[df["Vendor Name"].str.contains(name, case=False, na=False)]


def get_vendor_number(name):
    result = get_vendor_by_name(name)
    return result.iloc[0]["Vendor Number"] if not result.empty else None


def get_by_work_class(code):
    return df[df["Work Classes"].apply(lambda classes: any(code in wc for wc in classes))]


def get_expiring_soon(days=90):
    today = datetime.today()
    deadline = today + timedelta(days=days)

    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%b-%d-%Y")
        except:
            return None

    df["Parsed Expiry"] = df["Expiry Date"].apply(parse_date)
    return df[df["Parsed Expiry"].notnull() & (df["Parsed Expiry"] <= deadline)]



