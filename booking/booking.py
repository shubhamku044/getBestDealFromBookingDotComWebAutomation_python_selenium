import os
from selenium import webdriver
import booking.constant as const
from booking.booking_filteration import BookingFilteration
from booking.booking_report import BookingReport
from prettytable import PrettyTable



class Booking(webdriver.Chrome):
    def __init__(self, driver_path="/usr/local/bin/chromedriver", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )

        currency_element.click()
        selected_currency_element = self.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element_by_id('ss')
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element_by_css_selector(
            'li[data-i="0"]'
        )
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element_by_css_selector(
            f'td[data-date="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element = self.find_element_by_css_selector(
            f'td[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_adults(self, count):
        selection_element = self.find_element_by_id('xp__guests__toggle')
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element_by_css_selector(
                'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()
            adults_value_element = self.find_element_by_id(
                'group_adults'
            )

            adults_value = adults_value_element.get_attribute(
                'value'
            )
            if int(adults_value) == 1:
                break
        while True:
            increase_adults_element = self.find_element_by_css_selector(
                'button[aria-label="Increase number of Adults"]'
            )
            increase_adults_element.click()
            adults_value_element = self.find_element_by_id(
                'group_adults'
            )

            adults_value = adults_value_element.get_attribute(
                'value'
            )
            if int(adults_value) == count:
                break

    def click_search(self):
        search_button = self.find_element_by_css_selector(
            'button[type="submit"]'
        )
        search_button.click()

    def apply_filteration(self):
        filteration =  BookingFilteration(driver=self)
        filteration.apply_star_rating(4, 5)
        filteration.sort_price_lowest_first()
    
    def report_results(self):
        hotel_boxes = self.find_element_by_id(
            'hotellist_inner'
        )
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names = ["Hotel Name", "Hotel Price", "Hotel Ratings"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
        # print(report.pull_deal_box_attributes())