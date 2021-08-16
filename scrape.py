from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import csv

RHCE = "RHCE"
CISSP = "CISSP"
CISA = "CISA"
MCSA = "MCSA"
IT = "IT"
lin = "Linkedin"
company = "Company"
employeesh = "Employees"
notesh = "Recorded"

headers = [company, lin, employeesh, RHCE, CISSP, CISA, MCSA, IT, notesh]

def get_index():
    pass

def rand_wait(t0=5, t1=10):
    return time.sleep(random.randrange(t0, t1))


def parse_companies(in_path):

    with open(in_path, newline='') as csvf:
        r = csv.reader(csvf)
        companies = []
        in_headers = []
        for i, row in enumerate(r):
            j = i - 1
            if i == 0: # skip the header
                in_headers = row
                continue
            blank = ['']*len(headers)
            companies.append(blank.copy())
            # print(companies)
            # print(j)
            # print(row)
            companies[j][headers.index(company)] = row[in_headers.index(company)]
            companies[j][headers.index(lin)] = row[in_headers.index(lin)]
        return companies


def login(driver, user, passwd):

    rand_wait(8,10)
    username = driver.find_element(By.XPATH, '//*[@id="session_key"]')
    username.clear()
    username.send_keys(user)
    rand_wait(2,3)

    password = driver.find_element(By.XPATH, '//*[@id="session_password"]')
    password.send_keys(passwd)
    rand_wait(2,3)
    password.send_keys(Keys.RETURN)
    rand_wait(2,3)


def write_row(row, out_path, opt):
    with open(out_path, opt) as csvf:
        w = csv.writer(csvf)
        w.writerow(row)


def employee_size(driver, debug, cid):
    # TODO: can fall back to label the company name if URL fails
    url = "https://www.linkedin.com/company/" + cid + "/about"
    try:
        driver.get(url)
        if not(debug):
            rand_wait()
        company_size_elem = driver.find_element_by_class_name("org-page-details__employees-on-linkedin-count")
        employees = str(company_size_elem.text.strip().split()[0])
        print("employees: " + employees)
        if not(debug):
            rand_wait()
        return int(employees.replace(',','')), url
    except Exception as e:
        print("Failed getting employee size data. With error: " + str(e))
        print("Continuing...")
        if not (debug):
            rand_wait()
        return None

def include(driver, debug, url):
    notes = ""
    try:
        driver.get(url)
        if not(debug):
            rand_wait()
        print("url: " + str(url))
        notes += "url: " + str(url)
        try:
            value_elem = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/section/div[1]/div[1]/div[2]/div/ul/li[1]/label/strong")
            # /html/body/main/div[1]/div/section/div[1]/div[1]/div[2]/div/ul/li[1]/label/strong
            # value_elem = driver.find_element_by_class("t-14")
            print("finding results element: " + str(value_elem))
        except Exception as e:
            print("Could not find value at path...return 0")
            return 0, notes
        print("value elem: " + str(value_elem))
        value = value_elem.text
        print("value: " + str(value))
        if not(debug):
            rand_wait()
        print("cleaning value")
        value = str(value.strip().split()[0])
        print("cleaned value: " + str(value))
        return value, url
    except Exception as e:
        print("Failed getting "+type+" data. With error: " + str(e) + "\nContinuing...")
        # if not (debug):
        #     rand_wait()
        return None, notes


def include_function(driver, debug, cname):
    url = "https://www.linkedin.com/sales/search/people?companyIncluded="+ cname.replace(',','') + "&companyTimeScope=CURRENT&functionIncluded=13"
    return include(driver, debug, url)


def include_cert(driver, debug, cname, type):
    url = "https://www.linkedin.com/sales/search/people?companyIncluded="+ cname.replace(',','') +"&companyTimeScope=CURRENT&keywords="+type
    return include(driver, debug, url)


def company_id(c):
    url = c[headers.index(lin)]
    cid = url.split('/')[-2]
    return cid


def scrape(driver, debug, c):
    cid = company_id(c)
    print("CompanyID")
    print(cid)
    try:
        employees, notes = employee_size(driver, debug, cid)
        c[headers.index(employeesh)] = employees
        c[headers.index(notesh)] = 'employees: ' + notes
    except Exception as e:
        print("Failed getting employee data for " + cid + ". With error: " + str(e) + "Continuing...")
    cname = c[headers.index(company)]
    try:
        rhce_certified, notes = include_cert(driver, debug, cname, RHCE)
        c[headers.index(RHCE)] = rhce_certified
        c[headers.index(notesh)] = c[headers.index(notesh)] + ' ' + RHCE + ': ' + notes

    except Exception as e:
        print("Failed getting RHCE data for " + cid + ". With error: " + str(e) + "Continuing...")
    try:
        cissp_certified, notes = include_cert(driver, debug, cname, CISSP)
        c[headers.index(CISSP)] = cissp_certified
        c[headers.index(notesh)] = c[headers.index(notesh)] + ' ' + CISSP + ': ' + notes

    except Exception as e:
        print("Failed getting CISSP data for " + cid + ". With error: " + str(e) + "Continuing...")
    try:
        cisa_certified, notes = include_cert(driver, debug, cname, CISA)
        c[headers.index(CISA)] = cisa_certified
        c[headers.index(notesh)] = c[headers.index(notesh)] + ' ' + CISA + ': ' + notes

    except Exception as e:
        print("Failed getting CISA data for " + cid + ". With error: " + str(e) + "Continuing...")
    try:
        mcsa_certified, notes = include_cert(driver, debug, cname, MCSA)
        c[headers.index(MCSA)] = mcsa_certified
        c[headers.index(notesh)] = c[headers.index(notesh)] + ' ' + MCSA + ': ' + notes

        it_function, notes = include_function(driver, debug, cname)
        c[headers.index(IT)] = it_function
        c[headers.index(notesh)] = c[headers.index(notesh)] + ' ' + IT + ': ' + notes
    except Exception as e:
        print("Failed getting MCSA data for "+cid+". With error: " + str(e) + "Continuing...")



def main(driver, debug, user, passwd, in_path, out_path):

    try:
        login(driver, user, passwd)
    except Exception as e:
        print("Could NOT login fatal error: " + str(e))
        return

    if not(debug):
        rand_wait()

    companies = parse_companies(in_path)

    write_row(headers, out_path, 'w')
    for c in companies:
        print("Company")
        scrape(driver, debug, c)
        print(c)
        write_row(c, out_path, 'a')


if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser(description='A LinkedIn scraper.')
    parser.add_argument('--debug', action="store", dest='debug', default=False)
    parser.add_argument('--user', action="store", dest='user', default="")
    parser.add_argument('--pass', action="store", dest='passwd', default="")
    parser.add_argument('--out_path', action="store", dest='out_path', default="out.csv")
    parser.add_argument('--in_path', action="store", dest='in_path', default="in.csv")
    args = parser.parse_args()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.linkedin.com/")
    main(driver, args.debug, args.user, args.passwd, args.in_path, args.out_path)
    # input("Press 'Enter' to close...")
    driver.close()
