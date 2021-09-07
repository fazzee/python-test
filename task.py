from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.PDF import PDF
import os
import re
import time

FILES = "output" 
URL = "https://itdashboard.gov/"  
XLS_AGENCY = "Agencies"  
XLS_TABLE = "Table"  
BUTTON = "DIVE IN"  
OPEN_AGENCY = 0 


class Dashboard:
    uii_links = []
    headers = []
    agencies_data = []
    investment_table = {}

    def __init__(self, url):
        self.browser = Selenium()
        self.lib = Files()
        self.pdf = PDF()
        self.browser.set_download_directory(os.path.join(os.getcwd(), f"{FILES}/"))
        self.browser.open_available_browser(url)

    def click_dive_in(self, keyword):
        self.browser.wait_until_page_contains(keyword)
        self.browser.find_element('//a[@class="btn btn-default btn-lg-2x trend_sans_oneregular"]').click()

    def find_agencies(self):
        time.sleep(5)
        agencies = self.browser.find_elements('//div[@id="agency-tiles-widget"]//div[@class="col-sm-4 text-center noUnderline"]')
        found_agencies = []
        amounts = []
        for agency in agencies:
            agency_split = agency.text.split("\n")
            found_agencies.append(agency_split[0])
            amounts.append(agency_split[2])
        self.agencies_data = {'Agency': found_agencies, 'Amount': amounts}

    def agency_to_xls(self, filename):
      
        w = self.lib.create_workbook(f"{FILES}/{filename}.xlsx")
        w.append_worksheet("Sheet", self.agencies_data)
        w.save()

    def table_header(self):
        while True:
            try:
                all_heads = self.browser.find_element(
                    '//table[@class="datasource-table usa-table-borderless dataTable no-footer"]').find_element_by_tag_name(
                    "thead").find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("th")
                if all_heads:
                    break
            except:
                time.sleep(1)
        for head in all_heads:
            self.headers.append(head.text)

    def click_uii_links(self):
        tr_elements = self.browser.find_elements('//tr[@role="row"]')
        for tr_element in tr_elements[2:]:
            td_elements = tr_element.find_elements_by_tag_name('td')
            try:
                a_element = tr_element.find_element_by_tag_name('a').get_attribute("href")
            except:
                a_element = ''
            if a_element:
                self.uii_links.append(
                    {"link": a_element, "investment_title": td_elements[2].text, "uii": td_elements[0].text}
                )

    def open_agency(self, agency_number):

        self.browser.find_elements(
            '//div[@id="agency-tiles-widget"]//div[@class="col-sm-4 text-center noUnderline"]//div[@class="row top-gutter-20"]//div[@class="col-sm-12"]')[
            agency_number].click()
        self.table_header()
        for head in self.headers:
            self.investment_table[head] = []
        while True:
            current_label = self.browser.find_element("investments-table-object_info").text
            all_rows = self.browser.find_element("investments-table-object").find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr")
            for row in all_rows:
                for i, data in enumerate(row.find_elements_by_tag_name("td")):
                    try:
                        self.investment_table[self.headers[i]].append(data.text)
                    except:
                        self.investment_table[self.headers[i]].append("")
            self.click_uii_links()
            if self.browser.find_element('investments-table-object_next').get_attribute(
                    "class") == 'paginate_button next disabled':
                break
            else:
                self.browser.find_element('investments-table-object_next').click()
                while True:
                    if current_label != self.browser.find_element("investments-table-object_info").text:
                        break
                    time.sleep(1)

    def investment_to_excel(self, filename):
        w = self.lib.create_workbook(f"{FILES}/{filename}.xlsx")
        w.append_worksheet("Sheet", self.investment_table)
        w.save()

    def download_pdf(self):
        for url in self.uii_links:
            self.browser.go_to(url["link"])
            flag_time = time.time() + 10
            while True:
                try:
                    if flag_time <= time.time():
                        break
                    pdf_link = self.browser.find_element('//*[contains(@id,"business-case-pdf")]//a').get_attribute("href")
                    if pdf_link:
                        self.browser.find_element('//div[@id="business-case-pdf"]').click()
                        while True:
                            try:
                                time.sleep(2)
                                if self.browser.find_element('//div[@id="business-case-pdf"]').find_element_by_tag_name("span"):
                                    time.sleep(1)
                                else:
                                    break
                            except:
                                if self.browser.find_element('//*[contains(@id,"business-case-pdf")]//a[@aria-busy="false"]'):
                                    time.sleep(1)
                                    break
                        break
                except:
                    time.sleep(1)

    def compare_pdf_with_title(self):
        self.browser.go_to(URL)
        for link_item in self.uii_links:
            try:
                file_name = f'output/{link_item["uii"]}.pdf'
                new_text = self.pdf.get_text_from_pdf(file_name, 1)
                new_string = re.split(r'Bureau:|Section B', new_text[1])[1]
                investment_title = re.split(r'Name of this Investment|2.', new_string)[1].replace(': ', '')
                uii_text = re.split(r'Name of this Investment|2.', new_string)[2].replace(
                    ' Unique Investment Identifier (UII): ', '')
                if link_item["uii"] == uii_text:
                    print(f'Unique Investment Identifier (UII): {link_item["uii"]} found in PDF ({file_name}).')
                if link_item["investment_title"] == investment_title:
                    print(f'Name of this Investment: {link_item["investment_title"]} found in PDF ({file_name}).')
            except:
                pass

    def close_all_browsers(self):
        self.browser.close_all_browsers()


if not os.path.exists(FILES):
    os.mkdir(FILES)


if __name__ == "__main__":
    dashboard = Dashboard(url=URL)
    try:
        dashboard.click_dive_in(BUTTON)
        dashboard.find_agencies()
        dashboard.agency_to_xls(XLS_AGENCY)
        dashboard.open_agency(OPEN_AGENCY)
        dashboard.investment_to_excel(XLS_TABLE)
        dashboard.download_pdf()
        dashboard.compare_pdf_with_title()
    finally:
        dashboard.close_all_browsers()
