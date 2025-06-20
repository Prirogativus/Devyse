from database_connector import get_data, add_data, delete_data

laptops = []


def sync_with_database(laptops: list):
    db_laptops = get_data()
    if db_laptops != None:
        new_laptops = laptops - db_laptops
        laptops_to_delete = db_laptops - laptops
        for laptop in new_laptops:
            print(f"Adding new laptop to the database: {laptop['title']}, ID: {laptop['marketplace_ID']}")
            add_data([laptop])
        for laptop in laptops_to_delete:
            print(f"Deleting laptop from the database: {laptop['title']}, ID: {laptop['marketplace_ID']}")
            delete_data({laptop})
    else: 
        pass
    
        
        
