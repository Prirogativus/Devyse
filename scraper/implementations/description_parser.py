from scraper.interfaces import AbstractDescriptionParser
import configs.scraper_config as scc
import logging
from bs4 import BeautifulSoup
from typing import Literal
from rapidfuzz import process
import rapidfuzz as rf

logger = logging.getLogger(__name__)

class DescriptionParser(AbstractDescriptionParser):
    def __init__(self, 
                 selector: str = scc.olx_description_selector,
                 patterns_module: scc = scc
                 ):
        self.sc_config = patterns_module
        self.selector = selector
        self.COMPONENT_GETTERS: dict = {
            "cpu": self.get_cpu,
            "ram": self.get_ram,
            "gpu": self.get_gpu,
            "model": self.get_model,
            "storage": self.get_storage,
                                      }

    def enrich_laptop_data_dict(self, laptop_data: dict, description_page: BeautifulSoup) -> dict:
        """Enriches the laptop data dictionary with additional details extracted from the description."""
        description = self.get_description(description_page=description_page)
        title = laptop_data['title']
        return self.add_values(laptop_data,
                               description=description,
                               model=self.get_laptop_component(description, title, "model"),
                               cpu=self.get_laptop_component(description, title, "cpu"),
                               ram=self.get_laptop_component(description, title, "ram"),
                               storage=self.get_laptop_component(description, title, "storage"),
                               gpu=self.get_laptop_component(description, title, "gpu")
                               )

    def get_description(self, description_page: BeautifulSoup) -> str:
        """Extracts and returns the description text from the HTML content."""
        parent = description_page.select_one(self.selector)
        description_element = parent.find('div', recursive=True) if parent else None
        if description_element:
            description = description_element.get_text(separator="")
            logger.info(f"Description has been retrieved successfully: {description[:100]}.")
        else:
            description = "No description"
            logger.warning("Description element not found in the provided HTML.")
        return description

    def get_laptop_component(self, 
                             description: str,
                             title: str, 
                             component_type: Literal["brand", "model", "cpu", "ram", "storage", "gpu"],
                            ) -> str:
        """Extracts a specific laptop component from the description or title using regex patterns."""
        logger.info(f"Getting {component_type} from description...")
        getter = self.COMPONENT_GETTERS.get(component_type)
        pattern = self.import_pattern(component_type)
        if not getter:
            raise ValueError(f"No getter function found for component type: {component_type}")
        return getter(description, title, pattern)
    
    def import_pattern(self, component_type: str):
        """Imports the regex pattern for the specified component type from the configuration module."""
        pattern = getattr(self.sc_config, f"{component_type}_pattern", None)
        if not pattern:
            raise ValueError(f"No regex pattern found for component type: {component_type}")
        return pattern
    
    def get_model(self, description: str, title: str, pattern) -> str:
        """Extracts the laptop model from the description or title using the model regex pattern."""
        match = self.search_in_description(pattern, description)
        if match!= None:
            return match
        else: match = self.search_in_title(pattern, title)
        if match!= None:
            return match
        logger.warning(f"No model found in description or title.")
        return "Other/Unknown"
    
    def get_model_brand():
        pass
    def get_model_series():
        pass
   
    def get_cpu(self, description: str, title: str, pattern):
        secondary_patterns = [
                    self.sc_config.cpu_minimal_pattern, 
                    self.sc_config.cpu_apple_pattern
                    ]
        """Extracts the CPU information from the description or title using multiple regex patterns."""
        if match := self.search_in_description(pattern, description):
            return match
        elif match := self.search_in_title(pattern, title):
            return match
        else:
            for sp in secondary_patterns:
                if match := self.search_in_description(sp, description):
                    return match
                elif match := self.search_in_title(sp, title):
                    return match
        logger.warning(f"No cpu found in description or title.")
        return "Other/Unknown"

    def get_ram(self, description: str, title: str, pattern):
        """Extracts the RAM information from the description or title using the RAM regex pattern."""
        match = self.search_in_description(pattern, description)
        if match!= None:
            return match
        else: match = self.search_in_title(pattern, title)
        if match!= None:
            return match
        logger.warning(f"No model found in description or title.")
        return "Other/Unknown"

    def get_storage(self, description: str, title: str, pattern):
        """Extracts the storage information from the description or title using the storage regex pattern."""
        match = self.search_in_description(pattern, description)
        if match!= None:
            return match
        else: match = self.search_in_title(pattern, title)
        if match!= None:
            return match
        logger.warning(f"No storage found in description or title.")
        return "Other/Unknown"
        
    def get_gpu(self, description: str, title: str, pattern):
        """Extracts the GPU information from the description or title using the GPU regex pattern."""
        match = self.search_in_description(pattern, description)
        if match!= None:
            return match
        else: match = self.search_in_title(pattern, title)
        if match!= None:
            return match
        logger.warning(f"No gpu found in description or title.")
        return "Other/Unknown"

    def search_in_description(self, description: str, regex_pattern = None, rf_list = None ) -> str:
        """Searches for a component in the description using the provided regex pattern."""
        if rf_list:
            match = self.search_by_rapidfuzz(rf_list, description)
            return match
        elif regex_pattern:
            match = self.search_by_regex(regex_pattern, description)
            return match
        else: 
            raise ValueError("No list or regex provided for search_in_description function.")


    
    def search_in_title(self, pattern, title: str) -> str:
        """Searches for a component in the title using the provided regex pattern."""
        match = pattern.search(title)
        if match:
            component_value = match.group(0).strip()
            logger.info(f"Found component: {component_value} in title.")
            return component_value
        return None
    
    def search_by_rapidfuzz(rf_list: list[str], description: str):
        """Searches a word in a given text using rapidfuzz extraction method."""
        for word in rf_list:
            match = process.extractOne(word, description.split(), scorer=rf.fuzz.ratio)
            if match and match > 70:
                logger.info(f"Found component: {match} in description using rapidfuzz.")
                return match
            else: raise ValueError(f"No rapidfuzz match from this list: {rf_list},\n in the description: {description}")
        
    def search_by_regex(regex_pattern: str, description: str):
        match = regex_pattern.search(description)
        if match:
            component_value = match.group(0).strip()
            logger.info(f"Found component: {component_value} in descriprion using regex: {regex_pattern}")
            return component_value
        else: raise ValueError(f"No regex match for this pattern: {regex_pattern}, \n in this description: {description}")
    
    def add_values(self, 
                   laptop_data: dict, 
                   description: str,
                   model: str,
                   cpu: str,
                   ram: str,
                   storage: str,
                   gpu: str
                   ) -> dict:
        """Adds extracted values to the laptop data dictionary."""
        laptop_data.update(
            {   
            'description': description,
            'model': model,
            'cpu': cpu,
            'ram': ram,
            'storage': storage,
            'gpu': gpu,
            })
        return laptop_data