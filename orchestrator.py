import scraper as scr
import data_manager as dm
import database_connector as db
import config as cfg


def main():
    dm.laptops = scr.main()
    dm.sync_with_database(dm.laptops)

if __name__ == "__main__":
    main()
