import scraper as scr
import data_manager as dm
import database_connector as db
import config as cfg
import asyncio


def main():
    dm.laptops = asyncio.run(scr.DataScraper.main())
    dm.sync_with_database(dm.laptops)
    db.add_data(dm.laptops)
    print("Workflow completed.")
if __name__ == "__main__":
    main()
