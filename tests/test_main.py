from unittest import mock
import main

def test_main_workflow_runs_without_exception():
    with mock.patch("scraper.data_scraper.DataScraper.main", return_value=[]), \
         mock.patch("data.data_manager.sync_with_database"), \
         mock.patch("data.database_connector.add_data"):
        main.main()