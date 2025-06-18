import scraper as scr
import data_manager as dm
import database_connector as db
import config as cfg


def main():
    dm.laptops = scr.main()
    db.add_data(dm.laptops)

if __name__ == "__main__":
    main()