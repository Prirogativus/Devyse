import csv
import data.database_connector as db
import logging
import os


output_folder = "output"
os.makedirs(output_folder, exist_ok=True)
file_path = os.path.join(output_folder, "laptops.csv")
data = db.get_data()
fieldnames = db.LaptopListing.__table__.columns.keys()
def export_to_csv(data, file_path):
    with open(file_path, mode='w', newline='', encoding="utf-8") as file:
         csv_writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=':')
         csv_writer.writeheader()
         for d in data:
              row = {
                    "marketplace_id": d.marketplace_id,
                    "title": d.title,
                    "price": d.price,
                    "model": d.model,
                    "cpu": d.cpu,
                    "gpu": d.gpu,
                    "ram": d.ram,
                    "storage": d.storage,
                    "status": d.status,
                    "location": d.location,
                    "appearance_time": d.appearance_time.isoformat() if d.appearance_time else None,
                    "disappearance_time": d.disappearance_time.isoformat() if d.disappearance_time else None,
                    #"link": d.link,
                    #"description": d.description
              }
              csv_writer.writerow(row)

export_to_csv(data, file_path)