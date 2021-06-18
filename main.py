from booking.booking import Booking

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency='USD')
        bot.select_place_to_go('new york')
        bot.select_dates(check_in_date='2021-06-28', check_out_date='2021-07-02')
        bot.select_adults(10)
        bot.click_search()
        bot.apply_filteration()
        bot.refresh()
        bot.report_results()

except Exception as e:
    if 'in PATH' in str(e):
        print("This is a problem running this program using command line interface")
    else:
        raise
